"""Build clean monthly/daily price panels from the carlo01092/pse JSON dump.

Source: https://github.com/carlo01092/pse (public, MIT-less but public data
scraped from PSE EDGE). Daily OHLCV per ticker, 1985-01-02 .. 2021-03-12.

Outputs (written to pse_research/data/):
  psei_daily.csv     - PSEi daily close, 1985-2021
  monthly_close.csv  - month-end close panel, all tickers
  monthly_turnover.csv - median daily peso turnover (close*volume) per ticker-month
  splits_detected.csv  - overnight drops < -33% treated as split/stock-dividend
                         adjustments (heuristic; logged for audit)

Known limitations (documented in REPORT.md):
  * Price-only data - no cash dividends, so all stock/index returns understate
    total return by roughly the dividend yield (~2-3%/yr for the PSEi).
  * Universe is stocks listed as of Mar 2021 - survivorship bias for
    cross-sectional strategies; index-level series (PSEI) is unaffected.
  * Stock dividends/splits are not adjusted in the raw data. We retro-adjust
    overnight close-to-close drops worse than -33% (splits), but smaller stock
    dividends (20-25%) cannot be distinguished from price moves and remain.
"""

import json
import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd

SRC = "/tmp/pse-data2/json"
OUT = os.path.join(os.path.dirname(__file__), "data")
SPLIT_THRESHOLD = -0.33


def load_ticker(path):
    with open(path) as f:
        d = json.load(f)
    if not isinstance(d, dict) or "t" not in d or not d["t"]:
        return None
    idx = pd.to_datetime([datetime.fromtimestamp(t, tz=timezone.utc).date() for t in d["t"]])
    df = pd.DataFrame({"close": np.asarray(d["c"], dtype=float),
                       "volume": np.asarray(d["v"], dtype=float)}, index=idx)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df[df["close"] > 0]
    return df


def adjust_splits(close, sym, log):
    """Back-adjust prices for overnight drops worse than SPLIT_THRESHOLD."""
    ret = close.pct_change()
    events = []
    for dt in ret.index[ret < SPLIT_THRESHOLD]:
        prev = close.loc[:dt].iloc[-2]
        ratio = prev / close.loc[dt]
        events.append((dt, ratio))
        log.append({"symbol": sym, "date": dt.date(), "drop": round(ret.loc[dt], 4),
                    "ratio": round(ratio, 4)})
    adj = close.copy()
    for dt, ratio in events:
        adj.loc[adj.index < dt] /= ratio
    return adj


def main():
    os.makedirs(OUT, exist_ok=True)
    closes, turnovers = {}, {}
    split_log = []

    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".json"):
            continue
        sym = fn[:-5]
        df = load_ticker(os.path.join(SRC, fn))
        if df is None or len(df) < 60:
            continue
        close = df["close"]
        if sym != "PSEI":
            close = adjust_splits(close, sym, split_log)
        closes[sym] = close
        turnovers[sym] = (df["close"] * df["volume"]).resample("ME").median()

    panel = pd.DataFrame(closes)
    psei = panel["PSEI"].dropna()
    psei.to_frame("close").to_csv(os.path.join(OUT, "psei_daily.csv"))

    monthly = panel.resample("ME").last()
    monthly.to_csv(os.path.join(OUT, "monthly_close.csv"))
    pd.DataFrame(turnovers).to_csv(os.path.join(OUT, "monthly_turnover.csv"))
    pd.DataFrame(split_log).to_csv(os.path.join(OUT, "splits_detected.csv"), index=False)

    print(f"tickers: {len(closes)}  PSEI: {psei.index[0].date()} -> {psei.index[-1].date()}")
    print(f"splits/stock-dividends adjusted: {len(split_log)}")


if __name__ == "__main__":
    main()
