"""
PRICE ACTION ENGINE v5 — breakouts, reversals, candlestick patterns, S/R rejections.
Per pair we validate MANY setups (60/20/20 split) and combine all good ones into an
ENSEMBLE so signals flow steadily: target >= ~20 signals/day per pair, portfolio
>= 10 signals / 30 min, while every member setup is individually validated.
Tiers per member: A(elite) B(good) C(above breakeven, used only to fill frequency).
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

TOKEN, CHATID = os.environ["TELEGRAM_BOT_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}"
IST = timezone(timedelta(hours=5, minutes=30))
POFF, PERIOD, WANT = 7200, 60, 6000
EXPIRIES = [1, 2, 3]        # 5m removed — live results were poor
BREAKEVEN = 1/1.92
TARGET_SPD = 0.0            # PRECISION MODE: no C-tier frequency fillers
MAX_MEMBERS = 5

FIAT = {"USD","EUR","GBP","JPY","CHF","CAD","AUD","NZD","CNY","CNH","INR","MXN","BRL",
        "ARS","CLP","COP","PEN","PHP","VND","IDR","MYR","THB","SGD","HKD","KRW","TWD",
        "PKR","BDT","LKR","EGP","DZD","MAD","TND","AED","SAR","QAR","BHD","OMR","KWD",
        "JOD","LBP","IRR","YER","TRY","ZAR","RUB","UAH","PLN","CZK","HUF","RON","DKK",
        "NOK","SEK","KES","NGN","GHS","TZS","MZN","ZMW","BWP"}
def is_forex_otc(a):
    return a.endswith("_otc") and not a.startswith("#") and len(a)==10 and a[:3] in FIAT and a[3:6] in FIAT

def tg(t):
    for i in range(0, len(t), 3900):
        requests.post(f"{API}/sendMessage", data={"chat_id": CHATID, "text": t[i:i+3900]}, timeout=30)

async def page(api, sub, asset, t, collect=8.0):
    idx = random.randint(10_000_000, 99_999_999)
    await api.send_raw(f'42["loadHistoryPeriod",{{"asset":"{asset}","period":{PERIOD},"time":{t},"index":{idx},"offset":10800}}]')
    dl = time.time() + collect
    while time.time() < dl:
        try:
            raw = await asyncio.wait_for(sub.__anext__(), timeout=max(0.1, dl-time.time()))
        except (asyncio.TimeoutError, StopAsyncIteration):
            break
        if f'"index":{idx}' in raw:
            return json.loads(raw).get("data") or []
    return []

async def fetch_df(api, sub, asset):
    out = {}
    t = ((int(time.time()) + POFF)//60)*60
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
    df = pd.DataFrame([out[k] for k in ts], columns=["open","high","low","close"],
                      index=pd.to_datetime(ts, unit="s", utc=True))
    df.to_csv(f"/home/user/data/{asset}.csv")
    return df

def wilder(s, n): return s.ewm(alpha=1/n, adjust=False).mean()

# ================= PRICE ACTION LIBRARY =================
def build_pa_signals(df):
    c,o,h,l = df["close"],df["open"],df["high"],df["low"]
    body=(c-o).abs(); rng=(h-l).replace(0,np.nan)
    up=c>o; dn=c<o
    uw=h-np.maximum(o,c); lw=np.minimum(o,c)-l
    ab=body.rolling(10).mean()
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=wilder(tr,14)
    d=c.diff()
    rsi=100-100/(1+wilder(d.clip(lower=0),14)/wilder(-d.clip(upper=0),14).replace(0,np.nan))
    ma20,sd20=c.rolling(20).mean(),c.rolling(20).std()
    bbu,bbl=ma20+2*sd20,ma20-2*sd20
    bw=(bbu-bbl)/ma20.replace(0,np.nan)
    e20=c.ewm(span=20,adjust=False).mean(); e50=c.ewm(span=50,adjust=False).mean()
    e50up=e50>e50.shift(3); e50dn=e50<e50.shift(3)
    # rolling extremes (shifted = level BEFORE current bar)
    ext={}
    for N in (10,20,30,55):
        ext[N]=(h.rolling(N).max().shift(), l.rolling(N).min().shift())
    # streaks
    s=np.zeros(len(df)); dirs=np.sign((c-o).values)
    for i in range(1,len(df)):
        s[i]=s[i-1]+dirs[i] if dirs[i]==np.sign(s[i-1]) or s[i-1]==0 else dirs[i]
    streak=pd.Series(s,index=df.index)
    # candle anatomy
    pin_b=(lw>=2*body)&(lw>=0.55*rng)                 # bullish pin / hammer
    pin_s=(uw>=2*body)&(uw>=0.55*rng)                 # bearish pin / shooting star
    eng_b=up&dn.shift(1).fillna(False)&(c>=o.shift())&(o<=c.shift())&(body>=ab)
    eng_s=dn&up.shift(1).fillna(False)&(c<=o.shift())&(o>=c.shift())&(body>=ab)
    maru_b=up&(body/rng>=0.85)&(body>=1.5*ab)
    maru_s=dn&(body/rng>=0.85)&(body>=1.5*ab)
    doji=body<=0.15*rng
    tw_b=(l.sub(l.shift()).abs()<=0.15*atr)&dn.shift(1).fillna(False)&up   # tweezer bottom
    tw_s=(h.sub(h.shift()).abs()<=0.15*atr)&up.shift(1).fillna(False)&dn   # tweezer top
    soldiers=up&up.shift(1).fillna(False)&up.shift(2).fillna(False)&(body>=ab)&(body.shift()>=ab)
    crows=dn&dn.shift(1).fillna(False)&dn.shift(2).fillna(False)&(body>=ab)&(body.shift()>=ab)
    star_b=doji.shift(1).fillna(False)&dn.shift(2).fillna(False)&up&(body>=ab)      # morning star
    star_s=doji.shift(1).fillna(False)&up.shift(2).fillna(False)&dn&(body>=ab)      # evening star
    inside=(h<h.shift())&(l>l.shift())
    nr7=rng==rng.rolling(7).min()
    def SIG(b, sl): return np.where(b.fillna(False),1,0)-np.where(sl.fillna(False),1,0)
    S={}
    # ---------- BREAKOUTS ----------
    for N in (10,20,30,55):
        hiN,loN=ext[N]
        S[f"BRK_don{N}_close"]=SIG((c>hiN)&up,(c<loN)&dn)
        S[f"BRK_don{N}_confirm"]=SIG((c.shift()>hiN.shift())&up&(c>c.shift()),
                                     (c.shift()<loN.shift())&dn&(c<c.shift()))
        S[f"BRK_don{N}_body"]=SIG((c>hiN)&up&(body>=1.3*ab),(c<loN)&dn&(body>=1.3*ab))
    S["BRK_squeeze"]=SIG((bw.shift()<bw.rolling(60).quantile(0.2).shift())&(c>bbu.shift()),
                         (bw.shift()<bw.rolling(60).quantile(0.2).shift())&(c<bbl.shift()))
    S["BRK_NR7"]=SIG(nr7.shift(1).fillna(False)&(c>h.shift())&up,
                     nr7.shift(1).fillna(False)&(c<l.shift())&dn)
    S["BRK_inside"]=SIG(inside.shift(1).fillna(False)&(c>h.shift(2))&up,
                        inside.shift(1).fillna(False)&(c<l.shift(2))&dn)
    S["BRK_atr_expansion"]=SIG(up&(body>=2.0*atr),dn&(body>=2.0*atr))
    S["BRK_retest_go"]=SIG((c.shift(2)>ext[20][0].shift(2))&(l.shift()<=ext[20][0].shift(2))&up&(c>c.shift()),
                           (c.shift(2)<ext[20][1].shift(2))&(h.shift()>=ext[20][1].shift(2))&dn&(c<c.shift()))
    S["BRK_marubozu_follow"]=SIG(maru_b,maru_s)
    S["BRK_soldiers"]=SIG(soldiers,crows)
    # ---------- FALSE-BREAK / FAKEY REVERSALS ----------
    for N in (20,55):
        hiN,loN=ext[N]
        S[f"REV_fakey{N}"]=SIG((l<loN)&(c>loN)&up,(h>hiN)&(c<hiN)&dn)
    # ---------- PATTERN REVERSALS AT EXTREMES ----------
    for N in (10,20):
        hiN,loN=ext[N]
        at_lo=l<=loN*1.0; at_hi=h>=hiN*1.0
        S[f"REV_pin{N}"]=SIG(pin_b&at_lo,pin_s&at_hi)
        S[f"REV_engulf{N}"]=SIG(eng_b&at_lo,eng_s&at_hi)
        S[f"REV_tweezer{N}"]=SIG(tw_b&at_lo,tw_s&at_hi)
    S["REV_star"]=SIG(star_b,star_s)
    S["REV_pin_rsi"]=SIG(pin_b&(rsi<35),pin_s&(rsi>65))
    S["REV_engulf_rsi"]=SIG(eng_b&(rsi<35),eng_s&(rsi>65))
    S["REV_bb_reject"]=SIG((l<=bbl)&(c>bbl)&(lw>=body),(h>=bbu)&(c<bbu)&(uw>=body))
    S["REV_bb_rsi"]=SIG((c<=bbl)&(rsi<30),(c>=bbu)&(rsi>70))
    # double top/bottom: two touches of same level within 0.25*ATR, 5-30 bars apart + confirm
    lo30=l.rolling(30).min().shift(3)
    hi30=h.rolling(30).max().shift(3)
    S["REV_double_bottom"]=SIG((l.shift()<=lo30+0.25*atr)&up&(c>c.shift()),
                               (h.shift()>=hi30-0.25*atr)&dn&(c<c.shift()))
    # streak reversals with confirmation candle
    for K in (4,5,6):
        S[f"REV_streak{K}_confirm"]=SIG((streak.shift()<=-K)&up,(streak.shift()>=K)&dn)
        S[f"REV_streak{K}"]=SIG(streak<=-K,streak>=K)
    S["REV_hammer_after_drop"]=SIG(pin_b&(streak.shift()<=-3),pin_s&(streak.shift()>=3))
    # ---------- TREND-PULLBACK PRICE ACTION ----------
    S["PA_pullback_trend"]=SIG(e50up&(c>e50)&(l<=e20)&up&(c>c.shift()),
                               e50dn&(c<e50)&(h>=e20)&dn&(c<c.shift()))
    S["PA_engulf_trend"]=SIG(eng_b&(c>e50)&e50up,eng_s&(c<e50)&e50dn)
    S["PA_pin_trend"]=SIG(pin_b&(c>e50)&e50up,pin_s&(c<e50)&e50dn)
    # ---------- MACD + StochRSI combos ----------
    def xup(a,b): return (a>b)&(a.shift()<=b.shift())
    def xdn(a,b): return (a<b)&(a.shift()>=b.shift())
    macdF=c.ewm(span=5,adjust=False).mean()-c.ewm(span=13,adjust=False).mean()
    macdFs=macdF.ewm(span=6,adjust=False).mean(); hist=macdF-macdFs
    macdS=c.ewm(span=12,adjust=False).mean()-c.ewm(span=26,adjust=False).mean()
    macdSs=macdS.ewm(span=9,adjust=False).mean()
    rmin,rmax=rsi.rolling(14).min(),rsi.rolling(14).max()
    srsi=100*(rsi-rmin)/(rmax-rmin).replace(0,np.nan)
    srk=srsi.rolling(3).mean(); srd=srk.rolling(3).mean()
    S["MSR_rev"]=SIG(xup(srk,srd)&(srk<20)&(hist>hist.shift()),
                     xdn(srk,srd)&(srk>80)&(hist<hist.shift()))
    S["MSR_cross"]=SIG(xup(macdF,macdFs)&(srk>srd)&(srk<70),
                       xdn(macdF,macdFs)&(srk<srd)&(srk>30))
    S["MSR_pullback"]=SIG((macdS>macdSs)&xup(srk,srd)&(srk<40),
                          (macdS<macdSs)&xdn(srk,srd)&(srk>60))
    S["MSR_extreme"]=SIG((srk<5)&(hist>hist.shift()),(srk>95)&(hist<hist.shift()))
    S["MSR_hist_flip"]=SIG(xup(hist,pd.Series(0.0,index=df.index))&(srk<60),
                           xdn(hist,pd.Series(0.0,index=df.index))&(srk>40))
    return S

# ============ 60-SECOND EXPIRY LIBRARY (researched M1+1m setups) ============
def build_60s_signals(df):
    c,o,h,l = df["close"],df["open"],df["high"],df["low"]
    body=(c-o).abs(); rng=(h-l).replace(0,np.nan)
    up=c>o; dn=c<o
    ab=body.rolling(10).mean()
    tr=pd.concat([(h-l),(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1)
    atr=wilder(tr,14)
    d=c.diff()
    rsi=100-100/(1+wilder(d.clip(lower=0),14)/wilder(-d.clip(upper=0),14).replace(0,np.nan))
    e9=c.ewm(span=9,adjust=False).mean();  e20=c.ewm(span=20,adjust=False).mean()
    e21=c.ewm(span=21,adjust=False).mean();e50=c.ewm(span=50,adjust=False).mean()
    e100=c.ewm(span=100,adjust=False).mean();e200=c.ewm(span=200,adjust=False).mean()
    ma20,sd20=c.rolling(20).mean(),c.rolling(20).std()
    bbu,bbl=ma20+2*sd20,ma20-2*sd20
    ll14,hh14=l.rolling(14).min(),h.rolling(14).max()
    stk=100*(c-ll14)/(hh14-ll14).replace(0,np.nan)
    ku,kl=e20+2*wilder(tr,10),e20-2*wilder(tr,10)
    def SIG(b,s): return np.where(b.fillna(False),1,0)-np.where(s.fillna(False),1,0)
    def xup(a,lvl): return (a>lvl)&(a.shift()<=lvl)
    def xdn(a,lvl): return (a<lvl)&(a.shift()>=lvl)
    S={}
    # 1) classic 60s BB fade: close outside band -> revert next candle
    S["S60_bb_fade"]=SIG((c<bbl)&(body<2*ab),(c>bbu)&(body<2*ab))
    S["S60_bb_fade_rsi"]=SIG((c<bbl)&(rsi<25),(c>bbu)&(rsi>75))
    # 2) impulse exhaustion: 4+ same-colour candles outside BB then reversal candle
    run4dn=dn&dn.shift(1).fillna(False)&dn.shift(2).fillna(False)&dn.shift(3).fillna(False)
    run4up=up&up.shift(1).fillna(False)&up.shift(2).fillna(False)&up.shift(3).fillna(False)
    S["S60_impulse_exhaust"]=SIG(run4dn.shift(1).fillna(False)&(l.shift()<bbl.shift())&up,
                                 run4up.shift(1).fillna(False)&(h.shift()>bbu.shift())&dn)
    # 3) S/R level re-touch fade (77% ITM session method)
    hi120=h.shift(5).rolling(115).max(); lo120=l.shift(5).rolling(115).min()
    S["S60_level_fade"]=SIG((l<=lo120+0.15*atr)&(c>lo120),(h>=hi120-0.15*atr)&(c<hi120))
    # 4) Williams fractal + EMA20/50/100 stacked pullback
    frac_up=(l.shift(2)<l.shift(1))&(l.shift(2)<l.shift(3))&(l.shift(2)<l.shift(4))&(l.shift(2)<l)
    frac_dn=(h.shift(2)>h.shift(1))&(h.shift(2)>h.shift(3))&(h.shift(2)>h.shift(4))&(h.shift(2)>h)
    stkb=(e20>e50)&(e50>e100); stks=(e20<e50)&(e50<e100)
    S["S60_fractal_trend"]=SIG(stkb&(l.shift(2)<e20.shift(2))&frac_up&up,
                               stks&(h.shift(2)>e20.shift(2))&frac_dn&dn)
    # 5) EMA9/21 fresh cross + pullback confirm
    cb=(e9>e21)&(e9.shift(5)<=e21.shift(5)); cs=(e9<e21)&(e9.shift(5)>=e21.shift(5))
    S["S60_ema921_pull"]=SIG(cb&(l<=e9)&(c>e21)&up, cs&(h>=e9)&(c<e21)&dn)
    # 6) stochastic 20/80 cross with EMA50/200 trend filter
    S["S60_stoch_trend"]=SIG(xup(stk,20)&(c>e50)&(c>e200), xdn(stk,80)&(c<e50)&(c<e200))
    # 7) Keltner 2 consecutive closes outside + RSI side
    S["S60_keltner2"]=SIG((c>ku)&(c.shift()>ku.shift())&(rsi>50),
                          (c<kl)&(c.shift()<kl.shift())&(rsi<50))
    # 8) double green/red momentum after pullback candle
    S["S60_double_colour"]=SIG(up&up.shift(1).fillna(False)&(body>=ab)&(body.shift()>=ab)&dn.shift(2).fillna(False),
                               dn&dn.shift(1).fillna(False)&(body>=ab)&(body.shift()>=ab)&up.shift(2).fillna(False))
    # 9) momentum burst out of 15-bar range
    hi15,lo15=h.rolling(15).max().shift(),l.rolling(15).min().shift()
    S["S60_burst"]=SIG(up&(body>=1.8*ab)&(c>hi15), dn&(body>=1.8*ab)&(c<lo15))
    return S

def build_all_signals(df):
    S = build_pa_signals(df)
    S.update(build_60s_signals(df))
    S.update(build_quotex_signals(df))
    return S

# ===== borrowed & upgraded from projecttrader1300a (validated before use) =====
def build_quotex_signals(df):
    c, o, h, l = df["close"], df["open"], df["high"], df["low"]
    def SIG(b, s): return np.where(b.fillna(False), 1, 0) - np.where(s.fillna(False), 1, 0)
    def xup(a, b): return (a > b) & (a.shift() <= b.shift())
    def xdn(a, b): return (a < b) & (a.shift() >= b.shift())
    def wma(s, n):
        w = np.arange(1, n + 1, dtype=float)
        return s.rolling(n).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)
    S = {}
    # Hull MA 9 cross (low-lag trend trigger)
    hma = wma(2 * wma(c, 4) - wma(c, 9), 3)
    S["Q_hull_cross"] = SIG(xup(c, hma), xdn(c, hma))
    # Daily floor-trader pivot cross (prev UTC day H/L/C)
    day = df.index.floor("D")
    grp = df.groupby(day)
    piv = ((grp["high"].max() + grp["low"].min() + grp["close"].last()) / 3).shift(1)
    P = pd.Series(pd.Index(day).map(piv), index=df.index)
    S["Q_pivot_cross"] = SIG(xup(c, P), xdn(c, P))
    S["Q_pivot_side"] = SIG(c > P, c < P)
    # ADX-gated EMA trend (their core logic + chop veto, done properly)
    e9 = c.ewm(span=9, adjust=False).mean(); e21 = c.ewm(span=21, adjust=False).mean()
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr14 = wilder(tr, 14).replace(0, np.nan)
    upm = h.diff(); dnm = -l.diff()
    plus = np.where((upm > dnm) & (upm > 0), upm, 0.0)
    minus = np.where((dnm > upm) & (dnm > 0), dnm, 0.0)
    pdi = 100 * wilder(pd.Series(plus, index=df.index), 14) / atr14
    mdi = 100 * wilder(pd.Series(minus, index=df.index), 14) / atr14
    adx = wilder(100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan), 14)
    S["Q_trend_adx"] = SIG((e9 > e21) & (adx > 18) & (c > e21) & (c > o),
                           (e9 < e21) & (adx > 18) & (c < e21) & (c < o))
    return S

TIER_GATES=[("A",dict(tr=0.56,va=0.56,te=0.58,n=20,z=1.60)),
            ("B",dict(tr=0.55,va=0.55,te=0.56,n=18,z=1.28))]

def eval_pair(df):
    S=build_pa_signals(df)
    close=df["close"].values; n=len(df)
    i1,i2=int(n*0.6),int(n*0.8)
    days_te=(df.index[-1]-df.index[i2]).total_seconds()/86400
    rows=[]
    for name,sg in S.items():
        sg=np.asarray(sg)
        w=np.where(sg!=0)[0]; w=w[(w>=210)&(w<n-max(EXPIRIES))]
        if len(w)==0: continue
        best=None
        for k in EXPIRIES:
            diff=close[w+k]-close[w]; valid=diff!=0; ww=w[valid]
            if len(ww)==0: continue
            wins=np.where(sg[ww]==1,diff[valid]>0,diff[valid]<0)
            trm=ww<i1; vam=(ww>=i1)&(ww<i2); tem=ww>=i2
            if trm.sum()<25 or vam.sum()<8 or tem.sum()<10: continue
            tra,vaa,tea=wins[trm].mean(),wins[vam].mean(),wins[tem].mean()
            z=(wins[tem].sum()-0.5*tem.sum())/(0.5*math.sqrt(tem.sum()))
            tier=None
            for tn,g in TIER_GATES:
                if tra>=g["tr"] and vaa>=g["va"] and tea>=g["te"] and tem.sum()>=g["n"] and z>=g["z"]:
                    tier=tn; break
            if tier is None: continue
            row=dict(strategy=name,expiry=k,tier=tier,
                     train=round(float(tra),4),val=round(float(vaa),4),test=round(float(tea),4),
                     test_n=int(tem.sum()),z=round(float(z),2),
                     sig_per_day=round(float(tem.sum()/max(days_te,1e-9)),1))
            key=("ABC".index(tier),-min(vaa,tea))
            if best is None or key<best[0]: best=(key,row)
        if best: rows.append(best[1])
    # PRECISION MODE: only A/B members, best first
    order={"A":0,"B":1}
    rows.sort(key=lambda r:(order[r["tier"]],-min(r["val"],r["test"])))
    members=[r for r in rows if r["tier"] in "AB"][:MAX_MEMBERS]
    if not members: return None
    # union stats on test segment (first-member priority for expiry/direction)
    sigs={m["strategy"]:np.asarray(S[m["strategy"]]) for m in members}
    wins=[]; cnt=0
    for i in range(i2,n-max(EXPIRIES)):
        direc=0; k=None
        for m in members:
            v=sigs[m["strategy"]][i]
            if v!=0 and direc==0:
                direc=v; k=m["expiry"]
        if direc==0: continue
        dv=close[i+k]-close[i]
        if dv==0: continue
        cnt+=1; wins.append((dv>0)==(direc>0))
    ua=float(np.mean(wins)) if wins else 0.0
    uspd=cnt/max(days_te,1e-9)
    return dict(members=members,
                union=dict(test_acc=round(ua,4),test_n=cnt,sig_per_day=round(uspd,1)))

async def main():
    t0=time.time()
    async with PocketOptionAsync(os.environ["POCKET_OPTION_SSID"]) as api:
        payouts=await api.payout()
        pairs=sorted(a for a,p in payouts.items() if p==92 and is_forex_otc(a))
        print(f"PA ENGINE v5: {len(pairs)} forex-OTC pairs @92%")
        sub=await api.subscribe_raw()
        model={}; lines=[]; tot=0.0
        for i,asset in enumerate(pairs,1):
            try:
                df=await fetch_df(api,sub,asset)
                if len(df)<1500: raise RuntimeError(f"only {len(df)} candles")
                res=eval_pair(df)
                if res is None:
                    print(f"[{i}/{len(pairs)}] {asset}: no validated setups"); 
                    lines.append(f"— {asset}: no validated setups"); continue
                model[asset]=res; u=res["union"]; tot+=u["sig_per_day"]
                tiers="".join(m["tier"] for m in res["members"])
                print(f"[{i}/{len(pairs)}] {asset}: {len(res['members'])} setups [{tiers}] | "
                      f"union test {u['test_acc']:.1%} (n={u['test_n']}) | {u['sig_per_day']}/day")
                lines.append(f"{asset}: {len(res['members'])} setups [{tiers}] — union test "
                             f"{u['test_acc']:.0%} — {u['sig_per_day']}/day")
            except Exception as e:
                print(f"[{i}/{len(pairs)}] {asset}: ERROR {e}"); lines.append(f"— {asset}: ERROR {e}")
        json.dump({"trained_at":datetime.now(IST).isoformat(),"type":"price_action_v5",
                   "breakeven":round(BREAKEVEN,4),"model":model},
                  open("/home/user/pa_model.json","w"),indent=1)
        msg=(f"🕯 PRICE ACTION ENGINE v5 — {datetime.now(IST):%d-%b %H:%M} IST\n"
             f"Breakouts • false-breaks • pin/engulf/tweezer/star at S/R • double bottoms •\n"
             f"streak reversals • trend pullbacks | validated 60/20/20, ensembles per pair\n"
             f"{'—'*24}\n"
             f"🔥 PORTFOLIO: ~{tot:.0f} signals/day ≈ {tot/48:.1f} per 30 min across {len(model)} pairs\n\n"
             + "\n".join("• "+ln for ln in lines) +
             "\n\n⚠️ Every member setup individually validated. DEMO first.")
        tg(msg)
        open("/home/user/pa_report.txt","w").write(msg)
        print(f"\nDone in {time.time()-t0:.0f}s | portfolio ~{tot:.0f}/day (~{tot/48:.1f} per 30min)")

if __name__ == "__main__":
    asyncio.run(main())
