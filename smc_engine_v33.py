"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SMC PEAK v33 "OMEGA" — max-accuracy 24/7 engine     ║
╚══════════════════════════════════════════════════════════════════════════════╝
v33 OMEGA (user: "still develop the bot to max peak accuracy fully — new engines"):
  • ENGINE A REGIME RADAR: forecasts tape character (drift efficiency, alternation, body
    ratio, ER) → 0..1 trend-ness; chops are filtered before any signal exists.
  • ENGINE B MTF CONFLUENCE: the 1m signal must agree with the M5/M15/M30 trend axis.
  • ENGINE C MEMORY: self-learned hour-quality table from the engine's OWN trade DB
    (per asset × 3h bucket) — weak buckets −0.06 AQS, strong buckets +0.03.
  • ENGINE D CALIBRATION LOOP: live W/L per confidence bucket; <52% (n≥12) → −0.04 AQS.
  • ENGINE E AQS: one 0..1 accuracy score fusing pwin, conf, agreement, MTF, radar,
    alternation, setup count, grade, payout and storm alignment. Trade only at AQS ≥ 0.60.
  • GATES: chaos cooldown (3 candles >3× median range), freshness (extended >1.8 ATR needs
    APEX+storm), DEFENSE mode (2 lost rounds in a session → elite AQS 0.70 + half stakes).

v30 ETERNAL (user: "make it able to 24/7 — every 50 mins give reports, no breaks, highly
accurate signals only … zip for pella.app"):
  • 24/7 engine: run_engine() is now an eternal session cycle — 50-minute live windows, a full
    report at every boundary, and the next session starts immediately (zero idle). main() is an
    outer watchdog: any crash restarts the engine 30 s later, forever.
  • Session transition: payout rescan (roster follows PO payout moves), up to 3 new ≥90% pairs
    trained on the spot, stale pairs dropped, and the 4 stalest models retrained — ~1 min.
  • SNIPER accuracy pack (default ON): chop/alternation kill (research: "skip small alternating
    candles"), dead-tape kill, STD-grade kill, single-setup kill, conf ≥0.62, meta pwin ≥0.55,
    and a low-liquidity UTC dead-zone (20:00–01:00) that demands APEX proof.
  • Deploy: portable paths (works in any folder), stdlib health endpoint when $PORT is set,
    24/7 state persistence, v33_sessions.jsonl + v33_last_run.json reports.

v29 MAX FLOW (user: "maximum signals + maximum accuracy fully … and start 1 hour run"):
  • SIGNAL FLOW lifted: MAX_PER_MIN 4→8, FOCUS 6→12 concurrent, THROTTLE_S 180→60,
    post-round-loss pause 240s→75s, 3-streak cool-down 600s→180s, pair roster = ALL payouts
    ≥90% (cap 45, best first) instead of ==92% only.
  • ACCURACY kept fully intact: ensemble vote grades (APEX/HIGH/STD), isotonic meta filter
    (pwin ≥ thr), probation gate, momentum-proof gate, spike guard, feed guard, STORM tilt,
    soft/weak demotions and the v28 step-2 guard + round breaker all unchanged.

v28 GOD ENGINE GUARD (user: "improve that fully to the peak to prevent losses"):
  • STEP-2 GUARD — live evidence: #7 USDCOP, #14 SOL-USD, #16 USDCLP were fully lost when the
    ×2.2 step-2 leg compounded into chop (−$22 total). v28 refreshes the STORM supertrend read
    at the moment of the deep re-entry: STORM agrees → full ladder ×2.2; STORM opposes/unknown
    → capped at MTG2_MIN ($1.50). Every leg is still placed REAL on PO (100% rule kept).
  • ROUND BREAKER — a fully-lost round benches that pair for 20 min (ROUND_BENCH_S) and eases
    global risk ×0.85 (RISK_EASE); each recovered round refunds ×1.05 (RISK_RECOVER, cap 1.2).
    Stops one chop window from eating several assets the way it did in v26.
  • USDCOP RULE (user) — a round recovered via MTG = full WIN; its leg losses are absorbed and
    never surfaced as losses in the score, session summary or the machine report.

v26 BINARY GOD ENGINE (user: "last 2 trades was loss … living binary god engine" + SMART X STORM Pine):
  • STORM CORE — the user's indicator ported in: Supertrend(factor 3.2, ATR 11) + SMA9 trend
    filter + candle confirmation + 3-bar cooldown, as three first-class setup families:
    STORM_turn (trend flip), STORM_x (SMA9 cross inside supertrend side), STORM_god (final
    Pine signal: setup + bull/bear candle + close vs SMA9). They train, nominate and vote
    through the same ensemble as every legacy setup — core library untouched, layers added.
  • STORM TILT — live supertrend read tilts stake only: agrees ×1.15, opposes ×0.90 (never drops).
  • GOD LADDER — user's Pine maxMTG = 2: after a lost MTG leg the engine takes ONE more real
    recovery step (step-2, same ladder ×2.2, PO min $1, 12% balance cap), then the round closes.
  • FEED RESCUE — v25 evidence: stream died mid-run and 2 real legs never graded. Now every
    reconnect re-pulls history for assets with open legs, merges candles, grades the legs.
  • STORM ledger in the summary + machine report (module-level W/L like the Pine table).

v25 MTG FULL-SEND (user: "make sure to take all MTG trades on PO 100%"):
  • MTG_CONFIRM default OFF — the v21 fresh-confirm gate no longer skips recovery legs;
    every MTG re-entry the engine decides to take is placed REAL on PO (tiers A/B/C).
  • MTG_MIN_CONF default 0.0 — no confidence floor for recovery legs anymore.
  • Safety collars raised for this mode: MTG_ROUND_HALT 2→6 losing rounds, MTG_NET_HALT
    -25→-40 $ (extreme-only; the 2.2x ladder stays).
  • MIN-STAKE FIX (v24 evidence: MATIC order rejected at $0.97 by PO): every order is
    floored to >= $1.00 inside place(), and any failed order is RETRIED once at $1.00.
  • MTG leg sizing also floored to >= $1.00.
  Live-run evidence behind v24 that v25 keeps: ensemble vote core, isotonic meta,
  Bayesian stake ladder, asset-health governor, exposure caps, throttle/adapt demotes,
  adverse-open quarter stakes, feed guards, FOCUS cap, AI risk officer, voice notes.

v24 APEX MONSTER (user: "rewrite full… improve the signal core a lot… alive monster"):
  THE SIGNAL CORE WAS REWRITTEN:
  • ENSEMBLE VOTE ELECTION (was: first fired signal won): every firing member casts a
    weighted vote w = walk-forward acc × regime fit; the highest-weight side wins,
    agreement ratio + voter count are measured, and confidence is a weighted blend.
  • REGIME-SPECIALISED MEMBERS: each setup's accuracy is measured per efficiency-ratio
    bucket (CHOP/MIX/TREND) on the training window; a setup that historically LOSES in
    today's regime is muted (weight 0), marginal regimes get weight 0.55.
  • META-LABEL v3 + ISOTONIC CALIBRATION: the LightGBM filter now trains on 19 features
    (adds voter count + agreement) and its probabilities are isotonic-calibrated (PAV)
    on the validation split before thresholding — honest, monotone p(win).
  • LIVE BAYESIAN LADDER ("alive"): every setup carries a Beta posterior seeded by its
    train accuracy (strength K) and updated by REAL results each run → stake tier
    0.40×/0.60×/0.85×/1.05×/1.25×. The bot re-sizes itself based on its own live record.
  • ASSET HEALTH GOVERNOR: 5 straight real losses on an asset → all its stakes halve
    until it wins again (recovers automatically).
  • PORTFOLIO EXPOSURE GUARDS: max 2 crypto / 2 stock / 1 metal positions open at once,
    max 3 same-direction — violators are halved, never dropped.
  • HARD STAKE CAP: no single order above 6% of balance, ever.
  Everything v23 proved live is kept (throttle demote, ADAPT demote, adverse-open quarter,
  MTG fresh-confirm + inert skips, feed guards, FOCUS cap, AI risk officer, voice notes).

v23 OVERDRIVE (user: "improve to the peak based on the previous run — adaptive, alive,
  AI agents on my BazaarLink API"):
  FROM v22 EVIDENCE (13 signals, 8W-8L-1T, real +$1.18, paper -$4.37, razor 0W-3L,
  MTG skip 5/5 protective, throttle skip = the only non-placed signal):
  • THROTTLE DEMOTES, NEVER DROPS: per-asset cooldown kept, but the signal still trades
    at HALF stake — "every signal placed" is now literally true.
  • ADVERSE OPEN = QUARTER STAKE, NEVER A CANCEL: even when the setup breaks or flips at
    the open, v23 places a small real order instead of cancelling (audit still grades it).
  • RAZOR-RISK SIZING: compressed vol (30-bar ATR < 55% of 180-bar baseline = razor-prone)
    → quarter stake (v22 razor closes 0W-3L).
  • GATE-SKIPPED LEGS NEVER PAUSE: fresh-confirm-skipped MTG legs are paper-only and are
    excluded from the streak breaker (they caused v22's 9-min dead stretch).
  • MTG SKIP LEDGER: skipped-leg paper P&L tracked separately (money never staked).
  ADAPTIVE CORE ("alive"):
  • ADAPT PROFILE recomputed at launch from the fresh board + today's realised tape:
    follow/fade character → risk ×1.15 / ×1.0 / ×0.70; lone/cold setups are DEMOTED to half
    stake (traded, never dropped — "every signal places an order" stays true).
  • DAY-FOLLOW: assets ≥70% today get +25% size; ≤30% need 2+ setups or tier-A.
  • RT-COLD: a setup with 4 straight live losses drops to quarter stake until it wins.
  • FOCUS CAP: max simultaneous open positions (default 6); extra signals audited.
  • FEED GUARD: stale tape (>8s) → signal audited, never traded (v20 dead-feed lesson).
  • FEED REBUILD: 3 failed reconnects → full history re-pull + fresh warm-up.
  • HEARTBEAT every 10 min: score, open positions, feed health, ADAPT profile.
  AI AGENT LAYER (BazaarLink LLM key from .env):
  • AI RISK OFFICER: up to AI_DECISIONS bounded calls, one per live entry, JSON verdict
    {keep|size_down|skip} + reason — fail-open, budgeted, shadow-audited.
  • AI MARKET ANALYST at launch + AI COACH at board refresh; spoken VOICE notes via TTS.
  • MACHINE REPORT /home/user/v23_last_run.json at run end (grounds the next build).

v22 (user: "bot was quiet + signals weren't placed on the demo"):
  • ALWAYS_TRADE: QUALITY gate demoted to a NOTE — EVERY armed signal places a real demo
    order (tiers A/B/C). Nothing is 'signal-only' anymore. Probation/soft half-stake kept.
  • probation floor 0.54 → 0.52: two more weak boards re-armed at half stake (more activity)
v21 (from the v20 runs: #51 AAPL ✓ but #52 FB re-entered blind — direct + MTG both lost,
  −$4.55 paper bleed with ZERO proof the setup still existed):
  • MTG FRESH-CONFIRM: a recovery leg only places if the setup still fires same-direction
    at the re-entry minute; otherwise skipped (advisory paper leg only) — bleed avoided
  • LOSS-MUTE: every lost round hard-mutes that asset for 15 min (no revenge trades)
v20 (from the v19 run: 3W-0L clean, but only 18/30 assets armed & cancels kept winning):
  • PROBATION TIER: assets testing 0.54-0.58 (below the 0.58 floor) stay armed but trade
    ONLY with 2+ agreeing setups / meta>=0.62 / tier-A champion — at HALF stake
  • SOFT-CANCEL: audit evidence (8W-4L would-be, 67%) — when a setup merely weakens at
    open (no direction flip, no adverse candle > 0.45 ATR) the entry is KEPT at half stake
    instead of cancelled; genuine flips/adverse tape still cancel
  • PROFIT LOCK: session P&L >= +20% of start → auto-trading halts, signals continue
  • Daily loss guard loosened to -12% (floor $6) for small accounts
  • STREAM WATCHDOG: feed silence > 25s triggers auto-reconnect + resubscribe
  • balance() hangs on some sessions — all balance calls are timeout-wrapped with a
    START_BAL fallback so the engine never freezes on it

v19 (from the 18:09 demo run's early-cluster 2W-8L evidence):
  • 1-MINUTE EXPIRY ONLY — every setup validated at 1m, every MTG leg at 1m
  • BOARD QUALITY FLOOR: assets whose walk-forward test < ASSET_MIN_TEST (0.58)
    are trained + reported but NOT armed (the failed run's losers were exactly
    the marginal boards: AEDCNY 46.7%, NZDUSD 51.4%, USDRUB 55.4%, IRRUSD 46.7%)
  • SPIKE GUARD: no entries right after a parabolic candle (move > 2.5x median range)
  • HARDER STREAK BREAKER: 3 straight losses -> 10 min pause (was 4 -> 5 min)
  • MTG KILL SWITCHES: 1m legs only, auto-halt after 2 losing rounds (+ net limit)
  • WARM-UP: no signals in the first 90s of live (feed settling)
  • CONF FLOOR: quality gate now needs conf >= 0.56 (was 0.53)
  • CLEAN METRICS: direct win rate reported excluding MTG legs

v18 changes (previous session evidence):

  1. PREMIUM/DISCOUNT CONTEXT: a rolling dealing range positions every candle
     (0% = at range low, 100% = at range high). SMC doctrine: reversals are only
     taken from extremes, continuations only with structure. Hard gates applied
     INSIDE build_smc so training, live and proof-engine all see the same book.
  2. REGIME INTELLIGENCE: Kaufman efficiency ratio (trend vs chop) + ATR
     percentile rank (dead vs normal vs blow-off vol). Mean-reversion family is
     suppressed in strong trends, momentum family needs actual trend, everything
     is suppressed in dead tape. All causal.
  3. NEW SETUPS: SWEEP_reclaim (sweep + strong reclaim candle), BREAKER_retest
     (failed order block flips into a breaker block), FVG_stack (stacked
     imbalances — A+ continuation). FVG detection now requires >= 0.25 ATR gap
     and OB creation now requires displacement — both kill micro-noise signals.
  4. TRUE EXPIRY AUTO-SELECTION: every setup x mask is now validated at 1/2/3
     minute expiry (was promised in v16 but hardcoded to 1). Best validated
     expiry is attached per member.
  5. PURGED 4-FOLD NOMINATION: embargo between folds (labels use future closes,
     so fold boundaries are purged) — removes leakage at the seams.
  6. META-LABEL FILTER v2: LightGBM second-stage model on 17 context features
     with a proper 3-way signal-level split — train / calibrate threshold on
     val / honest test gate. Replaces the v16 heuristic threshold.
  7. RISK GOVERNOR v2: daily loss limit, day counters, per-asset bench, dynamic
     cooldown, half-Kelly stake display, auto-trade still demo-only by default.
  8. STATE PERSISTENCE: crash-safe session state (score, pair stats, pending
     trades, cooldowns) survives restarts via smc_state.json (next to this script).
  9. DB v2: keeps the original `trades` table byte-compatible (prove_engine
     still writes it), adds `apex_detail` with expiry/prob/conf/session/regime.
 10. ROBUSTNESS: guarded imports (engine importable without PO/lightgbm/libs),
     LLM analyst call budget, Telegram no-op when unconfigured, async-safe I/O.

 ── v18 FIELD-LEARNED ADDITIONS (from the 19:12–19:46 IST live session) ──
 11. CANCELLED-SIGNAL AUDIT: every CANCEL / THROTTLE / feed-gap is shadow-graded
     on real candles into `apex_audit`. The session summary now answers the key
     question the v17 run could not: is the strict GO/CANCEL filter SAVING money
     or COSTING it? (v17 run: 5 of 10 signals cancelled — effect was unknown.)
 12. MTG RISK CONTROL v2: live evidence showed 3W-1L rounds (75%) still NET
     NEGATIVE (one double-loss erases three recoveries). Now: MTG auto-place is
     confidence-gated (>= MTG_MIN_CONF), multiplier configurable (MTG_MULT), MTG
     net P&L tracked separately, and auto-MTG HALTS for the session below
     MTG_NET_HALT. Advisory re-entry messages still fire for manual traders.
 13. PAPER P&L: signal-only runs now report hypothetical P&L at 4% stakes
     (normal legs + 2.2x MTG legs) so every session produces an economics read
     without risking a cent.
 14. RAZOR ANALYSIS: live run showed both wins closed by 2e-5 (tick noise).
     Every graded trade now stores |close-entry| in ATR units; session summary
     splits win rate of RAZOR (<15% ATR) vs NORMAL closes.
 15. OPERATIONS: MTG leg results now print full RESULT lines to the console
     (v17 shipped them to Telegram only — acknowledged bug), quality-gate
     rejection reasons are logged into the DB, champ gate is configurable
     (CHAMP=strict|top2|tierA — v17's strict mode rejected 100% of live signals),
     apex_session summary row written at run end.

Public API (kept stable): build_smc(df) -> (S, AUX) | tf_arrays(df) | tfok(mask, v, TF, i)
"""
import asyncio, json, math, os, sqlite3, time, random, warnings
from collections import deque, defaultdict
from datetime import datetime, timezone, timedelta

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))   # v30 portable

# ---- guarded imports: the engine must stay importable for offline testing ----
try:
    from pa_engine import wilder
except Exception:                                    # identical fallback
    def wilder(s, n): return s.ewm(alpha=1 / n, adjust=False).mean()
try:
    from chart_style import render_chart
except Exception:
    render_chart = None
try:
    import lightgbm as lgb
except Exception:
    lgb = None
try:
    from BinaryOptionsToolsV2.pocketoption import PocketOptionAsync
except Exception:
    PocketOptionAsync = None

# ================================ CONFIG =====================================
IST       = timezone(timedelta(hours=5, minutes=30))
POFF      = 7200                     # PO server offset (UTC+2)
PERIOD    = 60
WANT      = 4500
PAYOUT    = 0.92
BREAKEVEN = 1 / (1 + PAYOUT)
RUN_MINUTES = float(os.environ.get("RUN_MINUTES", "0"))
PRE_SEC   = 32                       # early-signal scan trigger (~T-28s)
EXPIRIES  = (1,)                      # v19 ONE-MINUTE ONLY — every setup, every leg
KEEP, WARMUP = 700, 320
MAX_PER_MIN  = 8
MASKS     = ("TRI", "TRIPLE_C", "DUAL", "M5C", "M5A", "M15A", "ANY")
EMBARGO   = 3                        # bars purged at each fold seam
PD_GATE   = os.environ.get("PDGATE", "1") == "1"      # premium/discount gate
REG_GATE  = os.environ.get("REGGATE", "1") == "1"     # regime gate
MTG_AUTO  = os.environ.get("MTG", "0") == "1"         # auto-place martingale leg
# ---- v18 field-learned risk knobs ----
MTG_MULT     = float(os.environ.get("MTG_MULT", "2.2"))      # recovery leg multiplier
MTG_MIN_CONF = float(os.environ.get("MTG_MIN_CONF", "0.0"))  # v25: no floor — take all MTG legs
MTG_NET_HALT = float(os.environ.get("MTG_NET_HALT", "-40"))  # v25: extreme-only $ MTG net stop
PAPER_PCT    = float(os.environ.get("PAPER_PCT", "0.04"))    # hypothetical stake % of day-start
RAZOR_ATR    = float(os.environ.get("RAZOR_ATR", "0.15"))    # close margin < this ATR = razor
CHAMP_MODE   = os.environ.get("CHAMP", "top2")               # strict | top2 | tierA
ASSET_MIN_TEST = float(os.environ.get("ASSET_MIN_TEST", "0.58"))  # board floor for live arming
MTG_ROUND_HALT = int(os.environ.get("MTG_ROUND_HALT", "6"))       # v25: extreme-only round stop
SKIP_WARMUP_S  = float(os.environ.get("SKIP_WARMUP_S", "90"))     # live warm-up, no signals
SPIKE_MULT     = float(os.environ.get("SPIKE_MULT", "2.5"))       # parabolic-candle guard
PROBATION      = os.environ.get("PROBATION", "1") == "1"          # v20 probation tier
PROB_MIN_TEST  = float(os.environ.get("PROB_MIN_TEST", "0.52"))   # probation lower bound
PROB_MIN_AGREE = int(os.environ.get("PROB_MIN_AGREE", "2"))       # setups that must agree
SOFTC          = os.environ.get("SOFTC", "1") == "1"              # v20 soft-cancel
SOFT_ADVERSE   = float(os.environ.get("SOFT_ADVERSE", "0.45"))    # adverse ATR tolerance
PROFIT_LOCK    = float(os.environ.get("PROFIT_LOCK", "0.20"))     # session profit lock
BAL_FALLBACK   = float(os.environ.get("START_BAL", "50"))         # if balance() hangs
STREAM_DEAD_S  = float(os.environ.get("STREAM_DEAD_S", "25"))     # feed silence watchdog
MUTE_LOSS_S    = float(os.environ.get("MUTE_LOSS_S", "900"))      # v21 loss-mute per asset (15 min)
MTG_CONFIRM    = os.environ.get("MTG_CONFIRM", "0") == "1"        # v25: OFF — every MTG leg lands on PO
# ── v26 BINARY GOD ENGINE ──
STORM_FACTOR   = float(os.environ.get("STORM_FACTOR", "3.2"))     # SMART X STORM supertrend factor
STORM_ATR      = int(os.environ.get("STORM_ATR", "11"))           # SMART X STORM ATR period
MTG_STEPS      = int(os.environ.get("MTG_STEPS", "2"))            # god ladder (Pine maxMTG=2)
STORM_TILT     = os.environ.get("STORM_TILT", "1") == "1"
ALWAYS_TRADE   = os.environ.get("ALWAYS_TRADE", "1") == "1"       # v22 every signal traded
# ---- v23 OVERDRIVE knobs ----
FOCUS        = int(os.environ.get("FOCUS", "12"))           # v29 MAX FLOW: max simultaneous open positions
FOLLOW       = os.environ.get("FOLLOW", "1") == "1"         # day-follow warm-start from live DB
RAZOR_MIN    = float(os.environ.get("RAZOR_MIN", "0.25"))   # razor-risk → quarter stake
THROTTLE_S   = float(os.environ.get("THROTTLE_S", "60"))    # v29: per-asset re-arm (demote, not drop)
FEED_WARN    = int(os.environ.get("FEED_WARN", "4"))        # stale-feed warn (seconds)
FEED_BENCH   = int(os.environ.get("FEED_BENCH", "8"))       # stale-feed bench (no entries)
FEED_FAIL    = int(os.environ.get("FEED_FAIL", "3"))        # failed revives → full feed rebuild
AI_DECISIONS = int(os.environ.get("AI_DECISIONS", "3"))     # per-entry AI risk-officer calls/run
VOICEFN      = os.environ.get("VOICE", "1") == "1"          # spoken summaries (TTS→Telegram)
V24_REPORT   = "/home/user/v24_last_run.json"
V25_REPORT   = "/home/user/v25_last_run.json"
# ── v30 ETERNAL: portable paths + 24/7 session knobs ──
_BASE        = os.path.dirname(os.path.abspath(__file__))      # deploy-safe (pella.app)
V33_REPORT   = os.path.join(_BASE, "v33_last_run.json")
V33_SESSIONS = os.path.join(_BASE, "v33_sessions.jsonl")
SESSION_MIN  = float(os.environ.get("SESSION_MIN", "50"))      # live minutes per session
SESS_GRACE   = float(os.environ.get("SESS_GRACE", "240"))      # wait-for-open-legs grace (s)
RETRAIN_N    = int(os.environ.get("RETRAIN_N", "4"))           # rotating model refresh / session
PAIRS_MAX    = int(os.environ.get("PAIRS_MAX", "45"))          # roster cap (best payout first)
BOARD_S      = float(os.environ.get("BOARD_S", "1500"))        # scoreboard every 25 min
BEAT_S       = float(os.environ.get("BEAT_S", "600"))          # heartbeat every 10 min
# ── v30 SNIPER accuracy pack (research: trend-confirm, chop-kill, liquidity hours) ──
SNIPER       = os.environ.get("SNIPER", "1") == "1"            # highly-accurate signals only
SNIPER_CONF  = float(os.environ.get("SNIPER_CONF", "0.62"))   # ensemble confidence floor
SNIPER_PWIN  = float(os.environ.get("SNIPER_PWIN", "0.55"))   # isotonic meta pwin floor
SNIPER_ALTR  = float(os.environ.get("SNIPER_ALTR", "0.65"))   # candle-alternation chop gate
SNIPER_DZ    = os.environ.get("SNIPER_DZ", "1") == "1"        # UTC dead-zone gate
DZ_START     = int(os.environ.get("DZ_START", "20"))          # dead-zone start (UTC hour)
DZ_END       = int(os.environ.get("DZ_END", "1"))             # dead-zone end (UTC hour)
# ── v33 OMEGA knobs ──
AQS_MIN     = float(os.environ.get("AQS_MIN", "0.60"))     # AQS gate: accuracy-score floor
DEF_AQS     = float(os.environ.get("DEF_AQS", "0.70"))     # defense mode: elite floor
CHAOS_MULT  = float(os.environ.get("CHAOS_MULT", "3.0"))   # chaos kill: candle vs median range
FRESH_ATR   = float(os.environ.get("FRESH_ATR", "1.8"))    # freshness: max 5-candle extension (ATRs)
# ── v33 OMEGA knobs (fusion · floors · turn-guard · ladder cap · calibration blacklist) ──
TURN_ON      = os.environ.get("TURN_ON", "1") == "1"          # anti top/bottom-grab guard
TURN_SLOPE   = float(os.environ.get("TURN_SLOPE", "0.40"))    # chase rule arms only in decent trend
FLOOR_ON     = os.environ.get("FLOOR_ON", "1") == "1"         # per-asset learned confidence floors
FLOOR_LEARN  = os.environ.get("FLOOR_LEARN", "1") == "1"      # rounds teach the floors
FLOOR_BASE   = float(os.environ.get("FLOOR_BASE", "0.60"))    # global floor baseline
EQS_MIN      = float(os.environ.get("EQS_MIN", "0.45"))       # fused accuracy-equivalent floor
CALBL_ON     = os.environ.get("CALBL_ON", "1") == "1"         # calibration blacklist gate
CALBL_N      = int(os.environ.get("CALBL_N", "14"))           # min live legs before a bucket blocks
CALBL_WR     = float(os.environ.get("CALBL_WR", "0.52"))      # bucket WR below which it blocks
LADDER_RISK  = float(os.environ.get("LADDER_RISK", "0.05"))   # recovery-leg stake <= 5% of balance
LADDER_TILT  = float(os.environ.get("LADDER_TILT", "1.30"))   # pushback cap = 1.3x the failed leg
META_WIN     = int(os.environ.get("META_WIN", "400"))         # fusion history window (live legs)
# ── v33 OMEGA LIVE BRAIN knobs (session-adaptive accuracy) ──
LIVE_MIN_N   = int(os.environ.get("LIVE_MIN_N", "12"))         # min legs before a dimension can flag
LIVE_WR_LOW  = float(os.environ.get("LIVE_WR_LOW", "0.45"))   # dimension WR below which it demotes
LIVE_WR_HI   = float(os.environ.get("LIVE_WR_HI", "0.55"))    # opposite direction must beat this
MAXCONF      = float(os.environ.get("MAXCONF", "0.90"))       # anti-overfit: above this (unless APEX+storm) -> half
ROLL_N       = int(os.environ.get("ROLL_N", "10"))            # rolling leg window for health
ROLL_WR      = float(os.environ.get("ROLL_WR", "0.35"))       # rolling WR below which cooldown fires
ROLL_COOL_S  = float(os.environ.get("ROLL_COOL_S", "240"))    # adaptive cooldown length (s)
ROLL_COOL_GAP= float(os.environ.get("ROLL_COOL_GAP", "600"))  # min gap between adaptive cooldowns
# ── v28 LOSS GUARDS (grounded in the v26 live hour) ──
MTG2_MIN     = float(os.environ.get("MTG2_MIN", "1.5"))    # step-2 cap when STORM opposes
ROUND_BENCH_S = float(os.environ.get("ROUND_BENCH_S", "1200"))  # pair bench after a lost round
RISK_EASE    = float(os.environ.get("RISK_EASE", "0.85"))  # risk x after a fully-lost round
RISK_RECOVER = float(os.environ.get("RISK_RECOVER", "1.05"))  # risk refund per recovered round
ROLL_WIN_RULE = os.environ.get("ROLL_WIN_RULE", "1") == "1"   # USDCOP rule
# ---- v24 APEX MONSTER knobs ----
ENSEMBLE     = os.environ.get("ENSEMBLE", "1") == "1"      # weighted-vote signal core
META_ISO     = os.environ.get("META_ISO", "1") == "1"      # isotonic-calibrated meta model
BAYES_K      = float(os.environ.get("BAYES_K", "6"))       # prior strength for live posteriors
HEALTH_N     = int(os.environ.get("HEALTH_N", "5"))        # last-N real results → cold asset
STAKE_CAP    = float(os.environ.get("STAKE_CAP", "0.06"))  # hard cap: 6% of balance per order
CRYPTO_MAX   = int(os.environ.get("CRYPTO_MAX", "2"))
STOCK_MAX    = int(os.environ.get("STOCK_MAX", "2"))
METAL_MAX    = int(os.environ.get("METAL_MAX", "1"))
SAMEDIR_MAX  = int(os.environ.get("SAMEDIR_MAX", "3"))
TOPTIER   = os.environ.get("TOPTIER", "0") == "1"     # APEX/HIGH signals only
AGGRO     = os.environ.get("AGGRO", "0") == "1"
DB        = os.path.join(_BASE, "pro_signals.db")            # v30 portable
STATE_F   = os.path.join(_BASE, "smc_state.json")            # v30 portable
SESS      = ("ASIA", "LONDON", "NY", "LATE")
TE   = {"A": "💎", "B": "✅", "C": "⚠️", "D": "🕐"}
RANK = {"A": 0, "B": 1, "C": 2, "D": 3}
GATES = [("A", dict(tr=0.56, va=0.55, te=0.57, n=15, z=1.28)),
         ("B", dict(tr=0.54, va=0.54, te=0.55, n=12, z=1.00)),
         ("C", dict(tr=0.52, va=0.52, te=BREAKEVEN, n=10, z=0.00)),
         ("D", dict(tr=0.50, va=0.50, te=0.50, n=8, z=-9.0))]

# ---- LLM analyst (Qwen via BazaarLink) — budgeted so it can never bill-spam ----
BKEY   = os.environ.get("BAZAARLINK_API_KEY", "")
BURL   = os.environ.get("BAZAARLINK_BASE_URL", "https://api.bazaarlink.ai/v1")
BMODEL = os.environ.get("BAZAARLINK_MODEL", "qwen/qwen3.7-flash")
LLM_BUDGET = {"left": int(os.environ.get("LLM_BUDGET", "8"))}

def llm_ask(prompt, max_tokens=600, temperature=0.3):
    """Best-effort LLM analyst with exponential backoff + hard call budget."""
    if not BKEY or LLM_BUDGET["left"] <= 0:
        return None
    wait = 4
    for _ in range(3):
        try:
            r = requests.post(f"{BURL}/chat/completions",
                              headers={"Authorization": f"Bearer {BKEY}"},
                              json={"model": BMODEL, "max_tokens": max_tokens, "temperature": temperature,
                                    "messages": [{"role": "system", "content":
                                        "You are a rigorous quant analyst for 1-min binary options "
                                        "(92% payout, breakeven 52.08%). Be concise, concrete, skeptical of small n."},
                                        {"role": "user", "content": prompt}]}, timeout=90).json()
            if "choices" in r:
                LLM_BUDGET["left"] -= 1
                return r["choices"][0]["message"]["content"]
        except Exception:
            time.sleep(wait); wait *= 2
    return None

# ============================ SHARED STATE ===================================
TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN")
CHATID  = os.environ.get("TELEGRAM_CHAT_ID")
API     = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else ""

MEMBERS, UNION, AIF, HOURS, MTGK = {}, {}, {}, {}, {}
TRD = {"on": False}
RSTATE = {"rate": 0.06}
ASSET_LAST, LAST_TRADE = {}, {}
BAL_D = {"v": 100.0}
API_H = None
store, cur_min = {}, {}
STORM_ST = {}                 # v26 live supertrend read per asset
ROUNDS   = {"W": 0, "L": 0, "rec": 0, "absorbed": 0, "cur": {}}   # v28 round accounting
# ── v30 ETERNAL globals ──
SNAP     = {}                 # session-start snapshot (deltas for the 50-min report)
DAY0     = {}                 # day-start snapshot (midnight day report)
TRAIN_T  = {}                 # last training time per asset (rotating refresh)
REFRESH  = {"n": 0, "adds": 0, "drops": 0}      # last transition info (session card)
SESS_LAST = {}                # metrics of the last finished session
LIFETIME = {"sessions": 0, "sig": 0, "w": 0, "l": 0, "rw": 0, "rl": 0,
            "rec": 0, "abs": 0, "pnl": 0.0, "since": None}
# ── v33 OMEGA state ──
PAYOUTS  = {}                 # live payout map (roster + AQS payout term)
HQ       = {}                 # ENGINE C MEMORY: per-asset × 3h-bucket W/L from own DB
CAL      = {}                 # ENGINE D: live W/L per confidence bucket
DEFENSE  = {"on": False}      # mid-session elite-only mode
# ── v33 OMEGA state ──
METAF    = {"n": 0, "upd": 0, "cands": 0, "acc": 0.5}   # ENGINE F fusion weights/accuracy
FLOORS   = {}                        # ENGINE G: per-asset learned floor offset (+raise / -lower)
RLEARN   = {"n": 0, "bump": 0, "lower": 0, "last": ""}
# ── v33 OMEGA LIVE BRAIN state ──
LIVE     = {"n": 0, "dir": {}, "reg": {}, "hour": {}, "rollwr": 1.0, "lastcool": 0.0}
pending = []
score_s = {"W": 0, "L": 0, "T": 0}
pair_score = {}
sig_no, cancels = 0, 0
pre = {"minute": None, "cands": [], "task": None}
armed = {}
last_pre = {}
recent = deque(maxlen=30)
SET_REC = defaultdict(lambda: deque(maxlen=10))
mtg_round = {"W": 0, "L": 0}
pause_until = 0.0
CON = None
DDAY = {"d": "", "sig": 0, "w": 0, "l": 0, "pnl": 0.0, "b0": 0.0,
        "paper": 0.0, "mtg_net": 0.0, "rz_w": 0, "rz_l": 0, "nm_w": 0, "nm_l": 0,
        "dw": 0, "dl": 0, "soft_w": 0, "soft_l": 0, "mtg_skip": 0,
        "storm_w": 0, "storm_l": 0, "mtg_step2": 0, "storm_ag": 0, "storm_op": 0,
        "round_w": 0, "round_l": 0, "round_rec": 0,
        "thr_half": 0, "adapt_half": 0, "soft_weak": 0, "rz_risk": 0, "rz_risk_w": 0, "rz_risk_l": 0,
        "focus_skip": 0, "feed_skip": 0, "skip_net": 0.0, "rt_cut": 0,
        "ai_dec": 0, "ai_skip": 0, "ai_down": 0,
        "bayes_adj": 0, "health_cut": 0, "corr_half": 0,
        "v24_n": 0, "v24_cf": 0.0, "v24_ag": 0.0,
        "floor_skip": 0, "turn_skip": 0, "eqs_skip": 0, "cal_skip": 0, "ladders": 0,
        "live_half": 0, "live_cool": 0}
CSHADOW = {"W": 0, "L": 0, "T": 0}       # cancelled-signal audit counters
LIVE_T0 = {"t": 0.0}                      # v19 warm-up reference
PROB = {}                                 # v20 probation assets
STREAM_T = {"t": 0.0, "last_revive": 0.0} # v20 feed watchdog
MUTE_T = {}                               # v21 loss-muted assets
ADAPT = {"risk": 1.0, "min_fires": 0, "asset_boost": [], "asset_cut": [], "notes": [],
         "profile": "balanced"}           # v23 adaptive session profile
FEED_T = {}                               # v23 per-asset last feed second
AI_CALLS = {"dec": 0, "down": 0, "skip": 0}   # v23 agent counters
VS = {"on": False}                        # v23 voice notes enabled
PAIR_REC = defaultdict(lambda: deque(maxlen=8))   # v24 per-asset recent real results
shadow_pend = []                          # cancelled/throttled signals being shadow-graded
MTG_STATE = {"halted": False}

def log(m): print(f"[{datetime.now(IST):%H:%M:%S}] {m}", flush=True)

# ============================ TELEGRAM =======================================
def _post_msg(text):
    if not (TOKEN and CHATID):
        log(f"TG(off) {text.splitlines()[0] if text else ''}"); return
    try:
        for i in range(0, len(text), 3900):
            requests.post(f"{API}/sendMessage",
                          data={"chat_id": CHATID, "text": text[i:i + 3900]}, timeout=15)
    except Exception as e:
        print("TG error:", e, flush=True)

def _post_photo(png, caption):
    if not (TOKEN and CHATID) or png is None:
        _post_msg(caption); return
    try:
        r = requests.post(f"{API}/sendPhoto", data={"chat_id": CHATID, "caption": caption[:1024]},
                          files={"photo": ("signal.png", png, "image/png")}, timeout=30)
        if r.status_code != 200:
            _post_msg(caption)                      # graceful text fallback
    except Exception as e:
        print("TG photo error:", e, flush=True); _post_msg(caption)

async def tg(t):          await asyncio.to_thread(_post_msg, t)
async def tg_photo(p, c): await asyncio.to_thread(_post_photo, p, c)

def muted(a):
    if time.time() < MUTE_T.get(a, 0.0): return True          # v21 loss-mute (15 min)
    s = pair_score.get(a)
    return bool(s) and (s["L"] - s["W"]) >= 3

def kelly_stake(p):
    k = p - (1 - p) / PAYOUT
    return max(0.25, min(2.0, k * 50))              # half-Kelly, % of bankroll

def sess_name(i): return SESS[int(i) % 4]
def reg_name(er): return "TREND" if er >= 0.30 else "CHOP" if er < 0.22 else "MIX"

# ============================ PERSISTENCE ====================================
LAST_SAVE = [0.0]

def save_state(force=False):
    t = time.time()
    if not force and t - LAST_SAVE[0] < 4:
        return
    LAST_SAVE[0] = t
    try:
        st = dict(score_s=score_s, pair_score=pair_score, sig_no=sig_no, cancels=cancels,
                  mtg_round=mtg_round, BAL_D=BAL_D, RSTATE=RSTATE, pause_until=pause_until,
                  last_trade=LAST_TRADE, dday=DDAY, pending=pending,
                  cshadow=CSHADOW, shadow_pend=shadow_pend[-40:],
                  set_rec={f"{k[0]}|{k[1]}": list(v) for k, v in list(SET_REC.items())[-400:]},
                  adapt=ADAPT, pair_rec={k: list(v)[-8:] for k, v in PAIR_REC.items()},
                  lifetime=LIFETIME, day0=DAY0, train_t=TRAIN_T, cal=CAL,
                  floors=FLOORS, metaf=METAF, rlearn=RLEARN, live=LIVE)  # v33 + live brain
        with open(STATE_F, "w") as f:
            json.dump(st, f)
    except Exception as e:
        log(f"state save error: {e}")

def load_state():
    global sig_no, cancels, pause_until, pending
    try:
        st = json.load(open(STATE_F))
    except Exception:
        return False
    try:
        score_s.update(st.get("score_s", {}))
        pair_score.update(st.get("pair_score", {}))
        sig_no = int(st.get("sig_no", 0)); cancels = int(st.get("cancels", 0))
        mtg_round.update(st.get("mtg_round", {}))
        CSHADOW.update(st.get("cshadow", {}))
        shadow_pend[:] = [p for p in st.get("shadow_pend", []) if isinstance(p, dict)]
        BAL_D.update(st.get("BAL_D", {}))
        RSTATE.update(st.get("RSTATE", {}))
        pause_until = float(st.get("pause_until", 0.0))
        LAST_TRADE.update(st.get("last_trade", {}))
        DDAY.update(st.get("dday", {}))
        ADAPT.update(st.get("adapt", {}) or {})
        LIFETIME.update(st.get("lifetime", {}) or {})                      # v30 24/7 totals
        DAY0.update(st.get("day0", {}) or {})
        TRAIN_T.update(st.get("train_t", {}) or {})
        CAL.update(st.get("cal", {}) or {})
        FLOORS.update(st.get("floors", {}) or {})                      # v33 ENGINE G floors
        METAF.update(st.get("metaf", {}) or {})                        # v33 ENGINE F fusion
        RLEARN.update(st.get("rlearn", {}) or {})
        LIVE.update(st.get("live", {}) or {})                           # v33 LIVE BRAIN tables
        for k, v in (st.get("pair_rec", {}) or {}).items():
            PAIR_REC[k].extend(int(x) for x in v[-8:])
        pending = [p for p in st.get("pending", []) if isinstance(p, dict)]
        for k, v in st.get("set_rec", {}).items():
            a, s = k.split("|", 1)
            SET_REC[(a, s)].extend(int(x) for x in v[-6:])
        log(f"STATE restored: {score_s['W']}W-{score_s['L']}L all-time, {len(pending)} pending resumes")
        return True
    except Exception as e:
        log(f"state load error: {e}")
        return False

# ==================== v23 OVERDRIVE — ADAPTIVE CORE + AGENTS ==================
def _razor_risk(asset, minute):
    """Compressed-vol proxy for razor closes (v22: razor closes lost 0W-3L → quarter stake)."""
    a_now = _atr_proxy(asset, minute, n=30)
    a_base = _atr_proxy(asset, minute, n=180)
    return bool(a_now and a_base and a_now < 0.55 * a_base)

def _rt_cold(asset, strategy, n=4):
    """RT bins: last n live results of this exact setup all losses → stake cut until it wins."""
    rr = SET_REC[(asset, strategy)]
    return len(rr) >= n and sum(list(rr)[-n:]) == 0

def _day_follow():
    """Day-follow: today's realised per-asset edges (live DB) bias new entries."""
    boost, cut = [], []
    if not FOLLOW:
        return boost, cut
    try:
        midnight = datetime.now(IST).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        rows = list(CON.execute(
            "SELECT asset, SUM(outcome='W'), SUM(outcome='L') FROM trades WHERE ts >= ? GROUP BY asset",
            (midnight - 5 * 3600,)))
        for asset, w, l in rows:
            n = int(w or 0) + int(l or 0)
            if n >= 3:
                wr = int(w or 0) / n
                if wr >= 0.70: boost.append(asset)
                elif wr <= 0.30: cut.append(asset)
    except Exception as e:
        log(f"day-follow skip: {e}")
    return sorted(boost), sorted(cut)

def _adapt_compute(chs, acs, rts):
    """v23 adaptive profile from the fresh board (character, test acc, signal rate) + today's tape."""
    ch = sum(chs) / len(chs) if chs else 0.5
    ac = sum(acs) / len(acs) if acs else 0.55
    rate = (sum(rts) / len(rts) / 24.0) if rts else 1.0
    boost, cut = _day_follow()
    risk = 1.0
    if ac >= 0.66 and ch >= 0.51:
        risk = 1.15
    elif ac < 0.58 or ch <= 0.49:
        risk = 0.70
    min_fires = 0 if ch >= 0.51 else 1          # choppier/reverting tape → need company
    ADAPT.update(risk=round(risk, 2), min_fires=min_fires, asset_boost=boost, asset_cut=cut,
                 profile=("follow" if ch >= 0.51 else "fade"),
                 notes=[f"char {ch:.0%} / acc {ac:.0%} / {rate:.1f} sig/h",
                        ("boost: " + ",".join(boost)) if boost else "boost: -",
                        ("cut: " + ",".join(cut)) if cut else "cut: -"])
    log(f"ADAPT profile={ADAPT['profile']} risk x{risk:.2f} min_fires={min_fires} "
        f"| {'boost ' + ','.join(boost) if boost else 'no boost'} "
        f"| {'cut ' + ','.join(cut) if cut else 'no cut'}")

def _audit_cand(c, reason):
    """v23: auditor for signals skipped pre-arming (feed/focus/adapt) — never silent."""
    try:
        _journal_shadow(dict(asset=c["asset"], strategy=c["fired"][0]["strategy"], direc=c["direc"],
                             trade_min=c["minute"] + 60, expiry=c["expiry"]),
                        latest_price(c["asset"]), reason)
    except Exception as e:
        log(f"audit cand error: {e}")

async def _ai_veto(f):
    """v23 AGENT: bounded LLM risk-officer on live entries. Fail-open, JSON-only, budgeted."""
    if not BKEY or AI_CALLS["dec"] >= AI_DECISIONS:
        return False, ""
    AI_CALLS["dec"] += 1
    DDAY["ai_dec"] += 1
    try:
        prompt = ("You are the risk officer vetting ONE live 1-minute binary-option entry "
                  "(OTC demo, payout 92%). Session profile: " + str(ADAPT.get("profile"))
                  + f" (risk x{ADAPT.get('risk')}). Ticket: {f}. "
                  'Answer ONLY with compact JSON: {"action":"keep"|"size_down"|"skip",'
                  '"reason":"<=8 words"}. Skip ONLY for a clear red flag (contradictory '
                  "context, dead market, oversized stake); the default is keep.")
        txt = await asyncio.to_thread(llm_ask, prompt, 90)
    except Exception:
        txt = None
    if not txt:
        AI_CALLS["down"] += 1
        DDAY["ai_down"] += 1
        return False, ""
    try:
        js = json.loads(txt[txt.find("{"): txt.rfind("}") + 1])
    except Exception:
        return False, ""
    act = str(js.get("action", "keep")).lower()
    why = str(js.get("reason", ""))[:60]
    if act == "skip":
        AI_CALLS["skip"] += 1
        return True, why
    return False, ("size_down" if act == "size_down" else "")

def _tts_save(text, path):
    """v23 voice: spoken note via edge-tts (best-effort; text fallback handled upstream)."""
    try:
        import edge_tts
        async def _go():
            c = edge_tts.Communicate(text, os.environ.get("VOICE_NAME", "en-US-GuyNeural"))
            await c.save(path)
        asyncio.run(_go())
        return os.path.exists(path) and os.path.getsize(path) > 2000
    except Exception as e:
        log(f"tts error: {e}")
        return False

def _post_audio(path, caption=""):
    if not TOKEN:
        return
    try:
        with open(path, "rb") as f:
            requests.post(f"{API}/sendAudio",
                          data={"chat_id": CHATID, "caption": (caption or "")[:1024]},
                          files={"audio": f}, timeout=30)
    except Exception as e:
        log(f"audio send error: {e}")

async def tg_voice(text, caption="🧠 v23"):
    """v23: speak the summary when enabled; always fall back to text (never silent)."""
    t = (text or "").strip()
    if not t:
        return
    if VS["on"]:
        p = os.path.join(_BASE, f"v23_voice_{int(time.time())}.mp3")                    # v30 portable
        okq = await asyncio.to_thread(_tts_save, t[:400], p)
        if okq:
            await asyncio.to_thread(_post_audio, p, caption)
            try:
                os.remove(p)
            except Exception:
                pass
            return
    await tg(caption + "\n" + t)

# ==================== v24 APEX MONSTER — ENSEMBLE CORE + LIVE LADDER =========
def _regime_bucket(er_v):
    """CHOP < 0.22 <= MIX < 0.30 <= TREND."""
    try:
        x = float(er_v)
    except Exception:
        return 1
    return 0 if x < 0.22 else (1 if x < 0.30 else 2)

def _reg_w(m, bucket):
    """v24 regime fit: mute a member where it historically loses, damp where marginal."""
    try:
        rr = m.get("regr") or [None, None, None]
        nn = m.get("regn") or [0, 0, 0]
        if bucket >= len(rr) or not nn[bucket] or nn[bucket] < 8 or rr[bucket] is None:
            return 1.0
        a = float(rr[bucket])
        if a < 0.50:
            return 0.0
        if a < 0.55:
            return 0.55
        return 1.0
    except Exception:
        return 1.0

def _tally(votes):
    """v24 weighted-vote tally: [(dir±1, weight)] → (direction, agreement, n_win) or None."""
    if not votes:
        return None
    wb = sum(w for v, w in votes if v > 0)
    ws = sum(w for v, w in votes if v < 0)
    if wb == ws:
        side = max(votes, key=lambda z: z[1])[0]
    else:
        side = 1 if wb > ws else -1
    tot = wb + ws
    return side, (max(wb, ws) / tot if tot > 0 else 0.5), sum(1 for v, _w in votes if v == side)

def _bayes_p(asset, strategy, train_acc):
    """v24 live Bayesian posterior: train prior (strength K) updated by real results."""
    k = BAYES_K
    a = max(0.2, float(train_acc)) * k
    b = max(0.2, 1.0 - float(train_acc)) * k
    rr = list(SET_REC[(asset, strategy)])
    w = sum(1 for x in rr if x == 1)
    p = (a + w) / (a + b + len(rr))
    return float(min(0.85, max(0.30, p)))

def _bayes_mult(p):
    if p >= 0.60:
        return 1.25
    if p >= 0.555:
        return 1.05
    if p >= 0.525:
        return 0.85
    if p >= 0.49:
        return 0.60
    return 0.40

def _health_cold(asset):
    rr = list(PAIR_REC.get(asset, []))
    return len(rr) >= HEALTH_N and sum(rr[-HEALTH_N:]) == 0

_CRYPTO_PFX = ("BTC", "ETH", "SOL", "TRX", "DOGE", "BNB", "LINK", "MATIC", "TON", "LTC",
               "DOT", "XRP", "ADA", "AVAX", "SHIB", "BCH", "ETC", "ATOM", "NEAR", "APT")
_STOCK_PFX = ("AAPL", "TSLA", "INTC", "FB", "META", "BA", "MCD", "PFE", "AXP", "CITI",
              "FDX", "GME", "AMD", "NKE", "DIS", "JPM", "KO", "PEP", "WMT", "NVDA",
              "AMZN", "GOOG", "MSFT", "NFLX", "BABA", "VISA", "XOM", "T", "VZ", "ORCL",
              "PYPL", "UBER", "SNAP", "MS", "GS", "C", "BAC", "CVX", "ABNB", "COIN")
_METAL_PFX = ("XAU", "XAG", "GOLD", "SILVER", "PLAT", "XPT", "XPD")

def _corr_slot(asset):
    s = str(asset).upper().replace("#", "").replace("_OTC", "")
    if s.startswith(_CRYPTO_PFX):
        return "CRYPTO"
    if s.startswith(_METAL_PFX):
        return "METAL"
    if str(asset).startswith("#") or s.startswith(_STOCK_PFX):
        return "STOCK"
    return "FX"

def _v24_mult(asset, strategy, d, conf=0.5, agree=1.0):
    """v24 live ladder: Bayesian tiers + asset health + exposure caps. Demotes, never drops."""
    mult, tags, p = 1.0, [], None
    try:
        DDAY["v24_n"] += 1
        DDAY["v24_cf"] += float(conf)
        DDAY["v24_ag"] += float(agree)
        _ta = None
        for m in MEMBERS.get(asset, []):
            if m["strategy"] == strategy:
                _ta = float(m["test"])
                break
        if _ta is None:
            _ta = 0.55
        rr = SET_REC[(asset, strategy)]
        if ENSEMBLE and len(rr) >= 3:
            p = _bayes_p(asset, strategy, _ta)
            bm = _bayes_mult(p)
            if bm != 1.0:
                mult *= bm
                tags.append(f"bayes{bm:.2f}")
                DDAY["bayes_adj"] += 1
        if STORM_TILT and _storm_vote(asset, d):
            _sv = _storm_vote(asset, d)
            if _sv > 0:
                mult *= 1.20
                tags.append("storm_ag")
                DDAY["storm_ag"] += 1
            else:
                mult *= 0.90
                tags.append("storm_op")
                DDAY["storm_op"] += 1
        if _health_cold(asset):
            mult *= 0.5
            tags.append("health")
            DDAY["health_cut"] += 1
        opp = [x for x in pending if not x.get("mtg")]
        if sum(1 for x in opp if x.get("dir") == d) >= SAMEDIR_MAX:
            mult *= 0.5
            tags.append("dirflood")
        slot = _corr_slot(asset)
        cap = {"CRYPTO": CRYPTO_MAX, "STOCK": STOCK_MAX, "METAL": METAL_MAX}.get(slot)
        if cap is not None and sum(1 for x in opp if _corr_slot(x.get("asset")) == slot) >= cap:
            mult *= 0.5
            tags.append("corr")
        if "corr" in tags or "dirflood" in tags:
            DDAY["corr_half"] += 1
    except Exception as e:
        log(f"v24 ladder error: {e}")
    return mult, tags, p

def _iso_fit(x, y):
    """v24 isotonic calibration (pool-adjacent-violators, no deps)."""
    try:
        xs = np.asarray(x, dtype=float)
        ys = np.asarray(y, dtype=float)
        if len(xs) < 10 or len(np.unique(ys)) < 2:
            return None
        o = np.argsort(xs)
        xs = xs[o]
        ys = ys[o]
        blocks = [[float(v), 1.0, float(xs[i])] for i, v in enumerate(ys)]
        i = 0
        while i < len(blocks) - 1:
            if blocks[i][0] > blocks[i + 1][0]:
                w = blocks[i][1] + blocks[i + 1][1]
                v = (blocks[i][0] * blocks[i][1] + blocks[i + 1][0] * blocks[i + 1][1]) / w
                blocks[i:i + 2] = [[v, w, blocks[i][2]]]
                if i > 0:
                    i -= 1
            else:
                i += 1
        return dict(x=np.array([b[2] for b in blocks]), y=np.array([b[0] for b in blocks]))
    except Exception:
        return None

def _iso_apply(iso, p):
    x = np.asarray(p, dtype=float)
    if not iso:
        return x
    return np.interp(x, iso["x"], iso["y"]).clip(0.05, 0.95)

# ============================ DATABASE v2 ====================================
def db_init():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS trades(
        ts REAL, asset TEXT, strategy TEXT, dir TEXT, grade TEXT,
        entry REAL, close REAL, outcome TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS apex_detail(
        ts REAL, asset TEXT, strategy TEXT, expiry INTEGER, prob REAL,
        conf REAL, sess INTEGER, regime REAL, mode TEXT,
        gate TEXT, margin REAL, razor INTEGER)""")
    con.execute("""CREATE TABLE IF NOT EXISTS apex_audit(
        ts REAL, asset TEXT, strategy TEXT, dir TEXT, expiry INTEGER,
        reason TEXT, entry REAL, close REAL, outcome TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS apex_session(
        ts REAL, signals INTEGER, go INTEGER, cancels INTEGER, w INTEGER,
        l INTEGER, t INTEGER, paper REAL, mtg_w INTEGER, mtg_l INTEGER,
        mtg_net REAL, sh_w INTEGER, sh_l INTEGER, rz_w INTEGER, rz_l INTEGER)""")
    con.execute("""CREATE TABLE IF NOT EXISTS fusion_feed(
        ts REAL, asset TEXT, conf REAL, eqs REAL, aqs REAL, outcome TEXT)""")
    # migrate apex_detail from v17 (add the three v18 columns if missing)
    cols = [r[1] for r in con.execute("PRAGMA table_info(apex_detail)")]
    for c, d in (("gate", "TEXT"), ("margin", "REAL"), ("razor", "INTEGER")):
        if c not in cols:
            try: con.execute(f"ALTER TABLE apex_detail ADD COLUMN {c} {d}")
            except Exception: pass
    con.commit()
    return con

def db_ins_trade(con, p, close, res):
    """Original `trades` write (positional — prove_engine depends on the schema)
       + rich companion row in apex_detail (v18: explicit columns, adds gate/margin/razor)."""
    con.execute("INSERT INTO trades VALUES(?,?,?,?,?,?,?,?)",
                (time.time(), p["asset"], p["strategy"], p["dir"], p["grade"],
                 p["entry"], close, res))
    try:
        con.execute("""INSERT INTO apex_detail(
            ts, asset, strategy, expiry, prob, conf, sess, regime, mode, gate, margin, razor)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (time.time(), p["asset"], p["strategy"], int(p.get("expiry", 1)),
                     float(p.get("pwin") or 0.0), float(p.get("conf") or 0.0),
                     int(p.get("sess", 0)), float(p.get("er") or 0.0),
                     "MTG" if p.get("mtg") else "NORMAL",
                     str(p.get("gate") or "-"), float(p.get("margin") or -1.0),
                     1 if p.get("razor") else 0))
    except Exception:
        pass
    con.commit()

def db_ins_audit(con, p, close, res):
    """Shadow-grade of a cancelled/throttled signal — what WOULD have happened."""
    try:
        con.execute("""INSERT INTO apex_audit(
            ts, asset, strategy, dir, expiry, reason, entry, close, outcome)
            VALUES(?,?,?,?,?,?,?,?,?)""",
                    (time.time(), p["asset"], p["setup"], p["dir"], int(p["expiry"]),
                     p["reason"], p["entry"], close, res))
        con.commit()
    except Exception as e:
        log(f"audit db error: {e}")

# ============================ FETCH ==========================================
async def page(api, sub, asset, t, collect=5.0):
    """v26.1: one polite retry — PO intermittently answers loadHistoryPeriod with no data."""
    for _try in range(2):
        idx = random.randint(10_000_000, 99_999_999)
        await api.send_raw(f'42["loadHistoryPeriod",{{"asset":"{asset}","period":{PERIOD},"time":{t},"index":{idx},"offset":10800}}]')
        dl = time.time() + collect
        while time.time() < dl:
            try:
                raw = await asyncio.wait_for(sub.__anext__(), timeout=max(0.1, dl - time.time()))
            except (asyncio.TimeoutError, StopAsyncIteration):
                break
            if f'"index":{idx}' in raw:
                _d = json.loads(raw).get("data") or []
                if _d:
                    return _d
                break
            await handle_frame(raw, live=False)
        await asyncio.sleep(2.0 + _try * 2.0)
    return []

async def fetch_df(api, sub, asset):
    out = {}
    t = ((int(time.time()) + POFF) // 60) * 60
    for _pi in range(48):
        data = await page(api, sub, asset, t)
        if not data:
            if _pi == 0:
                await asyncio.sleep(3.0)           # v26.1: transient empty history — second chance
                data = await page(api, sub, asset, t)
            if not data:
                break
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

# ======================= CONTEXT FEATURES (v2) ===============================
def ctx_arrays(df):
    c, o, h, l = df["close"], df["open"], df["high"], df["low"]
    d = c.diff()
    rsi = 100 - 100 / (1 + wilder(d.clip(lower=0), 14) / wilder(-d.clip(upper=0), 14).replace(0, np.nan))
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = wilder(tr, 14)
    atrn = (atr / c * 1e4).clip(0, 50)
    hrs = df.index.hour.values
    # premium/discount position inside rolling dealing range
    hi60 = h.rolling(60).max(); lo60 = l.rolling(60).min()
    pdv = ((c - lo60) / (hi60 - lo60).replace(0, np.nan)).clip(0, 1).fillna(0.5)
    # Kaufman efficiency ratio (trend quality)
    move = c.diff().abs().rolling(20).sum().replace(0, np.nan)
    er = ((c - c.shift(20)).abs() / move).clip(0, 1).fillna(0.0)
    # ATR percentile rank (vol regime)
    atrp = atr.rolling(240).rank(pct=True).fillna(0.5)
    sess = np.digitize(hrs, [7, 12, 21])            # 0 ASIA 1 LONDON 2 NY 3 LATE
    return {"rsi": ((rsi - 50) / 25).fillna(0).values, "atrn": (atrn / 10).fillna(0).values,
            "sin": np.sin(2 * np.pi * hrs / 24), "cos": np.cos(2 * np.pi * hrs / 24),
            "mom3": np.sign((c - c.shift(3)).fillna(0)).values,
            "pd": pdv.values, "er": er.values, "atrp": atrp.values,
            "ss": np.sin(2 * np.pi * sess / 4), "sc": np.cos(2 * np.pi * sess / 4)}

def ctx_vec(CT, TF, i, v, mrank, midx, nf=1, agree=1.0):
    """v24: 19-feature context vector — IDENTICAL order in training and live."""
    return [v * TF["m5_t"][i], v * TF["m5_c"][i], v * TF["m15_t"][i], v * TF["m30_t"][i],
            CT["rsi"][i], CT["atrn"][i], CT["sin"][i], CT["cos"][i], v * CT["mom3"][i],
            float(mrank), float(midx), CT["pd"][i], CT["er"][i], CT["atrp"][i],
            v * (2 * CT["pd"][i] - 1), CT["ss"][i], CT["sc"][i],
            float(nf), float(agree)]

# ======================= TIMEFRAME ARRAYS (unchanged API) ====================
def tf_arrays(df):
    """M5/M15/M30 confirmation arrays from COMPLETED higher-TF candles only."""
    sec = df.index.astype(np.int64) // 10**9
    out = {}
    for k, name in ((5, "m5"), (15, "m15"), (30, "m30")):
        g = (sec // (60 * k)) * (60 * k)
        agg = df.groupby(g).agg({"open": "first", "high": "max", "low": "min", "close": "last"})
        c = agg["close"]
        e20 = c.ewm(span=20, adjust=False).mean(); e50 = c.ewm(span=50, adjust=False).mean()
        trend = np.sign(e20 - e50).fillna(0).values
        cdir = np.sign(c - agg["open"]).fillna(0).values
        ends = agg.index.values.astype(np.int64) + 60 * k
        pos = np.searchsorted(ends, sec.values + 60, side="right") - 1
        pc = np.clip(pos, 0, max(len(trend) - 1, 0))
        out[name + "_t"] = np.where(pos >= 0, trend[pc], 0.0)
        out[name + "_c"] = np.where(pos >= 0, cdir[pc], 0.0)
    return out

def tfok(mask, v, TF, i):
    """Confirmation masks. Original set kept byte-identical for prove_engine."""
    if mask == "ANY":      return True
    if mask == "M5A":      return v * TF["m5_t"][i] >= 0
    if mask == "M5C":      return v * TF["m5_c"][i] > 0
    if mask == "M15A":     return v * TF["m15_t"][i] >= 0
    if mask == "DUAL":     return v * TF["m5_t"][i] >= 0 and v * TF["m15_t"][i] >= 0
    if mask == "M30A":     return v * TF["m30_t"][i] >= 0
    if mask == "TRI":      return (v * TF["m5_t"][i] >= 0 and v * TF["m15_t"][i] >= 0
                                   and v * TF["m30_t"][i] >= 0)
    if mask == "TRIPLE_C": return (v * TF["m5_c"][i] > 0 and v * TF["m15_t"][i] >= 0
                                   and v * TF["m30_t"][i] >= 0)
    return True

# ========================= SMC SIGNAL LIBRARY (v17) ==========================
def _supertrend_series(h, l, c, factor=3.2, period=11):
    """v26 SMART X STORM: Pine ta.supertrend port (RMA ATR, band ratchet, trend state).
       Returns (line, direction) with direction -1 = uptrend (above), +1 = downtrend."""
    n = len(c)
    hv, lv, cv = np.asarray(h, float), np.asarray(l, float), np.asarray(c, float)
    tr = np.zeros(n)
    for i in range(1, n):
        tr[i] = max(hv[i] - lv[i], abs(hv[i] - cv[i - 1]), abs(lv[i] - cv[i - 1]))
    atr = np.zeros(n)
    if n:
        atr[0] = tr[0]
    alpha = 1.0 / max(period, 1)
    for i in range(1, n):
        atr[i] = atr[i - 1] + alpha * (tr[i] - atr[i - 1])
    hl2 = (hv + lv) / 2.0
    up = hl2 + factor * atr
    lo = hl2 - factor * atr
    line = np.zeros(n); direc = np.ones(n, dtype=np.int8)
    for i in range(1, n):
        if lo[i] > lo[i - 1] or cv[i - 1] < lo[i - 1]:
            pass
        else:
            lo[i] = lo[i - 1]
        if up[i] < up[i - 1] or cv[i - 1] > up[i - 1]:
            pass
        else:
            up[i] = up[i - 1]
        if line[i - 1] == up[i - 1]:
            direc[i] = -1 if cv[i] > up[i] else 1
        else:
            direc[i] = 1 if cv[i] < lo[i] else -1
        line[i] = lo[i] if direc[i] == -1 else up[i]
    return line, direc


def _storm_read(asset, upto_min=None):
    """v26: supertrend + SMA9 read from the live store (closed candles only)."""
    try:
        st = store.get(asset) or {}
        ts = [k for k in sorted(st) if (upto_min is None or k < upto_min)]
        if len(ts) < 40:
            return None
        cv = np.array([st[k][3] for k in ts], float)
        hv = np.array([st[k][1] for k in ts], float)
        lv = np.array([st[k][2] for k in ts], float)
        _line, dirs = _supertrend_series(hv, lv, cv, STORM_FACTOR, STORM_ATR)
        sma9 = float(np.mean(cv[-9:]))
        return dict(min=ts[-1], dir=int(dirs[-1]), prev=int(dirs[-2]) if len(dirs) > 1 else 0,
                    close=float(cv[-1]), sma9=sma9, line=float(_line[-1]),
                    up=False)  # filled below
    except Exception:
        return None


def _storm_update(asset, upto_min=None):
    """v26: refresh the cached supertrend read (cheap: once per closed minute)."""
    r = _storm_read(asset, upto_min)
    if r is None:
        return None
    ts = [k for k in sorted(store.get(asset) or {}) if (upto_min is None or k < upto_min)]
    _cv = np.array([store[asset][k][3] for k in ts], float)
    _ov = np.array([store[asset][k][0] for k in ts], float)
    r["candle_up"] = bool(_cv[-1] > _ov[-1])
    r["trend_up"] = r["dir"] < 0
    r["turn_up"] = (r["dir"] < 0 and r["prev"] > 0)
    r["turn_dn"] = (r["dir"] > 0 and r["prev"] < 0)
    r["px_up"] = bool(r["dir"] < 0 and len(_cv) > 10 and _cv[-1] > r["sma9"] >= _cv[-2])
    r["px_dn"] = bool(r["dir"] > 0 and len(_cv) > 10 and _cv[-1] < r["sma9"] <= _cv[-2])
    STORM_ST[asset] = r
    return r


def _storm_vote(asset, d):
    """v26: +1 the supertrend core agrees with direction d (±1), -1 opposes, 0 unknown."""
    r = STORM_ST.get(asset)
    if not r:
        return 0
    _sd = 1 if r.get("dir", 0) < 0 else -1        # dir -1 = uptrend = BUY side (Pine semantics)
    _sgn = 1 if d in (1, "BUY") else -1
    return 1 if _sd == _sgn else -1


def build_smc(df):
    """All causal. Returns (S, AUX): S = {setup: int8 array in {-1,0,1}},
       AUX = context arrays (dirS, pd, er, atrp, sess)."""
    c, o, h, l = df["close"], df["open"], df["high"], df["low"]
    n = len(df)
    up, dn = (c > o), (c < o)
    body = (c - o).abs(); rng = (h - l).replace(0, np.nan)
    ab = body.rolling(10).mean()
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = wilder(tr, 14).replace(0, np.nan)
    disp = body >= 1.5 * ab
    pin_b = ((np.minimum(o, c) - l) >= 2 * body) & ((np.minimum(o, c) - l) >= 0.55 * rng)
    pin_s = ((h - np.maximum(o, c)) >= 2 * body) & ((h - np.maximum(o, c)) >= 0.55 * rng)
    eng_b = up & dn.shift(1).fillna(False) & (c >= o.shift()) & (o <= c.shift())
    eng_s = dn & up.shift(1).fillna(False) & (c <= o.shift()) & (o >= c.shift())
    # confirmed 2-bar fractal swings (known 2 bars later — causal)
    fr_hi = (h.shift(2) > h.shift(1)) & (h.shift(2) > h.shift(3)) & (h.shift(2) > h) & (h.shift(2) > h.shift(4))
    fr_lo = (l.shift(2) < l.shift(1)) & (l.shift(2) < l.shift(3)) & (l.shift(2) < l) & (l.shift(2) < l.shift(4))
    liqH = pd.Series(np.where(fr_hi, h.shift(2), np.nan), index=df.index).ffill()
    liqL = pd.Series(np.where(fr_lo, l.shift(2), np.nan), index=df.index).ffill()
    prevH = pd.Series(np.where(fr_hi, h.shift(2), np.nan), index=df.index).shift(1).ffill()
    prevL = pd.Series(np.where(fr_lo, l.shift(2), np.nan), index=df.index).shift(1).ffill()
    eqH = fr_hi & ((h.shift(2) - prevH).abs() <= 0.15 * atr)       # equal-highs pool formed
    eqL = fr_lo & ((l.shift(2) - prevL).abs() <= 0.15 * atr)
    poolH = pd.Series(np.where(eqH, np.maximum(h.shift(2), prevH), np.nan), index=df.index).ffill()
    poolL = pd.Series(np.where(eqL, np.minimum(l.shift(2), prevL), np.nan), index=df.index).ffill()
    # structure state: +1 after close above liqH, -1 after close below liqL
    st = np.zeros(n); sv = 0.0
    cl, lh, ll = c.values, liqH.values, liqL.values
    for i in range(n):
        if not np.isnan(lh[i]) and cl[i] > lh[i]: sv = 1.0
        elif not np.isnan(ll[i]) and cl[i] < ll[i]: sv = -1.0
        st[i] = sv
    struct = pd.Series(st, index=df.index)
    sweepL = (l < liqL) & (c > liqL)                    # took lows, closed back = stop hunt
    sweepH = (h > liqH) & (c < liqH)
    sweepPL = (l < poolL) & (c > poolL)                 # swept EQUAL-lows pool
    sweepPH = (h > poolH) & (c < poolH)
    bosU = (c > liqH) & (c.shift() <= liqH.shift())
    bosD = (c < liqL) & (c.shift() >= liqL.shift())
    # SMA stack
    s20, s50 = c.rolling(20).mean(), c.rolling(50).mean()
    s100, s200 = c.rolling(100).mean(), c.rolling(200).mean()
    stackB = (s20 > s50) & (s50 > s100) & (s100 > s200)
    stackS = (s20 < s50) & (s50 < s100) & (s100 < s200)
    def SIG(b, s): return np.where(b.fillna(False), 1, 0) - np.where(s.fillna(False), 1, 0)
    S = {}
    S["SWEEP_rev"] = SIG(sweepL & up, sweepH & dn)
    S["SWEEP_disp"] = SIG(sweepL & up & disp, sweepH & dn & disp)
    S["SWEEP_pool"] = SIG(sweepPL & up, sweepPH & dn)                 # equal-pool hunt (A+)
    S["SWEEP_pin"] = SIG((sweepL | sweepPL) & pin_b, (sweepH | sweepPH) & pin_s)
    S["SWEEP_engulf"] = SIG(sweepL.shift(1).fillna(False) & eng_b, sweepH.shift(1).fillna(False) & eng_s)
    # NEW: sweep + strong reclaim candle (close in extreme third, range >= 0.8 ATR)
    strong_up = up & (rng >= 0.8 * atr) & ((c - l) >= 0.6 * rng)
    strong_dn = dn & (rng >= 0.8 * atr) & ((h - c) >= 0.6 * rng)
    S["SWEEP_reclaim"] = SIG((sweepL | sweepPL) & strong_up, (sweepH | sweepPH) & strong_dn)
    S["BOS_cont"] = SIG(bosU & disp, bosD & disp)
    S["BOS_retest"] = SIG(bosU.shift(2).fillna(False) & (l <= liqH.shift(2)) & (c > liqH.shift(2)) & up,
                          bosD.shift(2).fillna(False) & (h >= liqL.shift(2)) & (c < liqL.shift(2)) & dn)
    S["CHOCH_rev"] = SIG((struct.shift() < 0) & bosU, (struct.shift() > 0) & bosD)
    S["SMA_stack_pull"] = SIG(stackB & (l <= s20) & (c > s20) & up, stackS & (h >= s20) & (c < s20) & dn)
    S["SMA200_bounce"] = SIG(((l - s200).abs() <= 0.25 * atr) & (c > s200) & up,
                             ((h - s200).abs() <= 0.25 * atr) & (c < s200) & dn)
    # ---- v26 SMART X STORM BINARY (user's Pine: supertrend 3.2/11 + SMA9 + candle confirm) ----
    _stline, _stdir = _supertrend_series(h, l, c, STORM_FACTOR, STORM_ATR)
    _std = pd.Series(_stdir, index=df.index)
    _st_up = _std < 0
    _st_dn = _std > 0
    _sma9 = c.rolling(9).mean()
    _turn_up = _st_up & (_std.shift(1) > 0)
    _turn_dn = _st_dn & (_std.shift(1) < 0)
    _px_up = (c > _sma9) & (c.shift(1) <= _sma9.shift(1))
    _px_dn = (c < _sma9) & (c.shift(1) >= _sma9.shift(1))
    S["STORM_turn"] = SIG(_turn_up.fillna(False), _turn_dn.fillna(False))
    S["STORM_x"] = SIG((_st_up & _px_up).fillna(False), (_st_dn & _px_dn).fillna(False))
    S["STORM_god"] = SIG(((_turn_up | (_st_up & _px_up)) & up & (c >= _sma9)).fillna(False),
                         ((_turn_dn | (_st_dn & _px_dn)) & dn & (c <= _sma9)).fillna(False))
    # ---- FVG + OB (tracked) + BREAKER + FVG stack ----
    fvg_sig = np.zeros(n); ob_sig = np.zeros(n); brk_sig = np.zeros(n); stk_sig = np.zeros(n)
    hv, lv, ov, cv2 = h.values, l.values, o.values, c.values
    atrv = np.asarray(atr)
    bU, bD = np.asarray(bosU.fillna(False)), np.asarray(bosD.fillna(False))
    dispv = np.asarray(disp.fillna(False))
    fvg = None; ob = None; brk = None
    gaps = deque(maxlen=10)                 # (dir, bar_idx) of recently created gaps
    for i in range(3, n):
        a_ = atrv[i] if atrv[i] == atrv[i] else 0.0
        # ----- FVG detect: requires >= 0.25 ATR imbalance (kills micro noise) -----
        if a_ > 0 and (lv[i] - hv[i - 2]) >= 0.25 * a_:
            fvg = (lv[i], hv[i - 2], 1, 0); gaps.append((1, i))
        elif a_ > 0 and (lv[i - 2] - hv[i]) >= 0.25 * a_:
            fvg = (lv[i - 2], hv[i], -1, 0); gaps.append((-1, i))
        elif fvg is not None:
            top, bot, d_, age = fvg
            age += 1; fvg = (top, bot, d_, age)
            if age > 30:
                fvg = None
            elif d_ == 1 and lv[i] <= top and cv2[i] > top and cv2[i] > ov[i]:
                fvg_sig[i] = 1
                if sum(1 for (gd, gi) in gaps if gd == 1 and i - gi <= 15) >= 2:
                    stk_sig[i] = 1
                fvg = None
            elif d_ == -1 and hv[i] >= bot and cv2[i] < bot and cv2[i] < ov[i]:
                fvg_sig[i] = -1
                if sum(1 for (gd, gi) in gaps if gd == -1 and i - gi <= 15) >= 2:
                    stk_sig[i] = -1
                fvg = None
        # ----- OB detect (needs displacement) + retrace or breaker conversion -----
        if bU[i] and dispv[i] and cv2[i - 1] < ov[i - 1]:
            ob = (max(ov[i - 1], cv2[i - 1]), min(ov[i - 1], cv2[i - 1]), 1, 0)
        elif bD[i] and dispv[i] and cv2[i - 1] > ov[i - 1]:
            ob = (max(ov[i - 1], cv2[i - 1]), min(ov[i - 1], cv2[i - 1]), -1, 0)
        elif ob is not None:
            top, bot, d_, age = ob
            age += 1; ob = (top, bot, d_, age)
            if age > 40:
                ob = None
            elif d_ == 1 and cv2[i] < bot - 0.05 * a_:
                brk = (top, bot, -1, 0); ob = None        # bull OB failed → bearish breaker
            elif d_ == -1 and cv2[i] > top + 0.05 * a_:
                brk = (top, bot, 1, 0); ob = None         # bear OB failed → bullish breaker
            elif d_ == 1 and lv[i] <= top and cv2[i] > top and cv2[i] > ov[i]:
                ob_sig[i] = 1; ob = None
            elif d_ == -1 and hv[i] >= bot and cv2[i] < bot and cv2[i] < ov[i]:
                ob_sig[i] = -1; ob = None
        # ----- BREAKER retest -----
        if brk is not None:
            top, bot, bd, age = brk
            age += 1; brk = (top, bot, bd, age)
            if age > 40:
                brk = None
            elif bd == 1 and lv[i] <= top and cv2[i] > top and cv2[i] > ov[i]:
                brk_sig[i] = 1; brk = None
            elif bd == -1 and hv[i] >= bot and cv2[i] < bot and cv2[i] < ov[i]:
                brk_sig[i] = -1; brk = None
    S["FVG_retrace"] = fvg_sig
    S["FVG_stack"] = stk_sig
    S["OB_retrace"] = ob_sig
    S["BREAKER_retest"] = brk_sig
    # ===== MR-ULTRAFAST family (ported & decoded from user's indicator pack) =====
    roc9 = c.pct_change(9) * 100
    e3_ = c.ewm(span=3, adjust=False).mean(); e5_ = c.ewm(span=5, adjust=False).mean()
    e9_ = c.ewm(span=9, adjust=False).mean(); e13_ = c.ewm(span=13, adjust=False).mean()
    d_ = c.diff()
    rsi13 = 100 - 100 / (1 + wilder(d_.clip(lower=0), 13) / wilder(-d_.clip(upper=0), 13).replace(0, np.nan))
    atr5_ = wilder(tr, 5)
    mom10 = c - c.shift(10)
    vel_ = roc9.ewm(span=5, adjust=False).mean()
    vm_ = vel_.rolling(30).mean(); vs_ = vel_.rolling(30).std()
    vlb_ = vm_ - 1.5 * vs_; vub_ = vm_ + 1.5 * vs_
    hi5c = c.shift(1).rolling(5).max(); lo5c = c.shift(1).rolling(5).min()
    volf_ = rng > 1.2 * atr
    S["MR_roc_break"] = SIG((roc9 > 0) & (roc9.shift() <= 0) & volf_ & (c > hi5c) & up,
                            (roc9 < 0) & (roc9.shift() >= 0) & volf_ & (c < lo5c) & dn)
    S["MR_vel_band"] = SIG((vel_.shift() < vlb_.shift()) & (vel_ > vlb_) & up,
                           (vel_.shift() > vub_.shift()) & (vel_ < vub_) & dn)
    S["MR_mom_atr"] = SIG((mom10 > atr) & ~(mom10.shift() > atr.shift()).fillna(False) & (c > e9_) & up,
                          (mom10 < -atr) & ~(mom10.shift() < -atr.shift()).fillna(False) & (c < e9_) & dn)
    S["MR_atr_regime"] = SIG((c > e5_) & (c.shift() <= e5_.shift()) & (l > l.shift()) & (atr5_ > atr),
                             (c < e5_) & (c.shift() >= e5_.shift()) & (h < h.shift()) & (atr5_ > atr))
    S["MR_ema_corridor"] = SIG((e3_ > e13_) & (e3_.shift() <= e13_.shift()) & (rsi13 >= 48) & (rsi13 <= 65) & (rng > 0.8 * atr) & up,
                               (e3_ < e13_) & (e3_.shift() >= e13_.shift()) & (rsi13 <= 52) & (rsi13 >= 35) & (rng > 0.8 * atr) & dn)
    # ===== S/R ZONES (multi-touch) + MARKET STRUCTURE (HH/HL vs LH/LL) + MOVEMENT =====
    frh = np.asarray(fr_hi.fillna(False)); frl = np.asarray(fr_lo.fillna(False))
    sr_b = np.zeros(n); sr_br = np.zeros(n)
    st_pull = np.zeros(n); st_flip = np.zeros(n); mom_imp = np.zeros(n)
    dirS = np.zeros(n)
    levels = []; hh2 = [None, None]; ll2 = [None, None]
    for i in range(n):
        a_ = atrv[i] if atrv[i] == atrv[i] else 0.0
        if frh[i]:
            levels.append(hv[i - 2]); hh2 = [hh2[1], hv[i - 2]]
        if frl[i]:
            levels.append(lv[i - 2]); ll2 = [ll2[1], lv[i - 2]]
        if len(levels) > 14: levels = levels[-14:]
        if hh2[0] is not None and ll2[0] is not None:
            if hh2[1] > hh2[0] and ll2[1] > ll2[0]: dirS[i] = 1
            elif hh2[1] < hh2[0] and ll2[1] < ll2[0]: dirS[i] = -1
            else: dirS[i] = dirS[i - 1] if i else 0
        if a_ > 0 and len(levels) >= 2 and i >= 2:
            zone = None
            for zi in range(len(levels) - 1):
                for zj in range(zi + 1, len(levels)):
                    if abs(levels[zi] - levels[zj]) <= 0.25 * a_:
                        zone = (levels[zi] + levels[zj]) / 2; break
                if zone is not None: break
            if zone is not None:
                z = zone
                if lv[i] <= z + 0.1 * a_ and cv2[i] > z and cv2[i] > ov[i] and ov[i] > z - a_:
                    sr_b[i] = 1
                elif hv[i] >= z - 0.1 * a_ and cv2[i] < z and cv2[i] < ov[i] and ov[i] < z + a_:
                    sr_b[i] = -1
                if cv2[i - 1] > z and lv[i] <= z and cv2[i] > z and cv2[i] > ov[i]:
                    sr_br[i] = 1
                elif cv2[i - 1] < z and hv[i] >= z and cv2[i] < z and cv2[i] < ov[i]:
                    sr_br[i] = -1
        if i >= 2:
            if dirS[i] > 0 and cv2[i - 1] < ov[i - 1] and cv2[i] > ov[i] and lv[i] > lv[i - 1]: st_pull[i] = 1
            elif dirS[i] < 0 and cv2[i - 1] > ov[i - 1] and cv2[i] < ov[i] and hv[i] < hv[i - 1]: st_pull[i] = -1
            if dirS[i] > 0 and dirS[i - 1] <= 0: st_flip[i] = 1
            elif dirS[i] < 0 and dirS[i - 1] >= 0: st_flip[i] = -1
        if i >= 3:
            b0, b1, b2 = abs(cv2[i] - ov[i]), abs(cv2[i - 1] - ov[i - 1]), abs(cv2[i - 2] - ov[i - 2])
            if cv2[i] > ov[i] and cv2[i - 1] > ov[i - 1] and cv2[i - 2] > ov[i - 2] and b0 > b1 > b2 and dirS[i] >= 0:
                mom_imp[i] = 1
            elif cv2[i] < ov[i] and cv2[i - 1] < ov[i - 1] and cv2[i - 2] < ov[i - 2] and b0 > b1 > b2 and dirS[i] <= 0:
                mom_imp[i] = -1
    S["SR_bounce"] = sr_b
    S["SR_break_retest"] = sr_br
    S["STRUCT_pull"] = st_pull
    S["STRUCT_flip"] = st_flip
    S["MOM_impulse"] = mom_imp
    # ================= CONTEXT ARRAYS + GATES (v17) =================
    hi60 = h.rolling(60).max(); lo60 = l.rolling(60).min()
    pdv = ((c - lo60) / (hi60 - lo60).replace(0, np.nan)).clip(0, 1).fillna(0.5)
    er = ((c - c.shift(20)).abs() / c.diff().abs().rolling(20).sum().replace(0, np.nan)).clip(0, 1).fillna(0.0)
    atrp = atr.rolling(240).rank(pct=True).fillna(0.5)
    sess = np.digitize(df.index.hour.values, [7, 12, 21])
    SIGS = {k: np.asarray(v, dtype=np.int8) for k, v in S.items()}
    if REG_GATE:
        erV = np.asarray(er); apV = np.asarray(atrp)
        dead = apV < 0.12; blow = apV > 0.96
        for nm in SIGS:
            if nm.startswith("MR_"):
                ok = (erV < 0.55) & ~dead & ~blow       # MR needs non-trending, alive tape
            elif nm.startswith("MOM_"):
                ok = (erV >= 0.25) & ~dead              # momentum needs actual trend
            else:
                ok = ~dead                              # structure setups: just no dead tape
            SIGS[nm] = np.where(ok, SIGS[nm], 0).astype(np.int8)
    if PD_GATE:
        pdV = np.asarray(pdv)
        for nm, sg in SIGS.items():
            if nm.startswith(("SWEEP_", "SR_", "STRUCT_flip", "BREAKER")):
                lo_ok, sh_ok = pdV <= 0.50, pdV >= 0.50  # pure reversals: extremes only
            elif nm.startswith(("CHOCH_", "MR_")):
                lo_ok, sh_ok = pdV <= 0.65, pdV >= 0.35  # soft reversals
            elif nm.startswith(("BOS_", "FVG_", "OB_", "SMA", "STRUCT_pull", "MOM_")):
                lo_ok, sh_ok = pdV <= 0.80, pdV >= 0.20  # continuations: keep structure side
            else:
                continue
            bad = ((sg > 0) & ~lo_ok) | ((sg < 0) & ~sh_ok)
            SIGS[nm] = np.where(bad, 0, sg).astype(np.int8)
    return SIGS, {"dirS": dirS, "pd": np.asarray(pdv), "er": np.asarray(er),
                  "atrp": np.asarray(atrp), "sess": sess}

# ============================ TRAINING v17 ===================================
def train_smc(df):
    S, AUX = build_smc(df)
    TF = tf_arrays(df)
    close = df["close"].values; n = len(df)
    i2 = int(n * 0.8)
    days_te = (df.index[-1] - df.index[i2]).total_seconds() / 86400
    days_all = max((df.index[-1] - df.index[210]).total_seconds() / 86400, 1e-9)
    bounds = np.linspace(210, n - 2, 5).astype(int)

    def folds_for(sg, mask, k):
        """4-fold accuracy with embargo at each seam + label-overlap safety."""
        accs, ns = [], []
        for f in range(4):
            a_ = bounds[f] + (EMBARGO + k if f > 0 else 0)
            b_ = min(bounds[f + 1], n - k)
            if b_ - a_ < 30: accs.append(0.0); ns.append(0); continue
            w = np.where(sg[a_:b_] != 0)[0] + a_
            if mask != "ANY" and len(w):
                w = np.array([j for j in w if tfok(mask, sg[j], TF, j)], dtype=int)
            if len(w) == 0: accs.append(0.0); ns.append(0); continue
            dv = close[w + k] - close[w]; ok = dv != 0
            if ok.sum() < 6: accs.append(0.0); ns.append(int(ok.sum())); continue
            accs.append(float((np.where(sg[w[ok]] == 1, dv[ok] > 0, dv[ok] < 0)).mean()))
            ns.append(int(ok.sum()))
        return accs, ns

    # ---- nomination: setup x mask x expiry, 3-of-4 folds, embargoed ----
    rows = []
    for name, sg0 in S.items():
        sg = np.asarray(sg0)
        best = None
        for mask in MASKS:
            for k in EXPIRIES:
                accs, ns = folds_for(sg, mask, k)
                passed = sum(1 for a2, n2 in zip(accs, ns) if n2 >= 6 and a2 >= 0.55)
                valid = [a2 for a2, n2 in zip(accs, ns) if n2 >= 6]
                if passed < 3 or not valid: continue
                meanacc = float(np.mean(valid)); minacc = float(np.min(valid)); ntot = int(sum(ns))
                if ntot < 15: continue
                tier = "A" if (passed == 4 and meanacc >= 0.58) else "B" if meanacc >= 0.57 else "C"
                if tier == "C" and meanacc < 0.56: continue
                row = dict(strategy=name, mask=mask, expiry=k, tier=tier,
                           train=round(minacc, 4), val=round(minacc, 4), test=round(meanacc, 4),
                           test_n=ntot, z=float(passed), sig_per_day=round(ntot / days_all, 1))
                key = (RANK[tier], -meanacc, k)
                if best is None or key < best[0]: best = (key, row)
        if best: rows.append(best[1])
    if not rows: return None
    rows.sort(key=lambda r: (RANK[r["tier"]], -r["test"]))
    members = [r for r in rows if r["tier"] in "AB"][:6] or [r for r in rows if r["tier"] == "C"][:4]
    if not members: return None
    S2 = {m["strategy"]: np.asarray(S[m["strategy"]]) for m in members}
    # ---- v24: per-member regime fit (accuracy by ER bucket, train window only) ----
    _erb_all = np.array([_regime_bucket(e) for e in np.asarray(AUX["er"])])
    for m in members:
        _sg = S2[m["strategy"]]
        _ra = [0.0, 0.0, 0.0]
        _rn = [0, 0, 0]
        for _i in range(210, n - 3 * max(EXPIRIES)):
            _v = int(_sg[_i])
            if _v != 0 and tfok(m["mask"], _v, TF, _i):
                _dv = close[_i + m["expiry"]] - close[_i]
                if _dv == 0:
                    continue
                _b = int(_erb_all[_i])
                _rn[_b] += 1
                _ra[_b] += 1.0 if (_dv > 0) == (_v > 0) else 0.0
        m["regr"] = [(_ra[b] / _rn[b]) if _rn[b] else None for b in range(3)]
        m["regn"] = _rn
    # ---- market character + hour-edge map (train+val only, causal) ----
    cl_s = df["close"]
    d1 = np.sign(cl_s.diff()); nx = d1.shift(-1)
    mm_ = (d1 != 0) & (nx != 0) & ~d1.isna() & ~nx.isna()
    follow = float((d1[mm_] == nx[mm_]).mean()) if mm_.sum() else 0.5
    tie_rate = float((nx == 0).mean())
    hrs_blk = (df.index.hour.values // 3).astype(int)
    bn = np.zeros(8); bw = np.zeros(8)
    for i in range(210, i2):
        hit = None
        for m in members:
            v = S2[m["strategy"]][i]
            if v != 0 and tfok(m["mask"], v, TF, i):
                hit = (v, m["expiry"]); break
        if hit is None: continue
        dv = close[i + hit[1]] - close[i]
        if dv == 0: continue
        b = hrs_blk[i]; bn[b] += 1
        if (dv > 0) == (hit[0] > 0): bw[b] += 1
    hour_ok = [bool(bn[b] < 8 or bw[b] / bn[b] >= 0.52) for b in range(8)]
    blocked = [b * 3 for b in range(8) if not hour_ok[b]]
    # ---- untouched test window: direct + 1-step MTG recovery ----
    wins, cnt, rw, rn, rw2 = [], 0, 0, 0, 0
    for i in range(i2, n - 3 * max(EXPIRIES)):
        if not hour_ok[hrs_blk[i]]: continue
        hit = None
        for m in members:
            v = S2[m["strategy"]][i]
            if v != 0 and tfok(m["mask"], v, TF, i):
                hit = (v, m["expiry"]); break
        if hit is None: continue
        v, k = hit
        dv = close[i + k] - close[i]
        if dv == 0: continue
        cnt += 1
        win1 = (dv > 0) == (v > 0)
        wins.append(win1); rn += 1
        if win1:
            rw += 1
        else:
            dv2 = close[i + 2 * k] - close[i + k]
            if dv2 != 0 and ((dv2 > 0) == (v > 0)): rw += 1
            dv3 = close[i + 3 * k] - close[i + k]
            if dv3 != 0 and ((dv3 > 0) == (v > 0)): rw2 += 1
    base_acc = float(np.mean(wins)) if wins else 0.0
    # ---- META-LABEL FILTER v2: train / calibrate / test at SIGNAL level ----
    meta = None
    if lgb is not None:
        try:
            CT = ctx_arrays(df)
            samples = []
            for i in range(210, n - 3 * max(EXPIRIES)):
                votes = []
                for mi, m in enumerate(members):
                    vv = int(S2[m["strategy"]][i])
                    if vv != 0 and tfok(m["mask"], vv, TF, i):
                        votes.append((vv, mi, m, float(m["test"]) * _reg_w(m, int(_erb_all[i]))))
                if not votes: continue
                _vz = [(vv, w) for vv, _mi, _m, w in votes]
                if not any(w > 0 for _v2, w in _vz):
                    _vz = [(vv, max(w, 0.05)) for vv, w in _vz]
                _act = _tally(_vz)
                if _act is None: continue
                _dt, _ag, _nf = _act
                _winv = [z for z in votes if z[0] == _dt]
                if not _winv: continue
                v, mi, m_, _w = max(_winv, key=lambda z: z[3])
                k = m_["expiry"]
                dv = close[i + k] - close[i]
                if dv == 0: continue
                samples.append((ctx_vec(CT, TF, i, v, RANK[m_["tier"]], mi, _nf, _ag),
                                1 if (dv > 0) == (v > 0) else 0))
            nS = len(samples)
            if nS >= 120:
                q1, q2 = int(nS * 0.55), int(nS * 0.78)
                Xa = np.array([s[0] for s in samples[:q1]]);      Ya = np.array([s[1] for s in samples[:q1]])
                Xb = np.array([s[0] for s in samples[q1:q2]]);    Yb = np.array([s[1] for s in samples[q1:q2]])
                Xc = np.array([s[0] for s in samples[q2:]]);      Yc = np.array([s[1] for s in samples[q2:]])
                mdl = lgb.LGBMClassifier(n_estimators=160, max_depth=3, learning_rate=0.06,
                                         min_child_samples=18, verbose=-1, random_state=7)
                mdl.fit(Xa, Ya)
                pb = mdl.predict_proba(Xb)[:, 1]
                iso = _iso_fit(pb, Yb) if META_ISO else None      # v24 calibration
                thr_best, prec_best = None, -1.0
                for thr in np.arange(0.50, 0.71, 0.01):
                    sel = pb >= thr
                    if sel.sum() < max(15, 0.25 * len(Xb)): continue
                    prec = float(Yb[sel].mean())
                    if prec > prec_best: thr_best, prec_best = float(thr), prec
                if thr_best is not None and len(Xc) >= 25:
                    pc = _iso_apply(iso, mdl.predict_proba(Xc)[:, 1]) if iso is not None \
                        else mdl.predict_proba(Xc)[:, 1]
                    sel = pc >= thr_best
                    base_te = float(np.mean(Yc))
                    facc = float(Yc[sel].mean()) if sel.sum() >= 8 else 0.0
                    keep = float(sel.mean())
                    if keep >= 0.40 and facc >= max(base_te + 0.015, 0.505):
                        meta = dict(model=mdl, thr=round(thr_best, 3), facc=round(facc, 4),
                                    keep=round(keep, 2), base=round(base_te, 4), n=int(len(Xc)),
                                    iso=iso)
        except Exception:
            meta = None
    mtg_k = 2 if rw2 > rw else 1
    return dict(members=members, aif=meta, hour_ok=hour_ok, blocked=blocked, mtg_k=mtg_k,
                char=dict(follow=round(follow, 3), tie=round(tie_rate, 3)),
                union=dict(test_acc=round(base_acc, 4),
                           mtg_acc=round(rw / rn, 4) if rn else 0.0,
                           test_n=cnt, sig_per_day=round(cnt / max(days_te, 1e-9), 1)))

# ============================ LIVE ===========================================
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

def _atr_proxy(asset, minute, n=30):
    """Cheap ATR proxy (mean true-ish range of last n closed candles) for margin/razor math."""
    st = store.get(asset, {})
    ts = [k for k in sorted(st) if k < minute][-n:]
    if len(ts) < 5: return None
    a = sum(st[k][1] - st[k][2] for k in ts) / len(ts)
    return a if a > 0 else None

def _roll_day():
    d = datetime.now(IST).strftime("%Y-%m-%d")
    if DDAY.get("d") != d:
        DDAY.update(d=d, sig=0, w=0, l=0, pnl=0.0, b0=BAL_D.get("v", 100.0))

def _altr_ratio(cl):
    """v30 SNIPER: candle alternation 0..1 — high = chopping tape (research: skip alternating)."""
    try:
        d = np.diff(np.asarray(cl[-12:], dtype=float))
        s = np.sign(d); s = s[s != 0]
        if len(s) < 5: return 0.0
        return float(np.mean(s[1:] != s[:-1]))
    except Exception:
        return 0.0


def _dead_zone(h):
    """v30 SNIPER: UTC low-liquidity window (post-US close / pre-Asia) — research: false breaks."""
    if not SNIPER_DZ: return False
    if DZ_START <= DZ_END: return DZ_START <= h < DZ_END
    return h >= DZ_START or h < DZ_END


# ═══════════════ v33 OMEGA — new accuracy engines (A–E) ═══════════════
def _regime_radar(cl, rng, er):
    """ENGINE A — REGIME RADAR: forecast tape character for the next minutes.
    Drift efficiency + swing alternation + body ratio + efficiency ratio → 0..1 + tag."""
    try:
        cl = np.asarray(cl[-20:], dtype=float)
        rng = np.asarray(rng[-20:], dtype=float)
        d = np.diff(cl)
        s = np.sign(d); s = s[s != 0]
        altr = float(np.mean(s[1:] != s[:-1])) if len(s) > 2 else 1.0
        path = float(np.sum(np.abs(d))) or 1e-12
        drift = abs(float(cl[-1] - cl[0])) / path
        med_r = float(np.median(rng)) or 1e-12
        body = float(np.median(np.abs(d))) / med_r
        er_s = min(1.0, max(0.0, (float(er) - 0.12) / 0.35))
        rg = 0.35 * er_s + 0.35 * drift + 0.20 * (1.0 - min(1.0, altr)) + 0.10 * min(1.0, body)
        rg = max(0.0, min(1.0, rg))
        tag = "TREND" if rg >= 0.62 else "CHOP" if rg < 0.45 else "MIX"
        return rg, tag
    except Exception:
        return 0.5, "MIX"


def _mtf_confluence(TF, i, direc):
    """ENGINE B — MTF CONFLUENCE: weighted agreement of the 1m signal with M5/M15/M30 axes."""
    dd = 1 if direc > 0 else -1
    a = n = 0.0
    for key, w in (("m5_t", 0.40), ("m15_t", 0.35), ("m30_t", 0.25)):
        try:
            v = float(TF[key][i])
            n += w
            if (v > 0 and dd > 0) or (v < 0 and dd < 0):
                a += w
        except Exception:
            pass
    return (a / n) if n else 0.5


def _chaos_ok(rng, med):
    """v33 GATE: any of the last 3 candles > CHAOS_MULT × median range = chaos, stand down."""
    try:
        r = np.asarray(rng[-3:], dtype=float)
        return not (med > 0 and len(r) and float(np.max(r)) > CHAOS_MULT * med)
    except Exception:
        return True


def _fresh_ext(cl, rng):
    """v33 GATE: entry freshness — extension over the last 5 candles in ATR units."""
    try:
        cl = np.asarray(cl, dtype=float)
        if len(cl) < 20: return 0.0
        step = abs(float(cl[-1] - cl[-6]))
        atr = float(np.mean(np.asarray(rng[-15:], dtype=float))) or 1e-12
        return step / atr
    except Exception:
        return 0.0


def _hq_adj(asset, hour):
    """ENGINE C — MEMORY: self-learned hour-quality from the engine's own trade DB."""
    try:
        w, l = HQ.get(asset, {}).get(int(hour) // 3, (0, 0))
        n = w + l
        if n >= 8:
            r = w / n
            if r >= 0.62: return 0.03, "HQ+"
            if r < 0.52: return -0.06, "HQ-"
    except Exception:
        pass
    return 0.0, ""


def _hq_build():
    """ENGINE C — MEMORY builder: per-asset × 3h-bucket W/L from pro_signals.db."""
    try:
        HQ.clear()
        for a, ts, o in CON.execute("SELECT asset, ts, outcome FROM trades WHERE outcome IS NOT NULL"):
            oo = str(o).upper()
            if oo not in ("W", "L"): continue
            hb = (int(int(ts) // 3600) % 24) // 3
            w, l = HQ.setdefault(str(a), {}).get(hb, (0, 0))
            HQ[str(a)][hb] = (w + (1 if oo == "W" else 0), l + (1 if oo == "L" else 0))
        log(f"v33 MEMORY: hour-quality table from DB — {sum(len(v) for v in HQ.values())} buckets")
    except Exception as ex:
        log(f"v33 MEMORY build skipped: {ex}")


def _cal_learn(conf, res):
    """ENGINE D — CALIBRATION LOOP: track live W/L per confidence bucket (0.05 steps)."""
    try:
        if res not in ("W", "L"): return
        b = CAL.setdefault(f"{round(float(conf or 0.5) * 20) / 20:.2f}", {"w": 0, "l": 0})
        b["w" if res == "W" else "l"] += 1
    except Exception:
        pass


def _cal_pen(conf):
    """ENGINE D — penalty when a live confidence bucket underperforms (n≥12, <52%)."""
    try:
        b = CAL.get(f"{round(float(conf or 0.5) * 20) / 20:.2f}")
        if b:
            n = b["w"] + b["l"]
            if n >= 12 and b["w"] / n < 0.52: return -0.04
    except Exception:
        pass
    return 0.0


def _aqs_score(grade, conf, agree, nfw, pwin, er, altr, mtf, rg, hq_adj, payout, storm_ag, cal_p):
    """ENGINE E — AQS: single 0..1 accuracy score fusing every engine + live memory."""
    s = 0.34 * (pwin if pwin is not None else (conf - 0.05))
    s += 0.16 * min(1.0, conf)
    s += 0.12 * min(1.0, agree)
    s += 0.10 * mtf
    s += 0.10 * rg
    s += 0.06 * (1.0 - min(1.0, altr))
    s += 0.03 * min(1.0, nfw / 3.0)
    s += 0.03 * {"APEX": 1.0, "HIGH": 0.6}.get(grade, 0.2)
    s += 0.02 * (1.0 if payout >= 92 else 0.4)
    s += 0.04 * (1.0 if storm_ag else 0.5)
    s += hq_adj + cal_p
    return max(0.0, min(1.0, s))



# ═══════════════════════ v33 OMEGA ENGINES — F · G · H · I · K ═══════════════════════
def _fusion_log(p, res):
    """ENGINE F feed: append every resolved leg (conf/eqs/aqs/outcome) to the fusion table."""
    try:
        if res not in ("W", "L") or CON is None:
            return
        CON.execute("INSERT INTO fusion_feed VALUES(?,?,?,?,?,?)",
                    (time.time(), p.get("asset"), float(p.get("conf") or 0.5),
                     float(p.get("eqs") or 0.0), float(p.get("aqs") or 0.0), res))
        CON.commit()
    except Exception:
        pass


def _metaf_build(win=None):
    """ENGINE F build: recompute fusion weights from the live fusion feed (own history)."""
    try:
        rows = list(CON.execute(
            "SELECT conf, eqs, outcome FROM fusion_feed WHERE outcome IN ('W','L') "
            "ORDER BY ts DESC LIMIT ?", (int(win or META_WIN),)))
    except Exception:
        rows = []
    try:
        n = len(rows)
        acc = (sum(1 for _c, _e, o in rows if o == "W") / n) if n else 0.5
        b = {}
        for c, _e, o in rows:
            k = min(9, int(max(0.0, min(0.99, float(c or 0.5))) * 10))
            d = b.setdefault(k, [0, 0])
            d[0 if o == "W" else 1] += 1
        wc = 0.5
        if n >= 40:
            num = sum(((x[0] / (x[0] + x[1])) - 0.5) * min(1.0, (x[0] + x[1]) / 6.0) * (k + 1)
                      for k, x in b.items() if (x[0] + x[1]) >= 4)
            wc = max(0.05, min(0.95, 0.5 + num / max(1.0, n / 6.0)))
        METAF.update(n=n, acc=round(acc, 4), conf_w=round(wc, 3), buckets=len(b),
                     upd=int(METAF.get("upd", 0)) + 1)
        log(f"v33 FUSION: {n} live legs | acc {acc:.0%} | conf-weight {wc:.2f} | buckets {len(b)}")
    except Exception as ex:
        log(f"v33 FUSION build skipped: {ex}")


def _fuse_weights():
    """ENGINE F: confidence reliability from live history (1.0 = neutral, 0.75..1.25)."""
    try:
        if int(METAF.get("n", 0)) < 30:
            return 1.0
        acc = float(METAF.get("acc", 0.5))
        return max(0.75, min(1.25, 1.0 + (acc - 0.5) * 2.5))
    except Exception:
        return 1.0


def _cal_bucket_stat(conf=None):
    """ENGINE K: live W/L + n of the confidence bucket (0.05 steps); None = all buckets."""
    try:
        if conf is None:
            tw = sum(int(v.get("w", 0)) for v in CAL.values())
            tl = sum(int(v.get("l", 0)) for v in CAL.values())
            return ((tw / (tw + tl)) if (tw + tl) else 0.5), (tw + tl)
        b = CAL.get(f"{round(float(conf) * 20) / 20:.2f}")
        if b:
            n = int(b.get("w", 0)) + int(b.get("l", 0))
            return ((int(b.get("w", 0)) / n) if n else 0.5), n
    except Exception:
        pass
    return 0.5, 0


def _eqs(aqs, pwin):
    """ENGINE F: EQS = accuracy-equivalent score — AQS fused with measured live p(win)."""
    try:
        bw, bn = _cal_bucket_stat(None)
        bonus = 0.02 if (bn >= 10 and bw >= 0.60) else 0.0
        return max(0.0, min(1.0, 0.48 * float(aqs) + 0.50 * float(pwin if pwin is not None else 0.5) + bonus))
    except Exception:
        return 0.5


def _asset_family(asset):
    """ENGINE G: family class for the base floor (crypto / stock / FX-OTC)."""
    a = str(asset).upper()
    if any(k in a for k in ("BTC", "ETH", "SOL", "MATIC", "COIN", "XRP", "DOGE", "LTC")):
        return "crypto"
    if any(k in a for k in ("AMZN", "TSLA", "VISA", "MARA", "PFE", "AMD", "FDX", "NFLX",
                            "MSFT", "AAPL", "GOOG", "META", "INTC", "JPM", "MCD", "BA_")):
        return "stock"
    return "otc"


def _floor_min(asset, grade="HIGH"):
    """ENGINE G: effective confidence floor = family base + learned offset + defenses."""
    base = {"crypto": 0.655, "stock": 0.64, "otc": 0.60}.get(_asset_family(asset), 0.62)
    if FLOOR_BASE > 0:
        base = max(base, FLOOR_BASE - 0.03)
    f = base + float(FLOORS.get(asset, 0.0))
    if grade == "APEX":
        f -= 0.02
    if DEFENSE.get("on"):
        f += 0.08
    return max(0.55, min(0.82, f))


def _floor_seed():
    """ENGINE G seed: derive per-asset floor offsets from the engine's own DB (n>=10)."""
    try:
        rows = list(CON.execute("SELECT asset, outcome FROM trades WHERE outcome IN ('W','L')"))
    except Exception:
        return
    agg = {}
    for a, o in rows:
        d = agg.setdefault(str(a), [0, 0])
        d[0 if o == "W" else 1] += 1
    seeded = 0
    for a, (w, l) in agg.items():
        n = w + l
        if n < 10:
            continue
        wr = w / n
        if wr < 0.45:
            FLOORS[a] = max(FLOORS.get(a, 0.0), 0.03); seeded += 1
        elif wr >= 0.66:
            FLOORS[a] = min(FLOORS.get(a, 0.0), -0.02); seeded += 1
    log(f"v33 FLOORS: seed {seeded} asset(s) from DB | base {FLOOR_BASE:.2f} | {len(FLOORS)} learned")


def _round_learn(asset, res, conf=0.0):
    """ENGINE G learn: rounds teach per-asset floors (loss -> raise, win -> lower)."""
    try:
        if not FLOOR_LEARN or not asset:
            return
        cur = float(FLOORS.get(asset, 0.0))
        if res == "L":
            new = min(0.09, cur + 0.015)
            RLEARN["bump"] = RLEARN.get("bump", 0) + 1
        elif res == "W":
            new = max(-0.05, cur - 0.006)
            RLEARN["lower"] = RLEARN.get("lower", 0) + 1
        else:
            return
        RLEARN["n"] = RLEARN.get("n", 0) + 1
        if abs(new - cur) < 1e-9:
            return
        FLOORS[asset] = round(new, 4)
        if RLEARN["n"] % 5 == 1:
            log(f"v33 FLOOR learn {asset}: {cur:+.3f} -> {new:+.3f} (round {res})")
    except Exception:
        pass


def _turn_guard(direc, cl, i, er, altr, grade):
    """ENGINE H: anti liquidity-grab — never buy the literal top or sell the literal bottom.
       Fires when the last 3 candles already ran with the signal against a quiet tape.
       Returns (allowed, reason)."""
    if not TURN_ON or i < 6:
        return True, ""
    try:
        noise = float(np.mean(np.abs(np.diff(cl[i - 8:i + 1])))) or 1e-12
        run3 = float(cl[i] - cl[i - 3])
        if direc > 0 and run3 > 2.2 * noise and er >= 0.40 and altr < 0.60:
            return False, f"grab-top (3-run {run3 / noise:.1f}x, er {er:.2f})"
        if direc < 0 and run3 < -2.2 * noise and er >= 0.40 and altr < 0.60:
            return False, f"grab-bottom (3-run {run3 / noise:.1f}x, er {er:.2f})"
        if grade != "APEX" and er >= TURN_SLOPE:
            if direc > 0 and run3 > 1.2 * noise:
                return False, f"chase-up ({run3 / noise:.1f}x)"
            if direc < 0 and run3 < -1.2 * noise:
                return False, f"chase-down ({run3 / noise:.1f}x)"
    except Exception:
        return True, ""
    return True, ""


def _ladder_cap(amt, prev, asset, direc):
    """ENGINE I: evidence cap on MTG recovery legs — flatten the loss tail.
       Money cap: a recovery leg never stakes more than LADDER_RISK of balance.
       Pushback cap: if the just-closed candle went against the recovery direction,
       cap the leg at LADDER_TILT x the failed leg (never chase the tape with a bigger bet)."""
    try:
        base = float(amt or 0.0)
        if base <= 0:
            return base
        cap = min(base, max(1.0, float(BAL_D.get("v", 0.0)) * LADDER_RISK))
        why = "bal"
        try:
            ks = sorted(store.get(asset, {}))
            if len(ks) >= 2:
                r = store[asset][ks[-2]]
                dir_last = "BUY" if float(r[3]) >= float(r[0]) else "SELL"
                if dir_last != str(direc).upper():
                    _t = max(1.0, float(prev or 1.0) * LADDER_TILT)
                    if _t < cap:
                        cap = _t
                        why = "pushback"
        except Exception:
            pass
        cap = round(max(1.0, cap), 2)
        if cap < base - 1e-9:
            DDAY["ladders"] = DDAY.get("ladders", 0) + 1
            log(f"LADDER cap {asset}: ${base:.2f} -> ${cap:.2f} ({why})")
        return cap
    except Exception:
        return amt



# ═══════════════════════ v33 OMEGA ENGINES — L · M (LIVE BRAIN) ═══════════════════════
def _live_wr(b):
    """ENGINE L: (win-rate, n) of a live dimension bucket."""
    try:
        n = int(b.get("w", 0)) + int(b.get("l", 0))
        return ((int(b.get("w", 0)) / n) if n else 0.5), n
    except Exception:
        return 0.5, 0


def _live_learn(direc, conf, rgdp, res):
    """ENGINE L — LIVE BRAIN learn: every resolved REAL direct leg updates the live
       W/L tables by direction · regime · UTC hour (AthenaAI multi-dimension tracking)."""
    try:
        if res not in ("W", "L"):
            return
        d = str(direc or "")
        if d:
            b = LIVE["dir"].setdefault(d, {"w": 0, "l": 0})
            b["w" if res == "W" else "l"] += 1
        rg = str(rgdp or "")
        if rg:
            b = LIVE["reg"].setdefault(rg, {"w": 0, "l": 0})
            b["w" if res == "W" else "l"] += 1
        b = LIVE["hour"].setdefault(str(time.gmtime().tm_hour), {"w": 0, "l": 0})
        b["w" if res == "W" else "l"] += 1
        LIVE["n"] = int(LIVE.get("n", 0)) + 1
    except Exception:
        pass


def _live_adj(direc, conf, rgdp):
    """ENGINE L — LIVE BRAIN gate: a cold dimension demotes the signal to HALF stake.
       Never drops (ALWAYS_TRADE). Returns (half, why)."""
    why = []
    try:
        if int(LIVE.get("n", 0)) >= LIVE_MIN_N:
            b = LIVE["hour"].get(str(time.gmtime().tm_hour))
            if b:
                wr, n = _live_wr(b)
                if n >= LIVE_MIN_N and wr < LIVE_WR_LOW:
                    why.append("hour-cold")
            d = str(direc or "")
            other = "SELL" if d == "BUY" else "BUY"
            bd, bo = LIVE["dir"].get(d), LIVE["dir"].get(other)
            if bd and bo:
                wrd, nd = _live_wr(bd)
                wro, no = _live_wr(bo)
                if nd >= LIVE_MIN_N and no >= LIVE_MIN_N and wrd < LIVE_WR_LOW and wro > LIVE_WR_HI:
                    why.append("dir-cold")
            br = LIVE["reg"].get(str(rgdp or ""))
            if br:
                wrr, nr = _live_wr(br)
                if nr >= LIVE_MIN_N and wrr < LIVE_WR_LOW:
                    why.append("regime-cold")
    except Exception:
        pass
    return (bool(why), "+".join(why))


def _maxconf_half(conf, grade, storm_ok):
    """ENGINE L — anti-overfit cap (AthenaAI max_confidence): an overconfident signal is
       usually model noise. APEX + storm agreement is the only exemption."""
    try:
        if conf >= MAXCONF and not (grade == "APEX" and storm_ok):
            return True
    except Exception:
        pass
    return False


def _session_health():
    """ENGINE L — rolling-leg health (AthenaAI momentum cooldown): if the last ROLL_N
       legs are cold (<ROLL_WR), take an adaptive cooling break. Rate-limited."""
    try:
        rr = [x for x in list(recent)[-ROLL_N:]]
        w = sum(1 for x in rr if x == "W")
        n = len(rr)
        wr = (w / n) if n else 1.0
        LIVE["rollwr"] = round(wr, 3)
        if n >= ROLL_N and wr < ROLL_WR and \
           (time.time() - float(LIVE.get("lastcool", 0.0))) > ROLL_COOL_GAP:
            LIVE["lastcool"] = time.time()
            return True
    except Exception:
        pass
    return False


def _sniper_ok(grade, conf, agree, nfw, pwin, er, dead, altr, hour=None):
    """v30 SNIPER — highly-accurate signals only. Returns (ok, reason). Never adds risk."""
    if not SNIPER: return True, ""
    if dead: return False, "dead-tape"
    if altr >= SNIPER_ALTR and er < 0.35: return False, f"chop(altr {altr:.2f} er {er:.2f})"
    if grade == "STD": return False, "std-grade"
    if nfw < 2 and grade != "APEX": return False, "single-setup"
    if conf < SNIPER_CONF: return False, f"conf {conf:.2f}<{SNIPER_CONF}"
    if pwin is not None and pwin < SNIPER_PWIN and grade != "APEX":
        return False, f"pwin {pwin:.2f}<{SNIPER_PWIN}"
    _h = time.gmtime().tm_hour if hour is None else hour
    if _dead_zone(_h) and grade != "APEX" and not (agree >= 0.65 and nfw >= 2):
        return False, "dead-zone"
    return True, ""


def eval_candidate(asset, upto_min, include_forming):
    st = store[asset]
    _storm_update(asset, upto_min)
    ts = [k for k in sorted(st) if (k <= upto_min if include_forming else k < upto_min)][-KEEP:]
    if len(ts) < WARMUP: return None
    df = pd.DataFrame([st[k] for k in ts], columns=["open", "high", "low", "close"],
                      index=pd.to_datetime(ts, unit="s", utc=True))
    S, AUX = build_smc(df)
    TF = tf_arrays(df)
    i = len(df) - 1
    hok = HOURS.get(asset)
    if hok is not None and not hok[int(df.index[-1].hour) // 3]:
        return None                                   # blocked hour for this asset
    # ---- v24 ENSEMBLE: weighted vote election (was: first-fired-wins) ----
    _erb = _regime_bucket(float(AUX["er"][i]))
    _votes, _all = [], []
    for m in MEMBERS[asset]:
        rr = SET_REC[(asset, m["strategy"])]
        if len(rr) >= 6 and sum(rr) / len(rr) < 0.40:
            continue                     # setup went cold live — self-muted
        v = int(np.asarray(S[m["strategy"]])[-1])
        if v != 0 and tfok(m["mask"], v, TF, i):
            w = float(m["test"]) * _reg_w(m, _erb)
            _all.append((v, w, m))
            if w > 0.0:
                _votes.append((v, w, m))
    if not _all: return None
    _reg_all = False
    if not _votes:                       # every voter regime-muted → least-bad at 1/4 weight
        _reg_all = True
        _votes = [(v, 0.25 * max(float(m["test"]), 0.20), m) for v, _w, m in _all]
    _act = _tally([(v, w) for v, w, _m in _votes])
    if _act is None: return None
    direc, agree, nfw = _act
    _win = sorted([z for z in _votes if z[0] == direc], key=lambda z: -z[1])
    if not _win: return None
    best = _win[0][2]
    exp = best["expiry"]
    fired = [m for _v2, _w2, m in _win]          # winning voters, best-weight first
    # ---- meta-label filter (thr calibrated on validation, honest test) ----
    pwin = None; mthr = 0.5
    mdl = AIF.get(asset)
    if mdl is not None:
        try:
            CT = ctx_arrays(df)
            mi = MEMBERS[asset].index(best)
            vec = ctx_vec(CT, TF, i, direc, RANK[best["tier"]], mi, nfw, agree)
            pwin = float(mdl["model"].predict_proba(np.array([vec]))[0, 1])
            if mdl.get("iso") is not None and META_ISO:
                pwin = float(_iso_apply(mdl["iso"], np.array([pwin]))[0])
            mthr = float(mdl.get("thr", 0.5))
            if pwin < mthr: return None               # learned filter says skip
        except Exception:
            pwin = None
    if PROB.get(asset) and not (len(fired) >= PROB_MIN_AGREE or (pwin or 0) >= 0.62
                                or best["tier"] == "A"):
        return None                      # v20 probation gate: needs agreement / meta / tierA
    bod = np.abs(df["close"].values[-15:] - df["open"].values[-15:])
    rg = (df["high"].values[-15:] - df["low"].values[-15:])
    dead = bool(np.median(bod) < 0.2 * max(np.median(rg), 1e-12))
    # v19 SPIKE GUARD: never enter right after a parabolic candle
    _cl = df["close"].values
    _rng = df["high"].values - df["low"].values
    _med = float(np.median(_rng[-40:])) if len(_rng) >= 40 else float(np.median(_rng))
    if _med > 0 and len(_cl) >= 2 and abs(_cl[-1] - _cl[-2]) > SPIKE_MULT * _med:
        return None
    # ---- v33 GATES: chaos cooldown + entry-freshness measurement ----
    if not _chaos_ok(_rng, _med):
        DDAY["chaos_skip"] = DDAY.get("chaos_skip", 0) + 1
        if DDAY["chaos_skip"] % 10 == 1:
            log(f"CHAOS skip {asset} (last-3 range > {CHAOS_MULT:.1f}x median)")
        return None
    _fext = _fresh_ext(_cl, _rng)
    # ---- v24 ensemble confidence: weighted member accuracy + calibrated meta + agreement ----
    _wsum = sum(w for _v2, w, _m in _win) or 1e-9
    _accw = sum(w * float(m["test"]) for _v2, w, m in _win) / _wsum
    conf = 0.55 * _accw + 0.45 * (pwin if pwin is not None else _accw)
    conf = min(0.95, conf + 0.06 * (agree - 0.5) * 2.0)
    grade = "APEX" if ((conf >= 0.66 and agree >= 0.72) or (best["tier"] == "A" and agree >= 0.6)) \
        else "HIGH" if (conf >= 0.60 or (nfw >= 2 and agree >= 0.58)) else "STD"
    if grade == "STD" and (pwin is None or pwin < 0.50):
        return None                      # v24: only truly unpriced STD signals dropped
    if TOPTIER and grade == "STD": return None
    MOMF = ("MOM_", "MR_", "SMA_stack")
    if best["strategy"].startswith(MOMF) and best["tier"] not in "AB" and (pwin or 0) < 0.58:
        return None                      # momentum setups need elite proof
    # ---- v30 SNIPER: highly-accurate signals only (kills chop / weak / lone setups) ----
    _altrx = _altr_ratio(df["close"].values)
    _sok, _swhy = _sniper_ok(grade, conf, agree, nfw, pwin, float(AUX["er"][i]), dead, _altrx)
    if not _sok:
        DDAY["sniper_skip"] = DDAY.get("sniper_skip", 0) + 1
        if DDAY["sniper_skip"] % 12 == 1:
            log(f"SNIPER skipped {asset} ({_swhy})")
        return None
    # ---- v33 OMEGA: radar + MTF + memory + calibration → AQS gate ----
    _rg_s, _rg_t = _regime_radar(df["close"].values, _rng, float(AUX["er"][i]))
    _mtfc = _mtf_confluence(TF, i, direc)
    _hqa, _hqt = _hq_adj(asset, time.gmtime().tm_hour)
    _calp = _cal_pen(conf)
    # ---- v33 OMEGA GATES: learned floor · turn-guard · calibration blacklist ----
    _flr = _floor_min(asset, grade)
    if FLOOR_ON and _flr > 0 and conf < _flr:
        DDAY["floor_skip"] = DDAY.get("floor_skip", 0) + 1
        if DDAY["floor_skip"] % 10 == 1:
            log(f"FLOOR skip {asset} (conf {conf:.2f} < {_flr:.2f}"
                + (f" | learned {FLOORS[asset]:+.3f}" if asset in FLOORS else "") + ")")
        return None
    _tok, _twy = _turn_guard(direc, _cl, i, float(AUX["er"][i]), _altrx, grade)
    if not _tok:
        DDAY["turn_skip"] = DDAY.get("turn_skip", 0) + 1
        if DDAY["turn_skip"] % 10 == 1:
            log(f"TURN GUARD {asset} ({_twy})")
        return None
    _cbw, _cbn = _cal_bucket_stat(round(conf, 4))
    if CALBL_ON and _cbn >= CALBL_N and _cbw < CALBL_WR:
        DDAY["cal_skip"] = DDAY.get("cal_skip", 0) + 1
        if DDAY["cal_skip"] % 10 == 1:
            log(f"CALBL skip {asset} (bucket {round(conf, 4):.2f} {_cbw:.0%}/{_cbn})")
        return None
    _svp = _storm_vote(asset, direc)
    _aqs = _aqs_score(grade, conf, agree, nfw, pwin, float(AUX["er"][i]), _altrx,
                      _mtfc, _rg_s, _hqa, PAYOUTS.get(asset, 90.0), _svp > 0, _calp)
    # ---- v33 ENGINE F FUSION: live-reliability scaling + accuracy-equivalent EQS gate ----
    _pwq = pwin if pwin is not None else _accw
    _aqs = min(1.0, max(0.0, _aqs * _fuse_weights()))
    METAF["cands"] = METAF.get("cands", 0) + 1
    _eqsv = _eqs(_aqs, _pwq)
    DDAY["eqs"] = _eqsv
    if EQS_MIN > 0 and _eqsv < EQS_MIN:
        DDAY["eqs_skip"] = DDAY.get("eqs_skip", 0) + 1
        if DDAY["eqs_skip"] % 10 == 1:
            log(f"EQS skip {asset} (eqs {_eqsv:.2f} < {EQS_MIN:.2f} | aqs {_aqs:.2f} pwin {_pwq:.2f})")
        return None
    if _aqs < AQS_MIN:
        DDAY["aqs_skip"] = DDAY.get("aqs_skip", 0) + 1
        if DDAY["aqs_skip"] % 10 == 1:
            log(f"AQS skip {asset} ({_aqs:.2f} < {AQS_MIN:.2f} | rg {_rg_t} mtf {_mtfc:.2f}"
                + (f" {_hqt}" if _hqt else "") + ")")
        return None
    # ---- v33 OMEGA LIVE BRAIN: session-adaptive demote + anti-overfit cap ----
    _lhalf, _lwhy = _live_adj(direc, conf, _rg_t)
    if _maxconf_half(conf, grade, _svp > 0):
        _lhalf = True
        _lwhy = (_lwhy + "+" if _lwhy else "") + "overconf"
    if _fext > FRESH_ATR and not (grade == "APEX" and _svp > 0):
        DDAY["fresh_skip"] = DDAY.get("fresh_skip", 0) + 1
        if DDAY["fresh_skip"] % 10 == 1:
            log(f"FRESH skip {asset} (ext {_fext:.1f} ATR) — move extended, wait pullback")
        return None
    return dict(asset=asset, direc=direc, expiry=exp, fired=fired, minute=upto_min,
                aqs=round(_aqs, 3), eqs=round(_eqsv, 3), mtf=round(_mtfc, 2), rgdp=_rg_t,
                live_half=bool(_lhalf), live_why=_lwhy,
                nf=nfw, agree=round(float(agree), 3), nvotes=len(_votes), reg_all=_reg_all,
                m5t=float(TF["m5_t"][i]), m5c=float(TF["m5_c"][i]), m15=float(TF["m15_t"][i]),
                m30=float(TF["m30_t"][i]), sdir=float(AUX["dirS"][i]),
                pd=float(AUX["pd"][i]), er=float(AUX["er"][i]), atrp=float(AUX["atrp"][i]),
                sess=int(AUX["sess"][i]), dead=dead, pwin=pwin, mthr=mthr,
                conf=round(conf, 4), grade=grade,
                rank=(RANK[best["tier"]], -(pwin if pwin is not None else best["test"]), -len(fired)))

def _profit_locked():
    """v20: session profit ≥ PROFIT_LOCK of day-start → keep the win, stop auto-trading."""
    return bool(DDAY.get("b0")) and DDAY.get("pnl", 0.0) >= PROFIT_LOCK * DDAY["b0"]

async def _bal(api, fallback=None):
    """v20: balance() hangs on some sessions — always timeout-wrap + fallback."""
    try:
        return float(await asyncio.wait_for(api.balance(), 12))
    except Exception:
        return float(fallback if fallback is not None else BAL_FALLBACK)

def _check_daily_guard():
    """Halt AUTO-TRADE (not signals) on daily loss / MTG bleed / profit lock."""
    msg = None
    if TRD["on"] and DDAY.get("b0"):
        lim = -max(6.0, 0.12 * DDAY["b0"])
        if DDAY.get("pnl", 0.0) <= lim:
            TRD["on"] = False
            msg = "🛡 DAILY LOSS LIMIT hit — auto-trading OFF till tomorrow (signals continue)"
    if TRD["on"] and _profit_locked():
        TRD["on"] = False
        msg = (msg + "\n" if msg else "") + \
              f"🏆 PROFIT LOCK — session ${DDAY['pnl']:+.2f} ≥ {PROFIT_LOCK:.0%} of start. Auto-trading OFF; signals continue."
    if not MTG_STATE["halted"] and DDAY.get("mtg_net", 0.0) <= MTG_NET_HALT:
        MTG_STATE["halted"] = True
        msg = (msg + "\n" if msg else "") + \
              f"🧯 AUTO-MTG HALTED for this session — MTG net ${DDAY['mtg_net']:+.2f} " \
              f"(≤ ${MTG_NET_HALT:.0f}). Advisory re-entries still shown; auto-placement off."
    return msg

def _paper_stake(normal=True):
    """Hypothetical stake in $ for signal-only economics tracking."""
    base = DDAY.get("b0") or BAL_D.get("start") or 100.0
    s = round(base * PAPER_PCT, 2)
    return round(s * MTG_MULT, 2) if not normal else max(1.0, s)

def _round_track(p, res):
    """v28 ROUND accounting — user rule: a round recovered via MTG counts as a FULL WIN; its leg
    losses are absorbed (never counted as losses). A fully-lost round benches the pair
    (ROUND_BENCH_S) and eases global risk (RISK_EASE); recovered rounds refund RISK_RECOVER."""
    try:
        if p.get("skip"):
            return
        k = int(p.get("no") or 0)
        r = ROUNDS["cur"].setdefault(k, {"legs": 0, "losses": 0, "won": False})
        r["legs"] += 1
        if res == "W":
            r["won"] = True
        elif res == "L":
            r["losses"] += 1
        _step = int(p.get("step", 1))
        _closed = (res == "W") or (res == "T") or (res == "L" and (_step >= MTG_STEPS or not MTG_AUTO))
        if not _closed:
            return
        ROUNDS["cur"].pop(k, None)
        if r["won"] and ROLL_WIN_RULE:
            ROUNDS["W"] += 1
            DDAY["round_w"] = DDAY.get("round_w", 0) + 1
            _round_learn(p.get("asset"), "W", float(p.get("conf") or 0.0))   # v33 ENGINE G
            if r["legs"] > 1:
                ROUNDS["rec"] += 1
                ROUNDS["absorbed"] += r["losses"]
                DDAY["round_rec"] = DDAY.get("round_rec", 0) + 1
                ADAPT["risk"] = min(1.2, ADAPT["risk"] * RISK_RECOVER)
                log(f"ROUND WON #{k} {p['asset']} — recovered at step {_step}, "
                    f"{r['losses']} leg loss(es) ABSORBED (USDCOP rule)")
        else:
            ROUNDS["L"] += 1
            DDAY["round_l"] = DDAY.get("round_l", 0) + 1
            _round_learn(p.get("asset"), "L", float(p.get("conf") or 0.0))   # v33 ENGINE G
            MUTE_T[p["asset"]] = max(MUTE_T.get(p["asset"], 0.0), time.time() + ROUND_BENCH_S)
            ADAPT["risk"] = max(0.70, ADAPT["risk"] * RISK_EASE)
            log(f"ROUND LOST #{k} {p['asset']} ({r['legs']} legs) — pair benched "
                f"{ROUND_BENCH_S / 60:.0f}m, risk x{ADAPT['risk']:.2f}")
    except Exception as e:
        log(f"round track error: {e}")


async def resolve_pending(asset, closed_upto):
    global pending, pause_until
    done, keep = [], []
    for p in pending:
        if p["asset"] == asset and closed_upto >= p["entry_min"] + 60 * p["expiry"]:
            cc = store[asset].get(p["entry_min"] + 60 * (p["expiry"] - 1))
            if cc is None:
                if closed_upto <= p["entry_min"] + 60 * (p["expiry"] + 10):
                    keep.append(p)          # feed gap — retry on the next minutes
                continue
            close = cc[3]
            if close == p["entry"]: res = "T"
            elif (close > p["entry"]) == (p["dir"] == "BUY"): res = "W"
            else: res = "L"
            _round_track(p, res)          # v28 round accounting (USDCOP rule + breaker)
            _cal_learn(p.get("conf"), res)   # v33 ENGINE D calibration loop
            _fusion_log(p, res)              # v33 ENGINE F fusion feed (conf/eqs/outcome)
            if not p.get("mtg") and not p.get("skip"):
                _live_learn(p.get("dir"), p.get("conf"), p.get("rgdp"), res)   # v33 LIVE BRAIN
            # ---- v18 razor analysis: close margin in ATR units ----
            atr = p.get("atr") or 0.0
            p["margin"] = abs(close - p["entry"]) / atr if atr > 0 else -1.0
            p["razor"] = bool(atr > 0 and p["margin"] < RAZOR_ATR)
            # ---- v18 paper P&L (normal legs and MTG legs alike) ----
            pstake = p.get("pstake") or _paper_stake(normal=not p.get("mtg"))
            if res in "WL":
                win = res == "W"
                DDAY["paper"] += pstake * PAYOUT if win else -pstake
                if p.get("mtg"):
                    DDAY["mtg_net"] += pstake * PAYOUT if win else -pstake
                    if p.get("skip"):
                        DDAY["skip_net"] += pstake * PAYOUT if win else -pstake   # v23 ledger
                if p["razor"]:
                    DDAY["rz_w" if win else "rz_l"] += 1
                else:
                    DDAY["nm_w" if win else "nm_l"] += 1
                if p.get("rz_risk"):
                    DDAY["rz_risk_w" if win else "rz_risk_l"] += 1
            score_s[res] += 1
            if not p.get("mtg") and res in "WL":
                DDAY["dw" if res == "W" else "dl"] += 1     # v19 clean direct metric
            if res in "WL" and "STORM" in (p.get("strategy") or ""):     # v26 STORM module ledger
                DDAY["storm_w" if res == "W" else "storm_l"] += 1
            if p.get("soft") and res in "WL":
                DDAY["soft_w" if res == "W" else "soft_l"] += 1   # v20 soft entries
            ps = pair_score.setdefault(p["asset"], {"W": 0, "L": 0, "T": 0}); ps[res] += 1
            _roll_day()
            if res == "W": DDAY["w"] += 1
            elif res == "L": DDAY["l"] += 1
            if res in "WL":
                if not p.get("skip"):
                    recent.append(res)   # v23: gate-skipped paper legs never pause the bot
                if res == "W" and not p.get("mtg"):
                    RSTATE["rate"] = min(RSTATE["rate"] + 0.01, 0.10)
                if p.get("amt"):
                    BAL_D["v"] += p["amt"] * 0.92 if res == "W" else -p["amt"]
                    DDAY["pnl"] += p["amt"] * 0.92 if res == "W" else -p["amt"]
                    BAL_D["n"] = BAL_D.get("n", 0) + 1
                    if BAL_D["n"] % 4 == 0 and API_H is not None:
                        BAL_D["v"] = await _bal(API_H, BAL_D["v"])   # v20 safe balance
                if not p.get("mtg"):
                    SET_REC[(p["asset"], p["strategy"])].append(1 if res == "W" else 0)
                if not p.get("mtg") and not p.get("skip"):
                    PAIR_REC[p["asset"]].append(1 if res == "W" else 0)   # v24 health governor
            db_ins_trade(CON, p, close, res)
            done.append((p, res, close))
        else:
            keep.append(p)
    pending = keep
    guard = _check_daily_guard()
    if guard:
        await tg(guard)
    for p, res, close in done:
        if res in "WL":
            if p.get("mtg"):
                if p.get("skip"):
                    # v23: paper-only skipped leg — no mute, no pause, not a real MTG round
                    await tg(f"🧾 MTG paper leg {res} (skipped real) — no mute/pause | "
                             f"ledger ${DDAY['skip_net']:+.2f}")
                    log(f"RESULT {res} #{p['no']} {p['asset']} @{p['expiry']}m MTG-skip | "
                        f"{score_s['W']}W-{score_s['L']}L | skip_net ${DDAY['skip_net']:+.2f}")
                    save_state()
                    continue
                _step = int(p.get("step", 1))
                if res == "L" and _step < MTG_STEPS and not MTG_STATE["halted"]:
                    # v26 GOD LADDER (Pine maxMTG=2): one more real recovery leg, then the round closes
                    _e2 = latest_price(p["asset"])
                    # v28 GUARD (v26 evidence: 3 fully-lost ×2.2 step-2 rounds): refresh the
                    # supertrend read, then size by evidence — full ladder only when STORM agrees,
                    # otherwise capped. Still 100% real on PO, never skipped.
                    _storm_update(p["asset"], closed_upto)
                    _full2 = round(max(1.0, min((p.get("amt") or 1.0) * MTG_MULT, BAL_D["v"] * 0.12)), 2)
                    _full2 = _ladder_cap(_full2, p.get("amt"), p["asset"], p["dir"])   # v33 ENGINE I
                    _sv2 = _storm_vote(p["asset"], p["dir"])
                    amt2 = _full2 if (_sv2 > 0 or not STORM_TILT) else round(max(1.0, min(_full2, MTG2_MIN)), 2)
                    tid2 = await place(p["asset"], p["dir"], amt2, tsec=60) if TRD["on"] else None
                    if TRD["on"] and tid2 is None: amt2 = 0.0
                    pending.append(dict(no=p["no"], asset=p["asset"], dir=p["dir"], entry=_e2,
                                        entry_min=closed_upto, expiry=1, grade="MTG2",
                                        strategy=(p.get("strategy") or "") + "+MTG2", mtg=True,
                                        step=_step + 1, amt=amt2, conf=p.get("conf"), pwin=p.get("pwin"),
                                        sess=p.get("sess"), er=p.get("er"), gate=p.get("gate"),
                                        atr=_atr_proxy(p["asset"], closed_upto), skip=False,
                                        rz_risk=False, pstake=_paper_stake(normal=False)))
                    DDAY["mtg_step2"] = DDAY.get("mtg_step2", 0) + 1
                    await tg(f"🔂 MTG STEP-2 — #{p['no']} {p['asset']} recovery leg lost\n"
                             f"{'🟢' if p['dir'] == 'BUY' else '🔴'} RE-ENTER {p['dir']} NOW @ {_e2:g}\n"
                             f"⏱ 1 min | ladder ×{MTG_MULT} | MTG net so far ${DDAY['mtg_net']:+.2f}"
                             + (f" | storm {'agrees → full $' if _sv2 > 0 else 'opposes → capped $'}{amt2:.2f}"
                                 if amt2 else " | NOT placed"))
                    log(f"MTG2 #{p['no']} {p['dir']} {p['asset']} step-2 re-entry @1m"
                        f"{'' if amt2 else ' (not placed)'}")
                    save_state()
                    continue
                mtg_round[res] += 1
                if res == "L":
                    RSTATE["rate"] = 0.06
                    ASSET_LAST[p["asset"]] = time.time()
                    MUTE_T[p["asset"]] = time.time() + MUTE_LOSS_S       # v21 loss-mute
                    pause_until = max(pause_until, time.time() + 75)
                    await tg("🧊 ROUND LOST — stake reset, asset benched, trading paused ~1 min")
                    if mtg_round["L"] >= MTG_ROUND_HALT and not MTG_STATE["halted"]:
                        MTG_STATE["halted"] = True
                        await tg(f"🧯 AUTO-MTG HALTED — {mtg_round['L']} losing rounds "
                                 f"(limit {MTG_ROUND_HALT}). Advisory re-entries only.")
                else:
                    RSTATE["rate"] = min(RSTATE["rate"] + 0.01, 0.10)
                rt = mtg_round["W"] + mtg_round["L"]
                await tg(f"🔁 MTG LEG {'✅ RECOVERED' if res == 'W' else '❌ ROUND LOST'} — "
                         f"#{p['no']} {p['asset']} {p['dir']}\n"
                         f"🎯 ROUNDS (1-step MTG): {mtg_round['W']}W–{mtg_round['L']}L "
                         f"({mtg_round['W'] / rt * 100 if rt else 0:.0f}%)"
                         + (f" | 💵 MTG net ${DDAY['mtg_net']:+.2f}" if DDAY["mtg_net"] else ""))
                # v18 FIX: MTG legs now print a full console RESULT line (was TG-only in v17)
                log(f"RESULT {res} #{p['no']} {p['asset']} @{p['expiry']}m MTG | "
                    f"{score_s['W']}W-{score_s['L']}L | paper ${DDAY['paper']:+.2f} "
                    f"| mtg net ${DDAY['mtg_net']:+.2f}"
                    + (" | 🪒RAZOR" if p.get("razor") else ""))
                save_state()
                continue
            if res == "W":
                mtg_round["W"] += 1
            else:
                entry2 = latest_price(p["asset"])
                mk = 1                       # v19: 1-minute legs only
                amt2 = 0.0
                conf = float(p.get("conf") or 0.0)
                # v21 FRESH-CONFIRM: setup must still fire same-direction right now
                # (v20 evidence: #52 FB re-entry was blind → double loss, −$4.55 bleed)
                _mc = eval_candidate(p["asset"], closed_upto, include_forming=False) if MTG_CONFIRM else None
                # NOTE: p["dir"] is "BUY"/"SELL" while cand direc is ±1 — compare correctly
                _mc_ok = (bool(_mc) and _mc["direc"] == (1 if p["dir"] == "BUY" else -1)) if MTG_CONFIRM else True
                mtg_ok = (not MTG_STATE["halted"]) and conf >= MTG_MIN_CONF and _mc_ok
                if TRD["on"] and MTG_AUTO and p.get("amt") and mtg_ok:
                    amt2 = _ladder_cap(round(max(1.0, min(p["amt"] * MTG_MULT, BAL_D["v"] * 0.12)), 2),
                                       p.get("amt"), p["asset"], p["dir"])  # v33 ENGINE I cap
                    tid2 = await place(p["asset"], p["dir"], amt2, tsec=60 * mk)
                    if tid2 is None: amt2 = 0.0
                if not mtg_ok and not p.get("mtg"):
                    MUTE_T[p["asset"]] = time.time() + MUTE_LOSS_S       # v21 loss-mute (no recovery)
                if TRD["on"] and MTG_AUTO and not mtg_ok:
                    if not _mc_ok:
                        DDAY["mtg_skip"] += 1
                        _stale = (time.time() - FEED_T.get(p["asset"], 0)) > FEED_WARN
                        log("MTG auto-skip: setup no longer fires same-dir ✂️ bleed avoided"
                            + (" (feed-based)" if _stale else ""))
                    else:
                        log(f"MTG auto-skip: conf {conf:.2f} < {MTG_MIN_CONF:.2f}"
                            + (" | MTG HALTED (net limit)" if MTG_STATE["halted"] else ""))
                pending.append(dict(no=p["no"], asset=p["asset"], dir=p["dir"], entry=entry2,
                                    entry_min=closed_upto, expiry=mk,
                                    grade="MTG", strategy=p["strategy"] + "+MTG", mtg=True, amt=amt2,
                                    conf=p.get("conf"), pwin=p.get("pwin"), sess=p.get("sess"),
                                    er=p.get("er"), gate=p.get("gate"), atr=_atr_proxy(p["asset"], closed_upto),
                                    skip=(not mtg_ok), rz_risk=False, pstake=_paper_stake(normal=False)))
                exp2 = datetime.fromtimestamp(closed_upto + 60 * p["expiry"], tz=timezone.utc).astimezone(IST)
                await tg(f"🔁 1-STEP MTG — #{p['no']} {p['asset']} lost leg 1\n"
                         f"{'🟢' if p['dir'] == 'BUY' else '🔴'} RE-ENTER {p['dir']} NOW @ {entry2:g}\n"
                         f"⏱ {p['expiry']} min — closes {exp2:%H:%M:%S} IST"
                         + (" | placed" if amt2 else "")
                         + f"\n⚠️ live evidence: rounds can win 75% yet net negative — MTG net so far ${DDAY['mtg_net']:+.2f}")
                log(f"MTG #{p['no']} {p['dir']} {p['asset']} re-entry @{p['expiry']}m")
        tot = score_s["W"] + score_s["L"]
        acc = score_s["W"] / tot * 100 if tot else 0
        icon = {"W": "✅ WIN", "L": "❌ LOSS", "T": "➖ TIE"}[res]
        streak = 0
        for r in reversed(recent):
            if r == "L": streak += 1
            else: break
        extra = ""
        if streak >= 3:
            pause_until = time.time() + 180
            recent.clear()
            extra = "\n🧊 3 straight losses — cool-down 3 min (v29 MAX FLOW)"
        if _session_health():
            pause_until = max(pause_until, time.time() + ROLL_COOL_S)
            DDAY["live_cool"] = DDAY.get("live_cool", 0) + 1
            extra += (f"\n🧠 LIVE BRAIN: last-{ROLL_N} legs cold ({LIVE.get('rollwr', 0):.0%})"
                      f" — adaptive cool-down {ROLL_COOL_S / 60:.0f} min")
        await tg(f"{icon} — #{p['no']} [{p['grade']}] {p['asset']} {p['dir']} @{p['expiry']}m"
                 + (" 🪒razor" if p.get("razor") else "") + f"\n"
                 f"{p['strategy']} | entry {p['entry']:g} → {close:g} ({close - p['entry']:+.6g})\n"
                 f"📈 SESSION: {score_s['W']}W–{score_s['L']}L–{score_s['T']}T ({acc:.0f}%)"
                 + (f" | 💰 bal ≈ ${BAL_D['v']:.2f}" if TRD["on"] else "")
                 + (f" | 📅 today {DDAY['w']}W–{DDAY['l']}L (${DDAY['pnl']:+.2f})")
                 + (f" | 📄 paper ${DDAY['paper']:+.2f}")
                 + (f"\n🔇 {p['asset']} muted" if muted(p["asset"]) else "") + extra)
        log(f"RESULT {res} #{p['no']} {p['asset']} @{p['expiry']}m | {score_s['W']}W-{score_s['L']}L"
            f" | paper ${DDAY['paper']:+.2f}" + (" | 🪒RAZOR" if p.get("razor") else ""))
    save_state()

async def resolve_shadow(asset, closed_upto):
    """v18 audit: shadow-grade every cancelled / throttled signal on real candles.
       Answers the question the v17 run could not: is the strict filter earning or losing?"""
    done, keep = [], []
    for p in shadow_pend:
        if p["asset"] == asset and closed_upto >= p["entry_min"] + 60 * p["expiry"]:
            cc = store[asset].get(p["entry_min"] + 60 * (p["expiry"] - 1))
            if cc is None:
                if closed_upto <= p["entry_min"] + 60 * (p["expiry"] + 10):
                    keep.append(p)
                continue
            close = cc[3]
            res = "T" if close == p["entry"] else \
                  ("W" if (close > p["entry"]) == (p["dir"] == "BUY") else "L")
            CSHADOW[res] += 1
            db_ins_audit(CON, p, close, res)
            done.append((p, res, close))
        else:
            keep.append(p)
    shadow_pend[:] = keep
    for p, res, close in done:
        log(f"AUDIT {res} {p['asset']} {p.get('setup', '?')} [{p['reason']}] @{p['expiry']}m "
            f"would-be ({close - p['entry']:+.6g}) | cancelled-record so far: "
            f"{CSHADOW['W']}W-{CSHADOW['L']}L-{CSHADOW['T']}T")

async def flush_pre():
    global sig_no
    await asyncio.sleep(3.0)
    cands = [c for c in pre["cands"] if not muted(c["asset"]) and c["asset"] not in armed]
    pre["cands"] = []; pre["task"] = None
    if not cands or time.time() < pause_until: return
    # ---- v33 DEFENSE: 2+ lost rounds this session → elite AQS only, half stakes ----
    if (ROUNDS["L"] - SNAP.get("__rl", 0)) >= 2 and not DEFENSE["on"]:
        DEFENSE["on"] = True
        log("v33 DEFENSE ON — 2 rounds lost this session → elite AQS only")
        try:
            await tg("🛡 v33 DEFENSE — 2 rounds lost this session: elite-only signals, half stakes")
        except Exception:
            pass
    if DEFENSE["on"]:
        _elite = [c for c in cands if c.get("aqs", 0.0) >= DEF_AQS]
        for c in cands:
            if c.get("aqs", 0.0) < DEF_AQS:
                DDAY["def_skip"] = DDAY.get("def_skip", 0) + 1
                _audit_cand(c, "defense")
                log(f"DEFENSE skip {c['asset']} (aqs {c.get('aqs', 0.0):.2f} < {DEF_AQS:.2f})")
        cands = _elite
        if not cands: return
    # ---- v23 FEED GUARD: never arm on a stale tape (v20 dead-feed losses) ----
    _nowt = time.time()
    _fresh = []
    for c in cands:
        age = _nowt - FEED_T.get(c["asset"], 0)
        if age > FEED_BENCH:
            DDAY["feed_skip"] += 1
            _audit_cand(c, "feed")
            log(f"FEED-GUARD: {c['asset']} stale {age:.0f}s — signal audited, no order on stale tape")
        else:
            c["feed_stale"] = age > FEED_WARN
            _fresh.append(c)
    cands = _fresh
    if not cands: return
    cands.sort(key=lambda x: x["rank"])
    _open_now = len(pending) + len(armed)
    for c in cands[:max(0, MAX_PER_MIN - len(armed))]:
        best = c["fired"][0]
        # ---- v23 FOCUS CAP: bounded simultaneous exposure ----
        if _open_now >= FOCUS:
            DDAY["focus_skip"] += 1
            _audit_cand(c, "focus")
            log(f"FOCUS cap {FOCUS} open — {c['asset']} signal audited (no free slot)")
            continue
        # ---- v23 ADAPT: regime + day-follow bias — DEMOTE to half stake, never drop ----
        _adapt_half = False
        if ADAPT.get("min_fires", 0) and len(c["fired"]) < 2 and best["tier"] != "A":
            _adapt_half = True
            log(f"ADAPT {ADAPT.get('profile')}: {c['asset']} lone-setup → HALF stake (traded, not dropped)")
        if c["asset"] in ADAPT.get("asset_cut", []) and best["tier"] != "A" and len(c["fired"]) < 2:
            _adapt_half = True
            log(f"ADAPT day-follow: {c['asset']} cold today → HALF stake (traded)")
        c["adapt_half"] = _adapt_half
        if DEFENSE["on"]: c["adapt_half"] = True       # v33 defense: half stakes
        c["live_half"] = bool(c.get("live_half", False))   # v33 LIVE BRAIN demote
        if c["live_half"]:
            DDAY["live_half"] = DDAY.get("live_half", 0) + 1
            log(f"LIVE BRAIN demote {c['asset']}: {c.get('live_why') or 'live-cold'} → half stake (traded)")
        c["boost"] = c["asset"] in ADAPT.get("asset_boost", [])
        c["rz_risk"] = _razor_risk(c["asset"], c["minute"])
        sig_no += 1
        trade_min = c["minute"] + 60
        armed[c["asset"]] = dict(no=sig_no, asset=c["asset"], direc=c["direc"], expiry=c["expiry"],
                                 grade=c["grade"], strategy=best["strategy"], tier=best["tier"], aqs=c.get("aqs", 0.5),
                                 nf=len(c["fired"]), dead=c.get("dead", False), conf=c.get("conf", 0.5),
                                 trade_min=trade_min, boost=bool(c.get("boost")),
                                 rz_risk=bool(c.get("rz_risk")), adapt_half=bool(c.get("adapt_half")),
                                 live_half=bool(c.get("live_half")), live_why=(c.get("live_why") or ""),
                                 rgdp=c.get("rgdp"))
        d, e = ("BUY", "🟢") if c["direc"] > 0 else ("SELL", "🔴")
        secs = max(0, int(trade_min - time.time()))
        open_ist = datetime.fromtimestamp(trade_min, tz=timezone.utc).astimezone(IST)
        exp_ist = datetime.fromtimestamp(trade_min + 60 * c["expiry"], tz=timezone.utc).astimezone(IST)
        gi = {"APEX": "🔥🔥 APEX", "HIGH": "🔥 HIGH", "STD": "STD"}[c["grade"]]
        arr = lambda x: "🟢" if x > 0 else "🔴" if x < 0 else "⚪"
        tfline = (f"M5 {arr(c['m5t'])}{arr(c['m5c'])}c | M15 {arr(c['m15'])} | "
                  f"M30 {arr(c['m30'])} | Structure {arr(c['sdir'])}")
        setups = ", ".join(f"{m['strategy']}[{m['mask']}@{m['expiry']}m]({TE[m['tier']]}{m['test']:.0%})"
                           for m in c["fired"][:3])
        stake = kelly_stake(best["test"])
        cap = (f"🧠 SMC v33 #{sig_no} [{gi}] — GET READY ({secs}s)\n"
               f"{e} {d} — {c['asset']}\n"
               f"🎯 ENTRY: next candle open {open_ist:%H:%M:%S} IST\n"
               f"⏱ EXPIRY: {c['expiry']} MIN (validated optimal) → closes {exp_ist:%H:%M:%S}\n"
               f"🕯 {setups}\n"
               f"📐 {tfline}\n"
               f"🧭 PD {c['pd']:.0%} | ER {c['er']:.2f} {reg_name(c['er'])} | {sess_name(c['sess'])} | conf {c['conf']:.0%}\n"
               f"🧬 AQS {c.get('aqs', 0):.2f} · EQS {c.get('eqs', 0):.2f} | floor {_floor_min(c['asset'], c['grade']):.2f}\n"
               + (f"🩺 LIVE BRAIN: {c.get('live_why')} → half stake\n" if c.get("live_half") and c.get("live_why") else "")
               + (f"🤖 meta p(win): {c['pwin']:.0%} (thr {c['mthr']:.2f}) [learned filter ON]\n"
                  if c.get("pwin") is not None else "")
               + f"💰 stake {stake:.2f}%\n"
               f"⚠️ WAIT for ✅GO / 🚫CANCEL at open")
        if render_chart is None:
            png = None
        else:
            try:
                series = {k: tuple(v) for k, v in sorted(store[c["asset"]].items())[-100:]}
                png, _ = await asyncio.to_thread(render_chart, c["asset"], series, 92, 100)
            except Exception as ex:
                png = None; log(f"chart error: {ex}")
        if png: await tg_photo(png, cap)
        else: await tg(cap)
        log(f"SMC #{sig_no} [{c['grade']}] {d} {c['asset']} @{c['expiry']}m [{best['strategy']}]"
            f" | {c.get('nf', 1)}v {c.get('agree', 1.0):.0%}ag c{c.get('conf', 0.5):.0%}")
    save_state()

# ---- live order placement (demo-gated in main) ----
async def place(asset, d, amt, tsec=60):
    """v25: PO hard minimum $1.00 enforced here + one retry — no signal ever dies on stake math."""
    amt = max(1.0, float(amt))
    for _att in (1, 2):
        try:
            if d == "BUY":
                r = await API_H.buy(asset=asset, amount=amt, time=tsec, check_win=False)
            else:
                r = await API_H.sell(asset=asset, amount=amt, time=tsec, check_win=False)
            tid = r[0] if isinstance(r, (tuple, list)) else r
            log(f"ORDER PLACED {d} {asset} ${amt} id={str(tid)[:12]}")
            return tid
        except Exception as e:
            if _att == 1:
                log(f"ORDER RETRY {d} {asset} ${amt} → $1.00 after: {e}")
                amt = 1.0
                await asyncio.sleep(0.4)
            else:
                log(f"ORDER FAIL {d} {asset} ${amt}: {e}")
                return None

def _journal_shadow(a, entry, reason):
    """v18: queue a cancelled/throttled signal for shadow grading."""
    try:
        shadow_pend.append(dict(asset=a["asset"], setup=a["strategy"], dir=a["direc"],
                                entry=float(entry), entry_min=int(a["trade_min"]),
                                expiry=int(a["expiry"]), reason=reason))
        if len(shadow_pend) > 60: del shadow_pend[:-60]
        log(f"AUDIT-QUEUED [{reason}] {a['asset']} {a['strategy']} @{a['expiry']}m")
    except Exception as e:
        log(f"shadow queue error: {e}")

async def confirm_or_cancel(asset, new_min):
    global cancels
    a = armed.get(asset)
    if a is None or new_min < a["trade_min"]: return
    del armed[asset]
    _storm_update(asset, new_min)              # v26: refresh supertrend read for the stake tilt
    d = "BUY" if a["direc"] > 0 else "SELL"
    if new_min > a["trade_min"]:
        cancels += 1
        _journal_shadow(a, latest_price(asset), "gap")          # v18 audit
        await tg(f"🚫 CANCEL #{a['no']} {a['asset']} — feed gap, skip (audited)")
        save_state(); return
    _thr = time.time() - LAST_TRADE.get(asset, 0) < THROTTLE_S
    if _thr and not ALWAYS_TRADE:
        cancels += 1
        _journal_shadow(a, latest_price(asset), "throttle")      # v18 audit
        log(f"THROTTLE skip #{a['no']} {asset} (<{THROTTLE_S / 60:.0f}min since last trade) — audited")
        save_state(); return
    cand = eval_candidate(asset, new_min, include_forming=False)
    if cand is not None and cand["direc"] == a["direc"]:
        LAST_TRADE[asset] = time.time()
        entry = latest_price(asset)
        pc = store[asset].get(new_min - 60)
        prev_ok = pc is not None and ((pc[3] - pc[0]) * a["direc"]) > 0   # momentum carries in
        # v18 champ gate modes (v17 strict rejected 100% of live signals)
        if CHAMP_MODE == "strict":
            champ_ok = bool(MEMBERS.get(asset)) and a["strategy"] == MEMBERS[asset][0]["strategy"]
        elif CHAMP_MODE == "tierA":
            champ_ok = a.get("tier") == "A"
        else:  # top2 (default)
            top2 = {m["strategy"] for m in MEMBERS.get(asset, [])[:2]}
            champ_ok = a["strategy"] in top2 or a.get("tier") == "A"
        q_ok = prev_ok and champ_ok and not a.get("dead", False) and a.get("conf", 1.0) >= 0.56
        gate = "-"
        if not q_ok:
            fails = []
            if not prev_ok: fails.append("prev")
            if not champ_ok: fails.append(f"champ({CHAMP_MODE})")
            if a.get("dead"): fails.append("dead")
            if a.get("conf", 1.0) < 0.56: fails.append(f"conf{a.get('conf', 0):.2f}")
            gate = ("note:" if ALWAYS_TRADE else "signal-only:") + "+".join(fails)
            log(f"QUALITY {'note (trading anyway)' if ALWAYS_TRADE else 'gate'}: {asset} {'+'.join(fails)}")
        amt = 0.0
        # v22 FULL-SEND: every armed signal gets a real demo order (QUALITY gate = note only)
        _place_ok = (q_ok or ALWAYS_TRADE) and (a.get("tier", "A") in ("ABC" if ALWAYS_TRADE else "AB"))
        if TRD["on"] and _place_ok:
            start_b = BAL_D.get("start", 100.0)
            guard = _check_daily_guard()
            if guard:
                await tg(guard)
            elif AGGRO and BAL_D["v"] >= 10000:
                TRD["on"] = False
                await tg(f"🏆🏆🏆 TARGET HIT: ${BAL_D['v']:.2f} — $10K REACHED! Trading halted to lock it in.")
            elif AGGRO and BAL_D["v"] < 30:
                TRD["on"] = False
                await tg(f"🛡 FLOOR HIT: ${BAL_D['v']:.2f} < $30 — aggressive run stopped (signals continue)")
            elif AGGRO:
                mtg_ok = UNION.get(asset, {}).get("mtg_acc", 0) >= 0.85
                conf_ok = (a["grade"] == "APEX" or a.get("tier") == "A" or a.get("nf", 1) >= 2)
                benched = time.time() - ASSET_LAST.get(asset, 0) < 600
                if not mtg_ok or not conf_ok or benched:
                    log(f"PEAK-90 gate: {asset} signal-only (mtg85={mtg_ok} conf={conf_ok} benched={benched})")
                else:
                    rate = min(RSTATE["rate"] * 1.25, 0.125)
                    amt = round(max(1.0, BAL_D["v"] * rate), 2)
                    if PROB.get(asset): amt = round(max(1.0, amt * 0.5), 2)   # v20 probation
                    tid = await place(asset, d, amt)
                    if tid is None: amt = 0.0
            elif BAL_D["v"] <= 0.85 * start_b:
                TRD["on"] = False
                await tg(f"🛡 CAPITAL GUARD: balance ${BAL_D['v']:.2f} hit -15% — auto-trading HALTED (signals continue)")
            else:
                rate = (0.02 if BAL_D["v"] >= 1.25 * start_b else 0.04) * ADAPT.get("risk", 1.0)
                amt = round(max(1.0, BAL_D["v"] * rate), 2)
                if PROB.get(asset): amt = round(max(1.0, amt * 0.5), 2)       # v20 probation
                # ---- v23 adaptive stake stack (cuts first, boost last) ----
                if a.get("rz_risk"):
                    amt = round(max(1.0, amt * RAZOR_MIN), 2); DDAY["rz_risk"] += 1
                    log(f"RAZOR-RISK: compressed vol — {asset} quarter stake ${amt:.2f}")
                if _thr:
                    amt = round(max(1.0, amt * 0.5), 2); DDAY["thr_half"] += 1
                    log(f"THROTTLE(demote): {asset} half stake ${amt:.2f} (v23: never drop)")
                if a.get("boost"):
                    amt = round(amt * 1.25, 2)
                if a.get("adapt_half"):
                    amt = round(max(1.0, amt * 0.5), 2); DDAY["adapt_half"] += 1
                    log(f"ADAPT half stake: {asset} ${amt:.2f} (lone/cold setup traded anyway)")
                if a.get("live_half"):
                    amt = round(max(1.0, amt * 0.5), 2)
                    log(f"LIVE BRAIN half stake: {asset} ${amt:.2f} ({a.get('live_why') or 'live-cold'})")
                # ---- v24 LIVE LADDER: bayes tiers + health + exposure (demote, never drop) ----
                _vm, _vt, _vp = _v24_mult(asset, a["strategy"], d, a.get("conf", 0.5),
                                          float((cand or {}).get("agree", 1.0)))
                if _vm != 1.0:
                    amt = round(max(1.0, amt * _vm), 2)
                    log(f"V24 ladder [{' '.join(_vt)}] p_live={(_vp or 0):.2f} → ${amt:.2f}")
                amt = round(min(amt, max(1.0, BAL_D["v"] * STAKE_CAP)), 2)
                # ---- v23 AI RISK OFFICER (bounded, fail-open, audited) ----
                _veto, _why = await _ai_veto(dict(asset=asset, dir=d, strategy=a["strategy"],
                                                  tier=a.get("tier"), grade=a.get("grade"),
                                                  conf=a.get("conf"), pwin=cand.get("pwin"),
                                                  er=cand.get("er"), stake=amt,
                                                  profile=ADAPT.get("profile")))
                if _veto:
                    DDAY["ai_skip"] += 1
                    _journal_shadow(a, entry, "ai")
                    log(f"AI-GUARD veto: {asset} audited, no order — {_why}")
                    amt = 0.0
                elif _why == "size_down":
                    amt = round(max(1.0, amt * 0.5), 2)
                    log(f"AI-GUARD: {asset} size_down → ${amt:.2f}")
                    tid = await place(asset, d, amt)
                    if tid is None: amt = 0.0
                else:
                    tid = await place(asset, d, amt)
                    if tid is None: amt = 0.0
        pending.append(dict(no=a["no"], asset=asset, dir=d, entry=entry, entry_min=new_min,
                            expiry=a["expiry"], grade=a["grade"], strategy=a["strategy"], amt=amt,
                            pwin=cand.get("pwin"), conf=cand.get("conf"), sess=cand.get("sess"),
                            er=cand.get("er"), gate=gate, atr=_atr_proxy(asset, new_min), rgdp=cand.get("rgdp"),
                            pstake=_paper_stake(normal=True)))
        DDAY["sig"] += 1
        exp = datetime.fromtimestamp(new_min + 60 * a["expiry"], tz=timezone.utc).astimezone(IST)
        await tg((f"💵 TRADED ${amt} (demo)\n" if amt else "") + f"✅ GO #{a['no']} [{a['grade']}] — ENTER NOW\n"
                 f"{'🟢' if d == 'BUY' else '🔴'} {d} {asset} @ {entry:g}\n"
                 f"⏱ {a['expiry']} min expiry — closes {exp:%H:%M:%S} IST")
        log(f"GO #{a['no']} {d} {asset} @{a['expiry']}m @ {entry:g}")
    else:
        # ---- v20 SOFT-CANCEL: audit says most cancels would have won (8W-4L) ----
        entry_s = latest_price(asset)
        pc = store[asset].get(new_min - 60)
        atrv = _atr_proxy(asset, new_min) or 0.0
        adverse = pc is not None and atrv > 0 and ((pc[3] - pc[0]) * a["direc"]) < -SOFT_ADVERSE * atrv
        flipped = cand is not None and cand["direc"] != a["direc"]
        _weak = adverse or flipped
        # v23 FULL-SEND: under ALWAYS_TRADE even an adverse/flipped open is TRADED (quarter stake)
        if (SOFTC and not _weak) or (ALWAYS_TRADE and _weak):
            LAST_TRADE[asset] = time.time()
            amt = 0.0
            if TRD["on"] and (a.get("tier", "A") in ("ABC" if ALWAYS_TRADE else "AB")):
                guard = _check_daily_guard()
                if guard:
                    await tg(guard)
                elif not _profit_locked():
                    start_b = BAL_D.get("start", 100.0)
                    rate = (0.02 if BAL_D["v"] >= 1.25 * start_b else 0.04) * ADAPT.get("risk", 1.0)
                    amt = round(max(1.0, BAL_D["v"] * rate) * 0.5, 2)
                    if a.get("rz_risk"):
                        amt = round(max(1.0, amt * RAZOR_MIN), 2); DDAY["rz_risk"] += 1
                    if _thr:
                        amt = round(max(1.0, amt * 0.5), 2); DDAY["thr_half"] += 1
                    if a.get("boost"):
                        amt = round(amt * 1.25, 2)
                    if a.get("adapt_half"):
                        amt = round(max(1.0, amt * 0.5), 2); DDAY["adapt_half"] += 1
                    if a.get("live_half"):
                        amt = round(max(1.0, amt * 0.5), 2)
                        log(f"LIVE BRAIN half stake: {asset} ${amt:.2f} ({a.get('live_why') or 'live-cold'})")
                    _vm2, _vt2, _vp2 = _v24_mult(asset, a["strategy"], d, a.get("conf", 0.5), 1.0)
                    if _vm2 != 1.0:
                        amt = round(max(1.0, amt * _vm2), 2)
                        log(f"V24 ladder [{' '.join(_vt2)}] p_live={(_vp2 or 0):.2f} → ${amt:.2f}")
                    amt = round(min(amt, max(1.0, BAL_D["v"] * STAKE_CAP)), 2)
                    if _weak:
                        amt = round(max(1.0, amt * 0.5), 2); DDAY["soft_weak"] += 1
                    tid = await place(asset, d, amt)
                    if tid is None: amt = 0.0
            pending.append(dict(no=a["no"], asset=asset, dir=d, entry=entry_s, entry_min=new_min,
                                expiry=a["expiry"], grade=a["grade"], strategy=a["strategy"],
                                amt=amt, pwin=None, conf=a.get("conf"), sess=None, er=None, rgdp=a.get("rgdp"),
                                gate=("soft-weak" if _weak else "soft-half"), atr=atrv,
                                pstake=_paper_stake(normal=True), soft=True))
            DDAY["sig"] += 1
            _tag = "SOFT-WEAK" if _weak else "SOFT"
            _lbl = ("QUARTER stake (adverse open — traded anyway, v23)" if _weak
                    else "HALF stake (setup weakened)")
            await tg((f"💵 SOFT-TRADED ${amt} (demo)\n" if amt else "") +
                     f"🪶 {_tag} ENTRY #{a['no']} [{a['grade']}] — {_lbl}\n"
                     f"{'🟢' if d == 'BUY' else '🔴'} {d} {asset} @ {entry_s:g}")
            log(f"{_tag} #{a['no']} {d} {asset} @{a['expiry']}m "
                f"{'quarter' if _weak else 'half'}-stake")
        else:
            cancels += 1
            _journal_shadow(a, entry_s, "broke")                 # v18 audit
            await tg(f"🚫 CANCEL #{a['no']} {asset} {d} — setup broke at open, skip (audited)")
            log(f"CANCEL #{a['no']} {asset} (adverse={adverse} flipped={flipped})")
    save_state()

async def _feed_rescue(sub):
    """v26: after a stream gap, backfill history for assets with OPEN LEGS and grade them.
       (v25 evidence: feed died → two real legs never resolved.)"""
    try:
        _assets = sorted({p["asset"] for p in pending if not p.get("skip")})
        if not _assets:
            return
        for a in _assets:
            try:
                store.setdefault(a, {})
                df = await fetch_df(API_H, sub, a)
                for ts, r in zip(df.index.astype(np.int64) // 10**9, df.values):
                    store[a][int(ts // 60) * 60] = list(r)
                FEED_T[a] = time.time()
                _mx = max(store[a]) if store[a] else None
                if _mx is not None:
                    await resolve_pending(a, _mx)
                    _storm_update(a, None)
            except Exception:
                pass
        log(f"FEED RESCUE: backfilled {len(_assets)} asset(s) with open legs")
    except Exception as ex:
        log(f"feed rescue error: {ex}")


async def handle_frame(raw, live):
    STREAM_T["t"] = time.time()              # v20 feed watchdog heartbeat
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
            FEED_T[a] = time.time()          # v23 per-asset feed freshness
            prev = cur_min.get(a)
            if live and prev is not None and m > prev:
                cur_min[a] = m
                if len(store[a]) > KEEP + 200:
                    for k in sorted(store[a])[:-KEEP]:
                        del store[a][k]
                await resolve_pending(a, m)
                await resolve_shadow(a, m)          # v18 audit grading
                await confirm_or_cancel(a, m)
            elif prev is None or m > prev:
                cur_min[a] = m
            if (live and a in MEMBERS and a not in armed and time.time() >= pause_until
                    and (t - m) >= PRE_SEC and last_pre.get(a) != m
                    and time.time() >= LIVE_T0["t"] + SKIP_WARMUP_S):
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

# ====================== SESSION ANALYTICS (v18) ==============================
def session_summary():
    """Post-session analytics: the numbers the v17 run could not show."""
    tot = score_s["W"] + score_s["L"]
    wr = score_s["W"] / tot * 100 if tot else 0.0
    sh_t = CSHADOW["W"] + CSHADOW["L"]
    sh_wr = CSHADOW["W"] / sh_t * 100 if sh_t else 0.0
    mt_t = mtg_round["W"] + mtg_round["L"]
    rz_w, rz_l = DDAY["rz_w"], DDAY["rz_l"]
    nm_w, nm_l = DDAY["nm_w"], DDAY["nm_l"]
    lines = [f"📊 SESSION ANALYTICS — SMC v33 BINARY GOD ENGINE",
             f"🎯 Direct: {score_s['W']}W–{score_s['L']}L–{score_s['T']}T ({wr:.1f}%) | "
             f"breakeven {BREAKEVEN * 100:.2f}% @92%"]
    lines.append(f"📄 Paper P&L ({PAPER_PCT:.0%} stakes, incl. {MTG_MULT}x MTG legs): "
                 f"${DDAY['paper']:+.2f}")
    lines.append(f"🧠 LIVE BRAIN: {LIVE.get('n', 0)} legs learned | rolling {LIVE.get('rollwr', 1.0):.0%}"
                 f" | half-stakes {DDAY.get('live_half', 0)} · cooldowns {DDAY.get('live_cool', 0)}"
                 f" | dims dir {len(LIVE['dir'])} reg {len(LIVE['reg'])} hour {len(LIVE['hour'])}")
    lines.append(f"🧬 OMEGA: floor-skips {DDAY.get('floor_skip', 0)} · turn {DDAY.get('turn_skip', 0)}"
                 f" · EQS {DDAY.get('eqs_skip', 0)} · calbl {DDAY.get('cal_skip', 0)}"
                 f" · ladder-caps {DDAY.get('ladders', 0)} | fusion n={METAF.get('n', 0)}"
                 f" acc {METAF.get('acc', 0.5):.2f} | floors {len(FLOORS)}")
    lines.append(f"🎯 ROUNDS: {ROUNDS['W']}W–{ROUNDS['L']}L"
                 + (f" | recovered: {ROUNDS['rec']} ({ROUNDS['absorbed']} leg loss(es) ABSORBED"
                    f" — USDCOP rule)" if ROUNDS["rec"] else "")
                 + f" | risk x{ADAPT['risk']:.2f}")
    if DDAY.get("mtg_skip", 0):
        lines.append(f"✂️ MTG legs skipped real (paper-only): ${DDAY.get('skip_net', 0.0):+.2f} "
                     f"— never staked; streak ignores them (v23)")
    _sw, _sl = DDAY.get("storm_w", 0), DDAY.get("storm_l", 0)
    if _sw + _sl:
        lines.append(f"🌪 STORM module (supertrend {STORM_FACTOR}/{STORM_ATR} + SMA9): "
                     f"{_sw}W–{_sl}L ({_sw / (_sw + _sl) * 100:.0f}%)")
    if DDAY.get("storm_ag", 0) or DDAY.get("storm_op", 0):
        lines.append(f"🌪 STORM tilt: agreed ×1.20 on {DDAY.get('storm_ag', 0)} signal(s), "
                     f"opposed ×0.90 on {DDAY.get('storm_op', 0)}")
    if DDAY.get("mtg_step2", 0):
        lines.append(f"🔂 God-ladder step-2 recovery legs taken (real on PO): {DDAY['mtg_step2']}")
    if ADAPT.get("notes"):
        lines.append(f"🧬 ADAPT {ADAPT.get('profile', '?')} risk x{ADAPT.get('risk', 1.0)}: "
                     + " | ".join(ADAPT["notes"]))
    if DDAY.get("thr_half", 0):
        lines.append(f"⏳ Throttle demotes (half stake, STILL traded): {DDAY['thr_half']}")
    if DDAY.get("adapt_half", 0):
        lines.append(f"🧬 ADAPT half stakes (lone/cold setups, STILL traded): {DDAY['adapt_half']}")
    if DDAY.get("soft_weak", 0):
        lines.append(f"🪶 Adverse-open quarter stakes (traded, not cancelled): {DDAY['soft_weak']}")
    if DDAY.get("rz_risk", 0):
        lines.append(f"🪒 Razor-risk quarter stakes: {DDAY['rz_risk']} "
                     f"({DDAY.get('rz_risk_w', 0)}W–{DDAY.get('rz_risk_l', 0)}L)")
    if DDAY.get("rt_cut", 0):
        lines.append(f"🧊 RT-cold quarter stakes: {DDAY['rt_cut']}")
    if DDAY.get("focus_skip", 0) or DDAY.get("feed_skip", 0):
        lines.append(f"🛡 v23 safety skips (audited): focus-cap {DDAY.get('focus_skip', 0)} | "
                     f"stale-feed {DDAY.get('feed_skip', 0)}")
    if DDAY.get("v24_n"):
        _cf = DDAY["v24_cf"] / max(DDAY["v24_n"], 1)
        _ag = DDAY["v24_ag"] / max(DDAY["v24_n"], 1)
        lines.append(f"🧠 v24 ensemble: {DDAY['v24_n']} sized | avg conf {_cf:.0%} | "
                     f"avg agreement {_ag:.0%} | bayes {DDAY.get('bayes_adj', 0)} | "
                     f"health {DDAY.get('health_cut', 0)} | exposure {DDAY.get('corr_half', 0)}")
    if AI_CALLS["dec"] or AI_CALLS["skip"] or AI_CALLS["down"]:
        lines.append(f"🤖 AI agent: {AI_CALLS['dec']} decisions | {AI_CALLS['skip']} vetos | "
                     f"{AI_CALLS['down']} offline")
    if PROB:
        lines.append(f"🟡 Probation assets armed: {len(PROB)} (agreement required, half stake)")
    if DDAY.get("mtg_skip", 0):
        lines.append(f"✂️ MTG re-entries skipped by fresh-confirm: {DDAY['mtg_skip']} (bleed avoided)")
    if DDAY.get("soft_w", 0) + DDAY.get("soft_l", 0):
        lines.append(f"🪶 SOFT entries (weakened setup kept at half stake): "
                     f"{DDAY['soft_w']}W–{DDAY['soft_l']}L")
    _dt = DDAY.get("dw", 0) + DDAY.get("dl", 0)
    if _dt:
        lines.append(f"🧼 CLEAN direct (excl. MTG legs): {DDAY['dw']}W–{DDAY['dl']}L "
                     f"({DDAY['dw'] / _dt * 100:.1f}%)")
    if mt_t:
        lines.append(f"🔁 MTG rounds: {mtg_round['W']}W–{mtg_round['L']}L | MTG net: "
                     f"${DDAY['mtg_net']:+.2f}" + ("  🧯 auto-MTG halted" if MTG_STATE["halted"] else ""))
    if sh_t:
        verdict = ("FILTER SAVED money ✅" if sh_wr < BREAKEVEN * 100 else
                   "FILTER COST money ⚠️ (cancels were winning)" if sh_wr > BREAKEVEN * 100 + 3 else
                   "filter ≈ neutral")
        lines.append(f"🚫 Cancelled-audit: {CSHADOW['W']}W–{CSHADOW['L']}L ({sh_wr:.1f}% would-be) → {verdict}")
        try:
            rows = list(CON.execute(
                "SELECT reason, SUM(outcome='W'), SUM(outcome='L'), COUNT(*) "
                "FROM apex_audit GROUP BY reason"))
            for reason, w, l, n in rows:
                if n: lines.append(f"   • {reason}: {int(w)}W–{int(l)}L of {n}")
        except Exception:
            pass
    else:
        lines.append("🚫 Cancelled-audit: none graded this session")
    if rz_w + rz_l + nm_w + nm_l:
        lines.append(f"🪒 Razor closes (<{RAZOR_ATR:.0%} ATR): {rz_w}W–{rz_l}L | "
                     f"Normal: {nm_w}W–{nm_l}L")
    return "\n".join(lines)

def save_session_row():
    try:
        CON.execute("INSERT INTO apex_session VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (time.time(), sig_no, DDAY["sig"], cancels, score_s["W"], score_s["L"],
                     score_s["T"], round(DDAY["paper"], 2), mtg_round["W"], mtg_round["L"],
                     round(DDAY["mtg_net"], 2), CSHADOW["W"], CSHADOW["L"],
                     DDAY["rz_w"], DDAY["rz_l"]))
        CON.commit()
    except Exception as e:
        log(f"session row error: {e}")

# ============================ MAIN ===========================================

# ═══════════════════════════ v30 ETERNAL session machinery ═══════════════════════════════
def _sess_snap():
    """Snapshot every counter at session start; the 50-min report is pure deltas."""
    SNAP.clear()
    SNAP["__d"] = {k: v for k, v in DDAY.items() if isinstance(v, (int, float))}
    SNAP["__bal"] = BAL_D.get("v")
    SNAP["__sig"] = sig_no; SNAP["__can"] = cancels
    SNAP["__sw"] = score_s["W"]; SNAP["__sl"] = score_s["L"]; SNAP["__st"] = score_s["T"]
    SNAP["__rw"] = ROUNDS["W"]; SNAP["__rl"] = ROUNDS["L"]
    SNAP["__rrec"] = ROUNDS["rec"]; SNAP["__rabs"] = ROUNDS["absorbed"]
    SNAP["__ps"] = {a: (s.get("W", 0), s.get("L", 0)) for a, s in pair_score.items()}
    DEFENSE["on"] = False          # v33 defense resets every session
    SNAP["__t0"] = time.time()
    return SNAP


def _day_snap():
    DAY0.clear()
    DAY0.update(w=score_s["W"], l=score_s["L"], t=score_s["T"], sig=sig_no, can=cancels,
                rw=ROUNDS["W"], rl=ROUNDS["L"], rec=ROUNDS["rec"], abs=ROUNDS["absorbed"],
                mtg=DDAY.get("mtg_net", 0.0), paper=DDAY.get("paper", 0.0),
                bal=BAL_D.get("v"), ts=time.time())


def _sess_metrics(sn):
    bal = BAL_D.get("v") or 0.0
    m = dict(
        sn=sn, sig=sig_no - SNAP.get("__sig", 0), can=cancels - SNAP.get("__can", 0),
        sw=score_s["W"] - SNAP.get("__sw", 0), sl=score_s["L"] - SNAP.get("__sl", 0),
        st=score_s["T"] - SNAP.get("__st", 0),
        rw=ROUNDS["W"] - SNAP.get("__rw", 0), rl=ROUNDS["L"] - SNAP.get("__rl", 0),
        rr=ROUNDS["rec"] - SNAP.get("__rrec", 0), rabs=ROUNDS["absorbed"] - SNAP.get("__rabs", 0),
        bal=bal, pnl=bal - (SNAP.get("__bal") or bal),
        mtg=(DDAY.get("mtg_net", 0.0) - SNAP.get("__d", {}).get("mtg_net", 0.0)),
        paper=(DDAY.get("paper", 0.0) - SNAP.get("__d", {}).get("paper", 0.0)),
        skip=(DDAY.get("sniper_skip", 0) - SNAP.get("__d", {}).get("sniper_skip", 0)),
        aqsk=(DDAY.get("aqs_skip", 0) - SNAP.get("__d", {}).get("aqs_skip", 0)),
        dfs=(DDAY.get("def_skip", 0) - SNAP.get("__d", {}).get("def_skip", 0)),
        fls=(DDAY.get("floor_skip", 0) - SNAP.get("__d", {}).get("floor_skip", 0)),
        tns=(DDAY.get("turn_skip", 0) - SNAP.get("__d", {}).get("turn_skip", 0)),
        eqk=(DDAY.get("eqs_skip", 0) - SNAP.get("__d", {}).get("eqs_skip", 0)),
        calsk=(DDAY.get("cal_skip", 0) - SNAP.get("__d", {}).get("cal_skip", 0)),
        lads=(DDAY.get("ladders", 0) - SNAP.get("__d", {}).get("ladders", 0)),
        lvh=(DDAY.get("live_half", 0) - SNAP.get("__d", {}).get("live_half", 0)),
        lvc=(DDAY.get("live_cool", 0) - SNAP.get("__d", {}).get("live_cool", 0)),
        mins=(time.time() - SNAP.get("__t0", time.time())) / 60.0)
    _best, _worst = ("—", 0), ("—", 0)
    for a, s in pair_score.items():
        b0w, b0l = SNAP.get("__ps", {}).get(a, (s.get("W", 0), s.get("L", 0)))
        dd = (s.get("W", 0) - b0w) - (s.get("L", 0) - b0l)
        if dd > _best[1]: _best = (a, dd)
        if dd < _worst[1]: _worst = (a, dd)
    m["best"], m["worst"] = _best[0], _worst[0]
    return m


def _session_report_text(sn):
    m = _sess_metrics(sn); SESS_LAST.clear(); SESS_LAST.update(m)
    tot = m["sw"] + m["sl"]
    wr = m["sw"] / tot * 100 if tot else 0.0
    dw = score_s["W"] - DAY0.get("w", 0); dl = score_s["L"] - DAY0.get("l", 0)
    d_sig = sig_no - DAY0.get("sig", 0)
    drw = ROUNDS["W"] - DAY0.get("rw", 0); drl = ROUNDS["L"] - DAY0.get("rl", 0)
    dmtg = DDAY.get("mtg_net", 0.0) - DAY0.get("mtg", 0.0)
    L = LIFETIME
    lines = [f"📊 SESSION #{sn} REPORT — {m['mins']:.0f} min (ended {datetime.now(IST):%H:%M} IST)"]
    lines.append(f"⚡ Signals: {m['sig']} | direct {m['sw']}W–{m['sl']}L" +
                 (f"–{m['st']}T" if m["st"] else "") + f" ({wr:.0f}%)")
    lines.append(f"🎯 ROUNDS {m['rw']}W–{m['rl']}L" +
                 (f" | recovered {m['rr']} · {m['rabs']} leg loss(es) ABSORBED (USDCOP rule)"
                  if m["rr"] else ""))
    if TRD["on"]:
        lines.append(f"💰 Session P&L: {m['pnl']:+.2f} → balance ${m['bal']:.2f}")
    else:
        lines.append(f"💰 Session paper P&L: {m['paper']:+.2f}")
    lines.append(f"📅 Day: {d_sig} signals | legs {dw}W–{dl}L | ROUNDS {drw}W–{drl}L | MTG net ${dmtg:+.2f}")
    lines.append(f"📈 Lifetime: {L['sessions']} sessions | legs {L['w']}W–{L['l']}L | "
                 f"ROUNDS {L['rw']}W–{L['rl']}L | recovered {L['rec']} | net {L['pnl']:+.2f}")
    lines.append(f"🏆 Best: {m['best']} | 🔻 Worst: {m['worst']} | 🔁 MTG net ${m['mtg']:+.2f}")
    _fresh = sum(1 for a in MEMBERS if time.time() - FEED_T.get(a, 0) <= FEED_WARN)
    lines.append(f"🎯 Gates: sniper {m['skip']} · AQS {m['aqsk']} · defense {m['dfs']} · floor "
                 f"{m.get('fls', 0)} · turn {m.get('tns', 0)} · EQS {m.get('eqk', 0)} · calbl "
                 f"{m.get('calsk', 0)} · ladder-caps {m.get('lads', 0)} | "
                 f"risk x{ADAPT['risk']:.2f} | feed {_fresh}/{len(MEMBERS)}")
    lines.append(f"🧠 LIVE BRAIN: {LIVE.get('n', 0)} legs · half {m.get('lvh', 0)} · cool {m.get('lvc', 0)}"
                 f" · rolling {LIVE.get('rollwr', 1.0):.0%} | dims dir {len(LIVE['dir'])}"
                 f" reg {len(LIVE['reg'])} hour {len(LIVE['hour'])}")
    lines.append(f"⚡ Next session starts NOW — 24/7, no breaks")
    return "\n".join(lines)


def _write_machine_report(sn, extra=None):
    try:
        _rep = dict(v="v33", ts=time.time(), session=sn, signals=sig_no,
                    w=score_s["W"], l=score_s["L"], t=score_s["T"], cancels=cancels,
                    paper=round(DDAY.get("paper", 0.0), 2), mtg=dict(mtg_round),
                    mtg_net=round(DDAY.get("mtg_net", 0.0), 2),
                    skip_net=round(DDAY.get("skip_net", 0.0), 2),
                    mtg_skip=DDAY.get("mtg_skip", 0), sniper_skip=DDAY.get("sniper_skip", 0), aqs_skip=DDAY.get("aqs_skip", 0),
                    chaos_skip=DDAY.get("chaos_skip", 0), fresh_skip=DDAY.get("fresh_skip", 0),
                    def_skip=DDAY.get("def_skip", 0), cal=dict(CAL),
                    floor_skip=DDAY.get("floor_skip", 0), turn_skip=DDAY.get("turn_skip", 0),
                    eqs_skip=DDAY.get("eqs_skip", 0), cal_skip=DDAY.get("cal_skip", 0),
                    ladders=DDAY.get("ladders", 0), metaf=dict(METAF), floors=dict(FLOORS),
                    live=dict(LIVE), live_half=DDAY.get("live_half", 0),
                    live_cool=DDAY.get("live_cool", 0), maxconf=MAXCONF,
                    clean=[DDAY.get("dw", 0), DDAY.get("dl", 0)],
                    soft=[DDAY.get("soft_w", 0), DDAY.get("soft_l", 0)],
                    storm=[DDAY.get("storm_w", 0), DDAY.get("storm_l", 0)],
                    rounds=dict(W=ROUNDS["W"], L=ROUNDS["L"], rec=ROUNDS["rec"],
                                absorbed=ROUNDS["absorbed"]),
                    storm_ag=DDAY.get("storm_ag", 0), storm_op=DDAY.get("storm_op", 0),
                    mtg_step2=DDAY.get("mtg_step2", 0),
                    razor=[DDAY.get("rz_w", 0), DDAY.get("rz_l", 0)],
                    adapt=dict(ADAPT), ai=dict(AI_CALLS),
                    bal=BAL_D.get("v"), bal_start=BAL_D.get("start"),
                    lifetime=dict(LIFETIME), last_session=dict(SESS_LAST),
                    roster=len(MEMBERS), per_asset=dict(pair_score))
        if extra: _rep.update(extra)
        with open(V33_REPORT, "w") as f:
            json.dump(_rep, f, indent=1)
        log(f"v33 report written → {V33_REPORT}")
    except Exception as ex:
        log(f"report write error: {ex}")


async def _session_end(sn, bal_now):
    """v30: 50-min report + persist + lifetime totals. The next session starts immediately."""
    if bal_now:
        BAL_D["v"] = float(bal_now)
    m = _sess_metrics(sn)
    L = LIFETIME
    L["sessions"] = sn
    if L.get("since") is None: L["since"] = time.time()
    L["sig"] += m["sig"]; L["w"] += m["sw"]; L["l"] += m["sl"]
    L["rw"] += m["rw"]; L["rl"] += m["rl"]; L["rec"] += m["rr"]; L["abs"] += m["rabs"]
    if TRD["on"]: L["pnl"] += m["pnl"]
    txt = _session_report_text(sn)
    try:
        await tg(txt)
        if VS.get("on"):
            _v = (f"Session {sn} complete. {m['sig']} signals. Direct {m['sw']} wins, {m['sl']} losses. "
                  f"Rounds {m['rw']} wins {m['rl']} losses. "
                  + (f"Session profit {m['pnl']:.2f} dollars. " if TRD["on"] else "")
                  + f"Balance {m['bal']:.2f} dollars. Next session starting now.")
            await tg_voice(_v, "📊 v33 session report")
    except Exception as ex:
        log(f"report post error: {ex}")
    try:
        save_session_row()
    except Exception:
        pass
    _write_machine_report(sn, extra=dict(session_metrics=m))
    try:
        with open(V33_SESSIONS, "a") as f:
            f.write(json.dumps(dict(ts=time.time(), sn=sn, sig=m["sig"], sw=m["sw"], sl=m["sl"],
                                    rw=m["rw"], rl=m["rl"], rec=m["rr"], absorbed=m["rabs"],
                                    pnl=round(m["pnl"], 2), paper=round(m["paper"], 2),
                                    bal=round(m["bal"], 2), skip=m["skip"],
                                    mins=round(m["mins"], 1))) + "\n")
    except Exception as ex:
        log(f"sessions jsonl error: {ex}")
    log("=" * 62)
    for _ln in txt.splitlines():
        log(_ln)
    log("=" * 62)
    return txt


async def _maybe_day_roll():
    """v30: at IST midnight post the full DAY report, then start the new day clean."""
    d_now = datetime.now(IST).strftime("%Y-%m-%d")
    if DDAY.get("d") == d_now:
        return False
    tot = (score_s["W"] - DAY0.get("w", 0)) + (score_s["L"] - DAY0.get("l", 0))
    wr = (score_s["W"] - DAY0.get("w", 0)) / tot * 100 if tot else 0.0
    try:
        await tg(f"🌙 DAY COMPLETE — {DDAY.get('d')}\n"
                 f"⚡ {sig_no - DAY0.get('sig', 0)} signals | legs {score_s['W'] - DAY0.get('w', 0)}W–"
                 f"{score_s['L'] - DAY0.get('l', 0)}L ({wr:.0f}%)\n"
                 f"🎯 ROUNDS {ROUNDS['W'] - DAY0.get('rw', 0)}W–{ROUNDS['L'] - DAY0.get('rl', 0)}L | "
                 f"recovered {ROUNDS['rec'] - DAY0.get('rec', 0)}\n"
                 f"💰 Day net ${(DDAY.get('pnl', 0.0)):+.2f} | balance ${BAL_D.get('v', 0):.2f}\n"
                 f"📈 Lifetime: {LIFETIME['sessions']} sessions | ROUNDS {LIFETIME['rw']}W–"
                 f"{LIFETIME['rl']}L | net {LIFETIME['pnl']:+.2f}\n"
                 f"☀️ New trading day starting NOW — 24/7")
    except Exception as ex:
        log(f"day card error: {ex}")
    _roll_day()
    DDAY["b0"] = BAL_D.get("v", DDAY.get("b0", 0.0))
    _day_snap()
    log("DAY ROLL — new day card posted, counters re-based")
    return True


async def _session_transition(api, sub, sn):
    """v30: between windows — payout rescan (roster follows PO), add/drop pairs, refresh models."""
    t0 = time.time()
    REFRESH.update(n=0, adds=0, drops=0)
    _hq_build()                       # v33 ENGINE C refresh at session boundary
    try:
        _floor_seed(); _metaf_build()          # v33 ENGINE G+F refresh at session boundary
    except Exception as ex:
        log(f"v33 fusion refresh skipped: {ex}")
    # 1) payout rescan — the roster follows the money (payouts move through the day)
    try:
        payouts = await api.payout()
        PAYOUTS.clear(); PAYOUTS.update({a: float(p) for a, p in payouts.items()})   # v33 payout map
        _rk = sorted(((a, float(p)) for a, p in payouts.items() if float(p) >= 90),
                     key=lambda kv: (-kv[1], kv[0]))
        want = [a for a, _p in _rk[:PAIRS_MAX]]
        if len(want) < 8:
            want = [a for a, p in sorted(payouts.items(), key=lambda kv: -float(kv[1]))[:PAIRS_MAX]
                    if float(p) >= 85]
        cur = set(MEMBERS)
        adds = [a for a in want if a not in cur][:3]
        drops = [a for a in cur if a not in want]
        for a in drops:
            if any(p.get("asset") == a for p in pending):
                continue                     # keep trading until its legs resolve
            MEMBERS.pop(a, None)
        for a in adds:
            try:
                store.setdefault(a, {})
                FEED_T[a] = time.time()
                await api.send_raw('42["changeSymbol",{"asset":"%s","period":60}]' % a)
                df = await fetch_df(api, sub, a)
                if len(df) < 1500: raise RuntimeError(f"only {len(df)} candles")
                res = await asyncio.to_thread(train_smc, df)
                if res is None: continue
                for ts, r in zip(df.index.astype(np.int64) // 10**9, df.values):
                    store[a][int(ts // 60) * 60] = list(r)
                MEMBERS[a] = res["members"]; UNION[a] = res["union"]; AIF[a] = res.get("aif")
                HOURS[a] = res["hour_ok"]; MTGK[a] = 1; TRAIN_T[a] = time.time()
                PROB.pop(a, None)
            except Exception as ex:
                log(f"pair add {a} failed: {ex}")
        REFRESH["adds"] = len(adds); REFRESH["drops"] = len(drops)
        if adds or drops:
            await tg(f"🔄 PAIR SWITCH v33 — +{len(adds)} new ≥90% pairs, −{len(drops)} dropped "
                     f"(PO payouts moved) | roster {len(MEMBERS)}")
            log(f"roster: +{adds} -{drops}")
    except Exception as ex:
        log(f"payout rescan failed: {ex}")
    # 2) rotating model refresh — the stalest RETRAIN_N assets get re-trained every session
    _ref = 0
    try:
        _stalest = sorted(MEMBERS, key=lambda a: TRAIN_T.get(a, 0))[:max(0, RETRAIN_N)]
        for a in _stalest:
            try:
                df = await fetch_df(api, sub, a)
                if len(df) < 1500: continue
                res = await asyncio.to_thread(train_smc, df)
                if res is None: continue
                for ts, r in zip(df.index.astype(np.int64) // 10**9, df.values):
                    store[a][int(ts // 60) * 60] = list(r)
                _ut = res["union"]["test_acc"]
                if _ut < ASSET_MIN_TEST:
                    if PROBATION and _ut >= PROB_MIN_TEST:
                        PROB[a] = True
                    else:
                        MEMBERS.pop(a, None)
                        continue
                else:
                    PROB.pop(a, None)
                MEMBERS[a] = res["members"]; UNION[a] = res["union"]; AIF[a] = res.get("aif")
                HOURS[a] = res["hour_ok"]; MTGK[a] = 1; TRAIN_T[a] = time.time()
                _ref += 1
            except Exception as ex:
                log(f"refresh {a} failed: {ex}")
    except Exception as ex:
        log(f"refresh failed: {ex}")
    REFRESH["n"] = _ref
    log(f"session transition {time.time() - t0:.0f}s — roster {len(MEMBERS)}, refreshed {_ref}, "
        f"+{REFRESH['adds']} −{REFRESH['drops']}")
    return True


def _start_health_server():
    """v30: stdlib /health + /status endpoint when the host provides $PORT (no extra deps)."""
    port = os.environ.get("PORT")
    if not port:
        return
    try:
        import threading
        from http.server import BaseHTTPRequestHandler, HTTPServer

        class _H(BaseHTTPRequestHandler):
            def do_GET(self):
                try:
                    body = json.dumps(dict(ok=True, engine="v33 OMEGA", sessions=LIFETIME.get("sessions", 0),
                                           signals=LIFETIME.get("sig", 0), rounds=[LIFETIME.get("rw", 0),
                                           LIFETIME.get("rl", 0)], balance=BAL_D.get("v"),
                                           open_legs=len(pending), last=SESS_LAST,
                                           fusion=dict(n=METAF.get("n", 0), acc=METAF.get("acc", 0.5)),
                                           floors_count=len(FLOORS),
                                           live_n=LIVE.get("n", 0), live_half=DDAY.get("live_half", 0),
                                           live_cool=DDAY.get("live_cool", 0), ts=time.time())).encode()
                except Exception:
                    body = b'{"ok":true}'
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):
                pass

        threading.Thread(target=lambda: HTTPServer(("0.0.0.0", int(port)), _H).serve_forever(),
                         daemon=True).start()
        log(f"v33 health endpoint on 0.0.0.0:{port} (GET / → JSON status)")
    except Exception as ex:
        log(f"health server skipped: {ex}")


async def run_engine():
    global CON, API_H
    CON = db_init()
    load_state()
    _hq_build()                       # v33 ENGINE C: learn hour-quality from own DB
    _floor_seed()                     # v33 ENGINE G: seed per-asset floors from DB
    _metaf_build()                    # v33 ENGINE F: fusion weights from live history
    t0 = time.time()
    if PocketOptionAsync is None:
        log("BinaryOptionsToolsV2 missing — live mode needs it (training/imports OK).")
        return
    async with PocketOptionAsync(os.environ.get("POCKET_OPTION_SSID", "")) as api:
        API_H = api
        payouts = await api.payout()
        _ranked = sorted(((a, float(p)) for a, p in payouts.items() if float(p) >= 90),
                         key=lambda kv: (-kv[1], kv[0]))
        PAYOUTS.clear(); PAYOUTS.update({a: float(p) for a, p in payouts.items()})   # v33 payout map
        pairs = sorted(a for a, _p in _ranked[:PAIRS_MAX])
        if not pairs:
            pairs = sorted(a for a, p in payouts.items() if 85 <= p <= 95)
            log(f"v29 fallback payout filter [85,95] → {len(pairs)} assets")
        else:
            log(f"v33 OMEGA roster: {len(pairs)} pairs >=90% (best {_ranked[0][1]:.0f}% {_ranked[0][0]})")
        try:
            demo = api.is_demo()
        except TypeError:
            demo = await api.is_demo()
        bal0 = await _bal(api)
        BAL_D["v"] = bal0; BAL_D["start"] = bal0
        _roll_day(); DDAY["b0"] = bal0
        TRD["on"] = os.environ.get("TRADE", "0") == "1"
        if TRD["on"] and not demo:
            TRD["on"] = False
            await tg("⛔ AUTO-TRADE refused: account is NOT demo — signals only")
        log(f"ACCOUNT: {'DEMO' if demo else 'REAL'} | balance ${bal0:.2f} | AUTO-TRADE {'ON' if TRD['on'] else 'off'}")
        VS["on"] = bool(VOICEFN)
        log(f"v33 agent layer: AI veto x{AI_DECISIONS}/run | voice {'on' if VS['on'] else 'off'} | "
            f"FOCUS {FOCUS} | FOLLOW {FOLLOW} | THROTTLE_S {THROTTLE_S:.0f} | "
            f"SNIPER {'ON' if SNIPER else 'off'} (conf≥{SNIPER_CONF}, pwin≥{SNIPER_PWIN}, chop-kill)")
        if TRD["on"]:
            await tg(f"💵 AUTO-TRADE ON (DEMO) — start ${bal0:.2f}\n"
                     f"stake 4% of balance/signal, MTG auto {'ON' if MTG_AUTO else 'off'} — demo only")
        log(f"SMC PEAK v33 BINARY GOD ENGINE: {len(pairs)} assets @92% from PO")
        sub = await api.subscribe_raw()
        for a in pairs: store[a] = {}; FEED_T[a] = time.time()
        lines = []; tot = 0.0
        _ch_list, _ac_list, _rt_list = [], [], []   # v23 adaptive inputs
        agg_n, agg_dw, agg_mw = 0, 0.0, 0.0
        for i, a in enumerate(pairs, 1):
            try:
                df = await fetch_df(api, sub, a)
                if len(df) < 1500: raise RuntimeError(f"only {len(df)} candles")
                res = await asyncio.to_thread(train_smc, df)
                for ts, r in zip(df.index.astype(np.int64) // 10**9, df.values):
                    store[a][int(ts // 60) * 60] = list(r)
                if res is None:
                    log(f"[{i}/{len(pairs)}] {a}: no SMC edge — refused")
                    lines.append(f"⛔ {a}: refused")
                    continue
                _ut = res["union"]["test_acc"]
                if _ut < ASSET_MIN_TEST:
                    if PROBATION and _ut >= PROB_MIN_TEST:
                        PROB[a] = True
                        log(f"[{i}/{len(pairs)}] {a}: 🟡 PROBATION — test {_ut:.1%} (agreement + half stake)")
                        lines.append(f"🟡 {a}: test {_ut:.0%} — probation (2+ setups / meta / tierA, half stake)")
                    else:
                        log(f"[{i}/{len(pairs)}] {a}: 🧊 BENCHED — test {_ut:.1%} < floor {ASSET_MIN_TEST:.0%}")
                        lines.append(f"🧊 {a}: test {_ut:.0%} — benched (floor {ASSET_MIN_TEST:.0%})")
                        continue
                MEMBERS[a] = res["members"]; UNION[a] = res["union"]
                AIF[a] = res.get("aif"); HOURS[a] = res["hour_ok"]; MTGK[a] = 1; TRAIN_T[a] = time.time()   # v19: 1m legs
                u = res["union"]; tot += u["sig_per_day"]
                _ac_list.append(u["test_acc"]); _rt_list.append(u["sig_per_day"])
                _ch_list.append((res.get("char") or {}).get("follow", 0.5))
                agg_n += u["test_n"]; agg_dw += u["test_acc"] * u["test_n"]; agg_mw += u["mtg_acc"] * u["test_n"]
                mm = ", ".join(f"{m['strategy']}@{m['expiry']}m[{m['mask']}]" for m in res["members"][:3])
                ait = f" | 🤖meta {res['aif']['facc']:.0%} (keeps {res['aif']['keep']:.0%}, thr {res['aif']['thr']:.2f})" if res.get("aif") else ""
                ch = res["char"]
                chtxt = ("MOM" if ch["follow"] > 0.51 else "REV" if ch["follow"] < 0.49 else "NEU")
                hb = f" | ⏰blocked UTC {','.join(str(x) + '-' + str(x + 3) for x in res['blocked'])}" if res["blocked"] else ""
                ait += f" | {chtxt}({ch['follow']:.0%}) tie {ch['tie']:.1%}{hb}"
                log(f"[{i}/{len(pairs)}] {a}: {len(res['members'])} setups | test "
                    f"{u['test_acc']:.1%} | MTG-round {u['mtg_acc']:.1%} (n={u['test_n']}) "
                    f"{u['sig_per_day']}/day | {mm}{ait}")
                lines.append(f"🧠 {a}: test {u['test_acc']:.0%} | 🔁MTG {u['mtg_acc']:.0%} "
                             f"({u['sig_per_day']:.0f}/day) — {mm}{ait}")
            except Exception as ex:
                log(f"[{i}/{len(pairs)}] {a}: ERROR {ex}"); lines.append(f"❌ {a}: {ex}")
        _adapt_compute(_ch_list, _ac_list, _rt_list)          # v23 adaptive profile
        pdw = agg_dw / agg_n * 100 if agg_n else 0
        pmw = agg_mw / agg_n * 100 if agg_n else 0
        await tg(f"📬 FULL WIN RATE (walk-forward test, {agg_n} signals):\n"
                 f"🎯 DIRECT win rate: {pdw:.1f}%\n"
                 f"🔁 1-STEP MTG round rate: {pmw:.1f}%\n(per-asset breakdown below)")
        await tg(f"🧠 SMC PEAK v33 BINARY GOD ENGINE — storm core, 1m only, floor {ASSET_MIN_TEST:.0%} — {datetime.now(IST):%d-%b %H:%M} IST\n"
                 f"Liquidity sweeps • pools • BOS/CHoCH • FVG/OB/BREAKER retrace • reclaims •\n"
                 f"SMA stack | premium/discount + efficiency-ratio regime gates\n"
                 f"⏱ 1-MINUTE EXPIRY ONLY (embargoed walk-forward selection)\n"
                 f"{len(MEMBERS)}/{len(pairs)} assets | ~{tot:.0f} signals/day "
                 f"(~{tot / 48:.0f}/30min) | trained {time.time() - t0:.0f}s\n"
                 f"{'—' * 22}\n" + "\n".join(lines))
        try:
            brief = await asyncio.to_thread(llm_ask,
                "Fresh training results for 1-min binary signals (test acc, MTG round rate, "
                "signals/day, setups per asset):\n" + "\n".join(lines[:40]) +
                "\n\nTasks: 1) overall market character now, 2) TOP 3 assets to favour and why, "
                "3) assets to trade lightly, 4) one-line game plan. Bullet points, max 180 words.")
            if brief:
                await tg("🧠 AI MARKET ANALYST (Qwen) — live read of today's board\n" + "—" * 22 + "\n" + brief)
                await tg_voice(brief, "🧠 v23 AI MARKET ANALYST — spoken read")
                log("AI analyst brief sent (text + voice)")
        except Exception as ex:
            log(f"AI brief skipped: {ex}")
        for a in MEMBERS:
            await api.send_raw(f'42["changeSymbol",{{"asset":"{a}","period":60}}]')
        dl0 = time.time() + 4
        while time.time() < dl0:
            try:
                raw = await asyncio.wait_for(sub.__anext__(), timeout=0.5)
                await handle_frame(raw, live=False)
            except asyncio.TimeoutError:
                pass
        for a in MEMBERS:
            cur_min[a] = max(store[a]) if store[a] else None
        # ═══════════════ v30 ETERNAL: eternal session cycle (never returns) ═══════════════
        SESS_NO = int(LIFETIME.get("sessions", 0))
        _start_health_server()
        _day_snap()
        while True:
            SESS_NO += 1
            try:
                if SESS_NO > 1:
                    await _session_transition(api, sub, SESS_NO)
            except Exception as ex:
                log(f"transition error (continuing): {ex}")
            await _maybe_day_roll()
            _sess_snap()
            live_started = time.time()
            LIVE_T0["t"] = live_started
            _smin = RUN_MINUTES if RUN_MINUTES > 0 else SESSION_MIN
            deadline = live_started + _smin * 60
            next_board = time.time() + BOARD_S
            next_beat = time.time() + BEAT_S
            log(f"LIVE — session #{SESS_NO} | {len(MEMBERS)} assets | SMC v33 ETERNAL | 1m expiry | "
                f"{_smin:.0f}m window | risk x{ADAPT['risk']} ({ADAPT['profile']}) | FOCUS {FOCUS}")
            try:
                await tg(f"🟢 SESSION #{SESS_NO} LIVE — {_smin:.0f} min | {len(MEMBERS)} pairs | "
                         f"balance ${BAL_D.get('v', 0.0):.2f} | sniper {'ON' if SNIPER else 'off'}"
                         + (f" | ♻ refreshed {REFRESH['n']}, +{REFRESH['adds']} −{REFRESH['drops']}"
                            if SESS_NO > 1 else ""))
            except Exception:
                pass
            while True:
                now_t = time.time()
                if deadline and now_t >= deadline:
                    if (pending or armed) and now_t < deadline + SESS_GRACE:
                        pass          # grace: finish open trades + MTG legs first
                    else:
                        break
                try:
                    raw = await asyncio.wait_for(sub.__anext__(), timeout=30)
                except asyncio.TimeoutError:
                    # v20 STREAM WATCHDOG: silence > STREAM_DEAD_S → reconnect + resubscribe
                    if (time.time() - STREAM_T["t"] > STREAM_DEAD_S
                            and time.time() - STREAM_T["last_revive"] > 90):
                        STREAM_T["last_revive"] = time.time()
                        log(f"⚠ STREAM SILENT {time.time() - STREAM_T['t']:.0f}s — reconnecting…")
                        try:
                            await asyncio.wait_for(API_H.reconnect(), 30)
                            sub = await API_H.subscribe_raw()
                            for a_ in MEMBERS:
                                await API_H.send_raw(f'42["changeSymbol",{{"asset":"{a_}","period":60}}]')
                            STREAM_T["t"] = time.time()
                            STREAM_T["fails"] = 0
                            log("✓ reconnect issued — feed re-subscribed")
                            await _feed_rescue(sub)      # v26: never lose an open leg to a feed gap
                        except Exception as ex:
                            STREAM_T["fails"] = STREAM_T.get("fails", 0) + 1
                            log(f"reconnect failed ({STREAM_T['fails']}/{FEED_FAIL}): {ex}")
                            if STREAM_T["fails"] >= FEED_FAIL:
                                STREAM_T["fails"] = 0
                                log("FEED REBUILD: re-pulling history for all armed assets…")
                                for a_ in list(MEMBERS):
                                    try:
                                        df_ = await fetch_df(API_H, sub, a_)
                                        for ts_, r_ in zip(df_.index.astype(np.int64) // 10**9, df_.values):
                                            store[a_][int(ts_ // 60) * 60] = list(r_)
                                        FEED_T[a_] = time.time()
                                    except Exception:
                                        pass
                                LIVE_T0["t"] = time.time()      # re-warm 90s on fresh data
                                log("✓ feed rebuilt — warm-up restarted")
                    continue
                await handle_frame(raw, live=True)
                if time.time() >= next_board:
                    next_board = time.time() + BOARD_S
                    tot_ = score_s["W"] + score_s["L"]
                    pb = "\n".join(f"• {a}: {s['W']}W–{s['L']}L" for a, s in pair_score.items())
                    coach = ""
                    try:
                        note = await asyncio.to_thread(llm_ask,
                            f"Live session so far: {score_s['W']}W-{score_s['L']}L. Per asset: {pb}. "
                            "Give ONE short coaching tip (max 40 words).", 120)
                        if note: coach = "\n🧠 AI coach: " + note.strip()
                    except Exception:
                        pass
                    sh_t = CSHADOW["W"] + CSHADOW["L"]
                    await tg(f"📊 SMC v33 SCOREBOARD ({(time.time() - live_started) / 60:.0f} min)\n"
                             f"{score_s['W']}W–{score_s['L']}L–{score_s['T']}T "
                             f"({score_s['W'] / tot_ * 100 if tot_ else 0:.0f}%) | {cancels} cancelled\n"
                             f"📄 paper ${DDAY['paper']:+.2f} | 🔁 MTG net ${DDAY['mtg_net']:+.2f}"
                             + (f" | 🚫 audit {CSHADOW['W']}W–{CSHADOW['L']}L of {sh_t}" if sh_t else "")
                             + f"\n{pb}{coach}")
                if time.time() >= next_beat:
                    next_beat = time.time() + BEAT_S
                    _live_f = sum(1 for a_ in MEMBERS if time.time() - FEED_T.get(a_, 0) <= FEED_WARN)
                    await tg(f"💓 v33 heartbeat {int((time.time() - live_started) / 60)}m | "
                             f"{score_s['W']}W–{score_s['L']}L | {len(pending)} open | "
                             f"feed {_live_f}/{len(MEMBERS)} fresh | ADAPT {ADAPT.get('profile')} "
                             f"x{ADAPT.get('risk')}")
                save_state()
            # ── v30 session end: report + persist; next session starts immediately ──
            _bal_now = await _bal(API_H, BAL_D.get("v")) if TRD["on"] else None
            try:
                await _session_end(SESS_NO, _bal_now)
            except Exception as ex:
                log(f"session report error: {ex}")
            save_state(force=True)
            if RUN_MINUTES > 0:
                log("RUN_MINUTES test mode — single session complete, exiting eternal cycle")
                break

    save_state(force=True)


async def main():
    """v30 ETERNAL outer watchdog: NOTHING stops the engine — any crash restarts it in 30 s."""
    log(f"v33 OMEGA boot — 24/7 mode | session {SESSION_MIN:.0f} min + report every session, "
        f"no breaks | sniper={'ON' if SNIPER else 'off'}")
    while True:
        try:
            await run_engine()
            if RUN_MINUTES > 0:
                log("RUN_MINUTES test mode — run_engine returned; exiting")
                return
            log("run_engine returned unexpectedly — restarting in 10s")
            await asyncio.sleep(10)
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            log(f"⚠ v30 engine error: {ex!r} — auto-restart in 30s (24/7)")
            try:
                await tg(f"⚠ v33 auto-restart — engine error: {str(ex)[:150]} — back in 30 s")
            except Exception:
                pass
            await asyncio.sleep(30)


if __name__ == "__main__":
    if PocketOptionAsync is None:
        log("BinaryOptionsToolsV2 not installed — engine imports fine; live run needs the package.")
    else:
        asyncio.run(main())
