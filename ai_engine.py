"""
AI ENGINE v7 — local machine-learning strategy (no external AI APIs).
FULL ANALYSIS + AI:
  • Per-pair market analysis: momentum vs mean-reversion tendency (lag-1 autocorrelation),
    volatility profile, drift — reported per pair.
  • AI model: HistGradientBoosting classifier per pair on ~40 engineered features
    (returns, candle anatomy, RSI/stoch/MACD/BB/ATR, drift, streaks, S/R position, time),
    predicting next-candle direction.
  • Walk-forward honesty: train 60% / validation 20% (threshold calibration) / test 20%.
    Signals fire ONLY when model probability >= calibrated threshold (val precision >= 56%).
  • Live: same battle-tested flow — early signal ~25s before candle open (with chart),
    GO/CANCEL revalidation at open, 1-min expiry, auto-grading, cool-down, mute, 1/min cap.
"""
import asyncio, json, math, os, time, random, warnings
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
warnings.filterwarnings("ignore")
load_dotenv("/home/user/.env")
from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync
from pa_engine import is_forex_otc, wilder
from chart_style import render_chart
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier

TOKEN, CHATID = os.environ["TELEGRAM_BOT_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}"
IST = timezone(timedelta(hours=5, minutes=30))
POFF, PERIOD, WANT = 7200, 60, 6000
BREAKEVEN = 1 / 1.92
RUN_MINUTES = float(os.environ.get("RUN_MINUTES", "0"))
PRE_SEC = 32
COOLDOWN_S = 600
KEEP, WARMUP = 700, 320
MIN_VAL_PREC = 0.56           # calibration target on validation
THR_GRID = np.arange(0.52, 0.71, 0.01)

MODELS, THR, STATS, store, cur_min = {}, {}, {}, {}, {}
pending = []
score = {"W": 0, "L": 0, "T": 0}
pair_score = {}
sig_no, cancels = 0, 0
pre = {"minute": None, "cands": [], "task": None}
armed = None
last_pre = {}
recent = []
pause_until = 0.0

def log(m): print(f"[{datetime.now(IST):%H:%M:%S}] {m}", flush=True)

def _post_msg(text):
    try:
        for i in range(0, len(text), 3900):
            requests.post(f"{API}/sendMessage", data={"chat_id": CHATID, "text": text[i:i+3900]}, timeout=15)
    except Exception as e:
        print("TG error:", e, flush=True)

def _post_photo(png, caption):
    try:
        requests.post(f"{API}/sendPhoto", data={"chat_id": CHATID, "caption": caption[:1024]},
                      files={"photo": ("signal.png", png, "image/png")}, timeout=30)
    except Exception as e:
        print("TG photo error:", e, flush=True)

async def tg(t): await asyncio.to_thread(_post_msg, t)
async def tg_photo(p, c): await asyncio.to_thread(_post_photo, p, c)

def muted(a):
    s = pair_score.get(a)
    return bool(s) and (s["L"] - s["W"]) >= 3

# ---------------- feature engineering ----------------
def features(df):
    c, o, h, l = df["close"], df["open"], df["high"], df["low"]
    F = pd.DataFrame(index=df.index)
    r = c.pct_change()
    for k in (1, 2, 3, 5, 10):
        F[f"r{k}"] = c.pct_change(k)
    F["rz"] = (r - r.rolling(20).mean()) / r.rolling(20).std().replace(0, np.nan)
    rng = (h - l).replace(0, np.nan)
    body = c - o
    F["body_rng"] = body / rng
    F["uw"] = (h - np.maximum(o, c)) / rng
    F["lw"] = (np.minimum(o, c) - l) / rng
    ab = body.abs().rolling(10).mean().replace(0, np.nan)
    F["body_ab"] = body.abs() / ab
    for k in (1, 2, 3):
        F[f"col{k}"] = np.sign(body).shift(k - 1)
    d = c.diff()
    F["rsi14"] = 100 - 100 / (1 + wilder(d.clip(lower=0), 14) / wilder(-d.clip(upper=0), 14).replace(0, np.nan))
    F["rsi7"] = 100 - 100 / (1 + wilder(d.clip(lower=0), 7) / wilder(-d.clip(upper=0), 7).replace(0, np.nan))
    ll, hh = l.rolling(14).min(), h.rolling(14).max()
    F["stoch"] = 100 * (c - ll) / (hh - ll).replace(0, np.nan)
    ma20, sd20 = c.rolling(20).mean(), c.rolling(20).std().replace(0, np.nan)
    F["pctb"] = (c - (ma20 - 2 * sd20)) / (4 * sd20)
    F["bw"] = 4 * sd20 / ma20
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = wilder(tr, 14).replace(0, np.nan)
    F["atr_n"] = atr / c
    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    F["macdh"] = (macd - macd.ewm(span=9, adjust=False).mean()) / atr
    e20 = c.ewm(span=20, adjust=False).mean(); e50 = c.ewm(span=50, adjust=False).mean()
    F["d_e20"] = (c - e20) / atr
    F["d_e50"] = (c - e50) / atr
    F["dz"] = (e50 - e50.shift(15)) / atr
    F["dz5"] = (e20 - e20.shift(5)) / atr
    s = np.zeros(len(df)); dirs = np.sign(body.values)
    for i in range(1, len(df)):
        s[i] = s[i-1] + dirs[i] if dirs[i] == np.sign(s[i-1]) or s[i-1] == 0 else dirs[i]
    F["streak"] = s
    hi20, lo20 = h.rolling(20).max(), l.rolling(20).min()
    F["don_pos"] = (c - lo20) / (hi20 - lo20).replace(0, np.nan)
    hi55, lo55 = h.rolling(55).max(), l.rolling(55).min()
    F["don_pos55"] = (c - lo55) / (hi55 - lo55).replace(0, np.nan)
    F["rng_n"] = rng / atr
    mins = df.index.minute.values
    F["min_sin"] = np.sin(2 * np.pi * mins / 60)
    F["min_cos"] = np.cos(2 * np.pi * mins / 60)
    hrs = df.index.hour.values
    F["hr_sin"] = np.sin(2 * np.pi * hrs / 24)
    F["hr_cos"] = np.cos(2 * np.pi * hrs / 24)
    return F.replace([np.inf, -np.inf], np.nan)

def train_pair(df):
    F = features(df)
    c = df["close"]
    y_raw = np.sign(c.shift(-1) - c)             # next candle direction
    data = F.iloc[210:-1]; y = y_raw.iloc[210:-1]
    ok = (~data.isna().any(axis=1)) & (y != 0)
    data, y = data[ok], (y[ok] > 0).astype(int)
    n = len(data)
    if n < 1200: return None
    i1, i2 = int(n * 0.6), int(n * 0.8)
    Xtr, ytr = data.iloc[:i1], y.iloc[:i1]
    Xva, yva = data.iloc[i1:i2], y.iloc[i1:i2]
    Xte, yte = data.iloc[i2:], y.iloc[i2:]
    m = HistGradientBoostingClassifier(max_iter=250, max_depth=4, learning_rate=0.06,
                                       l2_regularization=1.0, min_samples_leaf=40,
                                       early_stopping=True, random_state=7)
    m.fit(Xtr, ytr)
    pva = m.predict_proba(Xva)[:, 1]
    best = None
    for thr in THR_GRID:                          # calibrate on validation
        su = pva >= thr; sd = pva <= 1 - thr
        nsig = su.sum() + sd.sum()
        if nsig < 25: continue
        prec = (yva[su].sum() + (1 - yva[sd]).sum()) / nsig
        if prec >= MIN_VAL_PREC:
            best = (float(thr), float(prec), int(nsig)); break
    if best is None: return None
    thr = best[0]
    pte = m.predict_proba(Xte)[:, 1]
    su = pte >= thr; sd = pte <= 1 - thr
    nte = su.sum() + sd.sum()
    te_prec = float((yte[su].sum() + (1 - yte[sd]).sum()) / nte) if nte else 0.0
    days_te = (data.index[-1] - data.index[i2]).total_seconds() / 86400
    ac1 = float(pd.Series(np.sign(c.diff())).iloc[210:].autocorr(lag=1) or 0)
    return dict(model=m, thr=thr, val_prec=best[1], val_n=best[2],
                test_prec=round(te_prec, 4), test_n=int(nte),
                sig_per_day=round(nte / max(days_te, 1e-9), 1),
                ac1=round(ac1, 3), cols=list(data.columns))

# ---------------- data fetch ----------------
async def page(api, sub, asset, t, collect=8.0):
    idx = random.randint(10_000_000, 99_999_999)
    await api.send_raw(f'42["loadHistoryPeriod",{{"asset":"{asset}","period":{PERIOD},"time":{t},"index":{idx},"offset":10800}}]')
    dl = time.time() + collect
    while time.time() < dl:
        try:
            raw = await asyncio.wait_for(sub.__anext__(), timeout=max(0.1, dl - time.time()))
        except (asyncio.TimeoutError, StopAsyncIteration):
            break
        if f'"index":{idx}' in raw:
            return json.loads(raw).get("data") or []
        await handle_frame(raw, live=False)
    return []

async def fetch_df(api, sub, asset):
    out = {}
    t = ((int(time.time()) + POFF) // 60) * 60
    for _ in range(48):
        data = await page(api, sub, asset, t)
        if not data: break
        oldest = None
        for d in data:
            ts = int(d["time"]) - POFF
            out[ts] = (float(d["open"]), float(d["high"]), float(d["low"]), float(d["close"]))
            oldest = ts if oldest is None else min(oldest, ts)
        if len(out) >= WANT: break
        t = oldest + POFF
    ts = sorted(out)
    return pd.DataFrame([out[k] for k in ts], columns=["open", "high", "low", "close"],
                        index=pd.to_datetime(ts, unit="s", utc=True))

# ---------------- live ----------------
def add_tick(asset, ts, price):
    m = int(ts // 60) * 60
    st = store[asset]
    if m in st:
        cd = st[m]
        cd[1] = max(cd[1], price); cd[2] = min(cd[2], price); cd[3] = price
    else:
        st[m] = [price, price, price, price]
    return m

def latest_price(asset):
    st = store[asset]
    return st[max(st)][3]

def eval_candidate(asset, upto_min, include_forming):
    st = store[asset]
    if include_forming:
        ts = [k for k in sorted(st) if k <= upto_min][-KEEP:]
    else:
        ts = [k for k in sorted(st) if k < upto_min][-KEEP:]
    if len(ts) < WARMUP: return None
    df = pd.DataFrame([st[k] for k in ts], columns=["open", "high", "low", "close"],
                      index=pd.to_datetime(ts, unit="s", utc=True))
    F = features(df)
    x = F.iloc[[-1]][STATS[asset]["cols"]]
    if x.isna().any(axis=1).iloc[0]: return None
    p = float(MODELS[asset].predict_proba(x)[0, 1])
    thr = THR[asset]
    if p >= thr: direc = 1
    elif p <= 1 - thr: direc = -1
    else: return None
    conf = max(p, 1 - p)
    return dict(asset=asset, direc=direc, prob=conf, minute=upto_min,
                dz=float(F["dz"].iloc[-1]), rank=(-conf,))

async def resolve_pending(asset, closed_upto):
    global pending, pause_until
    done, keep = [], []
    for p in pending:
        if p["asset"] == asset and p["entry_min"] < closed_upto:
            close = store[asset].get(p["entry_min"], [None] * 4)[3]
            if close is None: continue
            if close == p["entry"]: res = "T"
            elif (close > p["entry"]) == (p["dir"] == "BUY"): res = "W"
            else: res = "L"
            score[res] += 1
            ps = pair_score.setdefault(p["asset"], {"W": 0, "L": 0, "T": 0}); ps[res] += 1
            if res in "WL": recent.append(res)
            del recent[:-3]
            done.append((p, res, close))
        else:
            keep.append(p)
    pending = keep
    for p, res, close in done:
        tot = score["W"] + score["L"]
        acc = score["W"] / tot * 100 if tot else 0
        icon = {"W": "✅ WIN", "L": "❌ LOSS", "T": "➖ TIE"}[res]
        extra = ""
        if len(recent) == 3 and all(r == "L" for r in recent):
            pause_until = time.time() + COOLDOWN_S
            recent.clear()
            extra = f"\n🧊 3 straight losses — cool-down {COOLDOWN_S // 60} min"
        await tg(f"{icon} — #{p['no']} {p['asset']} {p['dir']} @1m (AI conf {p['prob']:.0%})\n"
                 f"entry {p['entry']:g} → close {close:g} ({close - p['entry']:+.6g})\n"
                 f"📈 SESSION: {score['W']}W–{score['L']}L–{score['T']}T ({acc:.0f}%)"
                 + (f"\n🔇 {p['asset']} muted" if muted(p['asset']) else "") + extra)
        log(f"RESULT {res} #{p['no']} {p['asset']} {p['dir']} | {score['W']}W-{score['L']}L")

async def flush_pre():
    global armed, sig_no
    await asyncio.sleep(3.0)
    cands = [c for c in pre["cands"] if not muted(c["asset"])]
    pre["cands"] = []; pre["task"] = None
    if not cands or armed is not None or time.time() < pause_until: return
    c = min(cands, key=lambda x: x["rank"])
    sig_no += 1
    trade_min = c["minute"] + 60
    armed = dict(no=sig_no, asset=c["asset"], direc=c["direc"], prob=c["prob"], trade_min=trade_min)
    d, e = ("BUY", "🟢") if c["direc"] > 0 else ("SELL", "🔴")
    secs = max(0, int(trade_min - time.time()))
    open_ist = datetime.fromtimestamp(trade_min, tz=timezone.utc).astimezone(IST)
    st = STATS[c["asset"]]
    cap = (f"🧠 AI EARLY #{sig_no} — GET READY ({secs}s)\n"
           f"{e} {d} — {c['asset']} | enter at candle open {open_ist:%H:%M:%S} IST\n"
           f"⏱ 1 MIN expiry | AI confidence {c['prob']:.0%} (thr {THR[c['asset']]:.0%})\n"
           f"📊 model test {st['test_prec']:.0%} (n={st['test_n']}) | drift dz={c['dz']:+.2f}\n"
           f"⚠️ WAIT for ✅GO / 🚫CANCEL at open")
    try:
        series = {k: tuple(v) for k, v in sorted(store[c["asset"]].items())[-100:]}
        png, _ = await asyncio.to_thread(render_chart, c["asset"], series, 92, 100)
    except Exception as ex:
        png = None; log(f"chart error: {ex}")
    if png: await tg_photo(png, cap)
    else: await tg(cap)
    log(f"AI EARLY #{sig_no} {d} {c['asset']} conf {c['prob']:.0%} in {secs}s")

async def confirm_or_cancel(asset, new_min):
    global armed, cancels
    a = armed
    if a is None or asset != a["asset"] or new_min < a["trade_min"]: return
    armed = None
    d = "BUY" if a["direc"] > 0 else "SELL"
    if new_min > a["trade_min"]:
        cancels += 1
        await tg(f"🚫 CANCEL #{a['no']} {a['asset']} — feed gap, skip")
        return
    cand = eval_candidate(asset, new_min, include_forming=False)
    if cand is not None and cand["direc"] == a["direc"]:
        entry = latest_price(asset)
        pending.append(dict(no=a["no"], asset=asset, dir=d, entry=entry,
                            entry_min=new_min, prob=a["prob"]))
        exp = datetime.fromtimestamp(new_min + 60, tz=timezone.utc).astimezone(IST)
        await tg(f"✅ GO #{a['no']} — ENTER NOW\n"
                 f"{'🟢' if d == 'BUY' else '🔴'} {d} {asset} @ {entry:g}\n"
                 f"⏱ 1 min — closes {exp:%H:%M:%S} IST | AI conf {a['prob']:.0%}")
        log(f"GO #{a['no']} {d} {asset} @ {entry:g}")
    else:
        cancels += 1
        await tg(f"🚫 CANCEL #{a['no']} {asset} {d} — AI no longer confident at open, skip")
        log(f"CANCEL #{a['no']} {asset}")

async def handle_frame(raw, live):
    s = raw if isinstance(raw, str) else str(raw)
    if s.startswith("[["):
        try: ticks = json.loads(s)
        except Exception: return
        for item in ticks:
            try:
                if not isinstance(item, (list, tuple)) or len(item) < 3 or item[0] not in store:
                    continue
                a, t, p = item[0], float(item[1]) - POFF, float(item[2])
            except (TypeError, ValueError):
                continue
            m = add_tick(a, t, p)
            prev = cur_min.get(a)
            if live and prev is not None and m > prev:
                cur_min[a] = m
                if len(store[a]) > KEEP + 200:
                    for k in sorted(store[a])[:-KEEP]: del store[a][k]
                await resolve_pending(a, m)
                await confirm_or_cancel(a, m)
            elif prev is None or m > prev:
                cur_min[a] = m
            if (live and a in MODELS and armed is None and time.time() >= pause_until
                    and (t - m) >= PRE_SEC and last_pre.get(a) != m):
                last_pre[a] = m
                try:
                    cand = eval_candidate(a, m, include_forming=True)
                except Exception as ex:
                    cand = None; log(f"{a} pre-eval error: {ex}")
                if cand is not None and not muted(a):
                    if pre["minute"] != m:
                        pre["minute"] = m; pre["cands"] = []
                    pre["cands"].append(cand)
                    if pre["task"] is None or pre["task"].done():
                        pre["task"] = asyncio.get_event_loop().create_task(flush_pre())
    elif s.startswith("{") and '"asset"' in s and ('"candles"' in s or '"history"' in s):
        try: payload = json.loads(s)
        except Exception: return
        a = payload.get("asset")
        if a in store:
            for arr in (payload.get("candles") or []):
                ts = int(arr[0]) - POFF
                store[a][int(ts // 60) * 60] = [float(arr[1]), float(arr[3]), float(arr[4]), float(arr[2])]
            for t, p in (payload.get("history") or []):
                add_tick(a, float(t) - POFF, float(p))

async def main():
    t0 = time.time()
    async with PocketOptionAsync(os.environ["POCKET_OPTION_SSID"]) as api:
        payouts = await api.payout()
        pairs = sorted(a for a, p in payouts.items() if p == 92 and is_forex_otc(a))
        log(f"AI v7: {len(pairs)} forex-OTC pairs @92% fetched from PO")
        sub = await api.subscribe_raw()
        for a in pairs: store[a] = {}
        lines = []; pooled = []
        for i, a in enumerate(pairs, 1):
            try:
                df = await fetch_df(api, sub, a)
                if len(df) < 1500: raise RuntimeError(f"only {len(df)} candles")
                res = await asyncio.to_thread(train_pair, df)
                for ts, r in zip(df.index.astype(np.int64) // 10**9, df.values):
                    store[a][int(ts // 60) * 60] = list(r)
                if res is None:
                    log(f"[{i}/{len(pairs)}] {a}: AI found no >=56% confidence band — SKIPPED (honest)")
                    lines.append(f"⛔ {a}: no reliable AI edge — not traded")
                    continue
                if res["test_prec"] < 0.53:      # val edge must SURVIVE on test, else don't trade it
                    log(f"[{i}/{len(pairs)}] {a}: val {res['val_prec']:.1%} but TEST only "
                        f"{res['test_prec']:.1%} — overfit, NOT traded")
                    lines.append(f"⛔ {a}: AI edge didn't survive test ({res['test_prec']:.0%}) — not traded")
                    continue
                MODELS[a] = res.pop("model"); THR[a] = res["thr"]; STATS[a] = res
                tend = "momentum" if res["ac1"] > 0.03 else "mean-revert" if res["ac1"] < -0.03 else "neutral"
                log(f"[{i}/{len(pairs)}] {a}: thr {res['thr']:.2f} | val {res['val_prec']:.1%} | "
                    f"TEST {res['test_prec']:.1%} (n={res['test_n']}) | {res['sig_per_day']}/day | "
                    f"ac1={res['ac1']:+.3f} ({tend})")
                lines.append(f"🧠 {a}: test {res['test_prec']:.0%} (n={res['test_n']}), "
                             f"{res['sig_per_day']:.0f}/day, {tend}")
                pooled.append(a)
            except Exception as ex:
                log(f"[{i}/{len(pairs)}] {a}: ERROR {ex}"); lines.append(f"❌ {a}: {ex}")
        # global feature importance (RandomForest on up to 3 pooled pairs)
        imp_txt = ""
        try:
            frames = []
            for a in pooled[:3]:
                dfa = pd.DataFrame([store[a][k] for k in sorted(store[a])],
                                   columns=["open", "high", "low", "close"],
                                   index=pd.to_datetime(sorted(store[a]), unit="s", utc=True))
                Fa = features(dfa); ya = np.sign(dfa["close"].shift(-1) - dfa["close"])
                Da, Ya = Fa.iloc[210:-1], ya.iloc[210:-1]
                ok = (~Da.isna().any(axis=1)) & (Ya != 0)
                frames.append((Da[ok], (Ya[ok] > 0).astype(int)))
            X = pd.concat([f[0] for f in frames]); Y = pd.concat([f[1] for f in frames])
            rf = RandomForestClassifier(n_estimators=150, max_depth=6, n_jobs=-1, random_state=7).fit(X, Y)
            top = sorted(zip(X.columns, rf.feature_importances_), key=lambda x: -x[1])[:8]
            imp_txt = "🔬 TOP AI FEATURES: " + ", ".join(f"{k}({v:.0%})" for k, v in top)
            log(imp_txt)
        except Exception as ex:
            log(f"importance error: {ex}")
        json.dump({"trained_at": datetime.now(IST).isoformat(),
                   "stats": {a: STATS[a] for a in STATS}},
                  open("/home/user/ai_model_stats.json", "w"), indent=1)
        await tg(f"🧠 AI ENGINE v7 — {datetime.now(IST):%d-%b %H:%M} IST\n"
                 f"Local ML (gradient boosting, ~40 features/pair), walk-forward 60/20/20,\n"
                 f"signals ONLY when AI probability ≥ calibrated threshold (val ≥56%)\n"
                 f"Pairs with a real AI edge: {len(MODELS)}/{len(pairs)} | trained {time.time() - t0:.0f}s\n"
                 f"{imp_txt}\n{'—' * 22}\n" + "\n".join(lines) +
                 f"\n{'—' * 22}\nEarly signal ~25s before open → ✅GO/🚫CANCEL at open. DEMO first.")
        for a in MODELS:
            await api.send_raw(f'42["changeSymbol",{{"asset":"{a}","period":60}}]')
        dl0 = time.time() + 4
        while time.time() < dl0:
            try:
                raw = await asyncio.wait_for(sub.__anext__(), timeout=0.5)
                await handle_frame(raw, live=False)
            except asyncio.TimeoutError:
                pass
        for a in MODELS:
            cur_min[a] = max(store[a]) if store[a] else None
        live_started = time.time()
        deadline = live_started + RUN_MINUTES * 60 if RUN_MINUTES > 0 else None
        next_board = time.time() + 1800
        log(f"LIVE — {len(MODELS)} AI pairs | early :{PRE_SEC + 3}s | GO/CANCEL at open")
        while True:
            if deadline and time.time() >= deadline: break
            try:
                raw = await asyncio.wait_for(sub.__anext__(), timeout=30)
            except asyncio.TimeoutError:
                continue
            await handle_frame(raw, live=True)
            if time.time() >= next_board:
                next_board = time.time() + 1800
                tot = score["W"] + score["L"]
                pb = "\n".join(f"• {a}: {s['W']}W–{s['L']}L{' 🔇' if muted(a) else ''}"
                               for a, s in pair_score.items())
                await tg(f"📊 AI SCOREBOARD ({(time.time() - live_started) / 60:.0f} min)\n"
                         f"{score['W']}W–{score['L']}L–{score['T']}T "
                         f"({score['W'] / tot * 100 if tot else 0:.0f}%) | {cancels} cancelled\n{pb}")
        tot = score["W"] + score["L"]
        await tg(f"🏁 AI RUN COMPLETE — {sig_no} signals, {cancels} cancelled\n"
                 f"{score['W']}W–{score['L']}L–{score['T']}T ({score['W'] / tot * 100 if tot else 0:.0f}% win)")
        log(f"RUN COMPLETE — {sig_no} signals, {score['W']}W-{score['L']}L")

if __name__ == "__main__":
    asyncio.run(main())
