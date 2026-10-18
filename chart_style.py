"""Premium edge-to-edge dark chart rendering for PO candle series (v2)."""
import io
import numpy as np
from datetime import datetime, timezone, timedelta

import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

IST = timezone(timedelta(hours=5, minutes=30))

BG     = "#0d1017"
GRID   = "#1d2433"
UP     = "#00c896"
DOWN   = "#ff4d5e"
TEXT   = "#e8eaf0"
MUTED  = "#8b93a7"
GOLD   = "#f0b90b"

_mc = mpf.make_marketcolors(up=UP, down=DOWN,
                            edge={"up": UP, "down": DOWN},
                            wick={"up": UP, "down": DOWN})
_style = mpf.make_mpf_style(
    base_mpf_style="nightclouds", marketcolors=_mc,
    facecolor="none", figcolor=BG, edgecolor=BG,
    gridcolor=GRID, gridstyle=":", gridaxis="horizontal",
    rc={"font.size": 10, "font.family": "DejaVu Sans",
        "axes.labelcolor": TEXT, "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.edgecolor": BG},
)

def render_chart(asset: str, series: dict, payout: int = 92, show: int = 100,
                 figsize=(12.8, 7.2), candle_width=0.85):
    rows = []
    for ts in sorted(series):
        o, h, l, c = series[ts]
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(IST).replace(tzinfo=None)
        rows.append({"Date": dt, "Open": o, "High": h, "Low": l, "Close": c})
    df = pd.DataFrame(rows).set_index("Date").sort_index().tail(show)
    if len(df) < 5:
        return None, None

    last = df.iloc[-1]
    first_open = df.iloc[0]["Open"]
    chg = last["Close"] - first_open
    chg_pct = chg / first_open * 100
    t0, t1 = df.index[0], df.index[-1]
    up_last = last["Close"] >= last["Open"]
    hi_val, lo_val = df["High"].max(), df["Low"].min()
    hi_pos = int(np.argmax(df["High"].values))
    lo_pos = int(np.argmin(df["Low"].values))
    n = len(df)

    fig, axes = mpf.plot(
        df, type="candle", style=_style, figsize=figsize,
        ylabel="", datetime_format="%H:%M", xrotation=0, returnfig=True,
        scale_padding={"left": 0.05, "right": 0.85, "top": 0.42, "bottom": 0.42},
        tight_layout=False,
        update_width_config=dict(candle_width=candle_width, candle_linewidth=0.5),
    )
    ax = axes[0]

    # ---- edge-to-edge layout: header/footer live INSIDE the canvas ----
    ax.set_position([0.005, 0.075, 0.925, 0.785])  # edge-to-edge plot, header band above
    ax.set_xlim(-0.9, n - 0.1 + n * 0.005)

    # rich vertical gradient background inside plot
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(grad, extent=[*ax.get_xlim(), *ax.get_ylim()], aspect="auto",
              cmap=plt.matplotlib.colors.LinearSegmentedColormap.from_list(
                  "bgg", ["#182033", "#0d1017"]),
              alpha=0.9, zorder=-10)

    # soft glow under the close line
    ax.fill_between(range(n), df["Close"].values, df["Low"].min(),
                    color=(UP if chg >= 0 else DOWN), alpha=0.05, zorder=0)

    # gold accent line at very top + watermark
    fig.lines.append(plt.Line2D([0.0, 1.0], [0.997, 0.997], transform=fig.transFigure,
                                color=GOLD, lw=2.2, solid_capstyle="butt"))
    ax.text(0.5, 0.45, asset.replace("_otc", "").replace("#", ""),
            transform=ax.transAxes, ha="center", va="center",
            fontsize=78, fontweight="bold", color=TEXT, alpha=0.045, zorder=0)

    # ---- in-chart header (top-left) ----
    name = asset.replace("_otc", "").replace("#", "")
    fig.text(0.012, 0.952, name, fontsize=25, fontweight="bold", color=TEXT, va="top")
    fig.text(0.012, 0.898, "OTC  •  M1  •  1-minute candles", fontsize=10.5,
             color=MUTED, va="top")
    fig.text(0.205, 0.898, f" Payout {payout}% ", fontsize=10.5, fontweight="bold",
             color="#0d1017", va="top",
             bbox=dict(boxstyle="round,pad=0.28", fc=GOLD, ec="none"))

    # ---- in-chart price block (top-right) ----
    chg_color = UP if chg >= 0 else DOWN
    arrow = "▲" if chg >= 0 else "▼"
    fig.text(0.936, 0.952, f"{last['Close']:g}", fontsize=24, fontweight="bold",
             color=chg_color, ha="right", va="top")
    fig.text(0.936, 0.898, f"{arrow} {abs(chg):.5g}  ({chg_pct:+.2f}%)   •   "
             f"{t0:%d %b %Y}  {t0:%H:%M}–{t1:%H:%M} IST",
             fontsize=10.5, fontweight="bold", color=chg_color, ha="right", va="top")

    # ---- session high / low markers (placement avoids header/edges) ----
    def _side(pos):
        if pos < n * 0.30:  return dict(ha="left",  xytext=(8, -2))
        if pos > n * 0.70:  return dict(ha="right", xytext=(-8, -2))
        return dict(ha="center", xytext=(0, 9))
    s = _side(hi_pos)
    ax.annotate(f"HIGH {hi_val:g}", xy=(hi_pos, hi_val), textcoords="offset points",
                fontsize=8.5, fontweight="bold", color=UP, zorder=15, va="bottom", **s)
    ax.scatter([hi_pos], [hi_val], marker="^", s=22, color=UP, zorder=15)
    s = _side(lo_pos)
    s["xytext"] = (s["xytext"][0], -4)
    ax.annotate(f"LOW {lo_val:g}", xy=(lo_pos, lo_val), textcoords="offset points",
                fontsize=8.5, fontweight="bold", color=DOWN, zorder=15, va="top", **s)
    ax.scatter([lo_pos], [lo_val], marker="v", s=22, color=DOWN, zorder=15)

    # ---- last price dotted line + pill ----
    lp = last["Close"]
    ax.axhline(lp, color=chg_color, lw=0.9, ls=(0, (5, 4)), alpha=0.8, zorder=10)
    ax.annotate(f" {lp:g} ", xy=(1.0, lp), xycoords=("axes fraction", "data"),
                xytext=(3, 0), textcoords="offset points", va="center", ha="left",
                fontsize=10.5, fontweight="bold", color="#0d1017", zorder=25,
                annotation_clip=False,
                bbox=dict(boxstyle="round,pad=0.3", fc=(UP if up_last else DOWN), ec="none"))

    # cosmetics
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, labelsize=9.5)
    ax.yaxis.tick_right()
    ax.margins(x=0)

    # footer strip
    fig.text(0.008, 0.014,
             f"IST (UTC+5:30)  •  {n} candles  •  last candle forming  •  PocketOption live chart feed",
             color=MUTED, fontsize=9)
    fig.text(0.992, 0.014, "BinaryOptionsTools-v2", color="#3c4356",
             fontsize=8.5, ha="right")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160, facecolor=BG)
    plt.close(fig)
    buf.seek(0)

    cap = (f"{'🟢' if chg >= 0 else '🔴'} {asset}  •  M1  •  {payout}% payout\n"
           f"O {last['Open']:g}   H {last['High']:g}   L {last['Low']:g}   C {last['Close']:g}\n"
           f"Session H {hi_val:g} / L {lo_val:g}  •  Δ {chg:+.5g} ({chg_pct:+.2f}%)\n"
           f"🕐 {t0:%H:%M} – {t1:%H:%M} IST  •  last candle forming")
    return buf.read(), cap
