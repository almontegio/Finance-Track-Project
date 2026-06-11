"""Follow-up tests answering reader questions on REPORT.md.

A) Is DCA better than lump sum on individual dividend stocks? (No - worse.)
B) Does the 10-month SMA filter work on individual blue chips? (As a drawdown
   reducer yes, as a return enhancer only for boom-bust names.)
C) Does a simple equal-weight dividend-payer basket beat the index? (Yes,
   1995-2021, price-only +4.3pp/yr before counting its higher dividend yield;
   but it lagged in the 2010-2021 bull decade.)

Run: python3 pse_research/followup_tests.py
"""

import sys
import os

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from backtest import (COST_HIST, dca_vs_lumpsum, load, metrics, sma_timing)

DIV_BASKET = ["TEL", "MER", "GLO", "MBT", "BPI"]


def main():
    monthly, turnover, _ = load()
    psei_m = monthly["PSEI"].dropna()

    print("A) DCA vs lump sum, individual dividend stocks, 5y rolling windows")
    for sym in ["TEL", "MER", "GLO", "MBT", "BPI", "BDO", "SCC", "AP", "ALI"]:
        s = monthly[sym].dropna()
        if len(s) < 120:
            continue
        df = dca_vs_lumpsum(s, 5)
        print(f"   {sym:4s} n={len(df):3d} | DCA wins {(df['ratio'] > 1).mean()*100:4.0f}% "
              f"| median DCA/LS wealth ratio {df['ratio'].median():.3f}")

    print("\nB) 10-month SMA filter per stock vs B&H same stock (hist costs, cash 4%)")
    for sym in ["ICT", "SM", "JFC", "TEL", "MER", "ALI", "MBT", "URC", "SMPH", "BDO"]:
        s = monthly[sym].dropna()
        if len(s) < 150:
            continue
        eq, trades, _ = sma_timing(s, 10, COST_HIST, 0.04)
        ms, mb = metrics(eq), metrics(s.iloc[10:])
        print(f"   {sym:4s} SMA {ms['CAGR']*100:6.2f}%/{ms['MaxDD']*100:5.1f}%  "
              f"B&H {mb['CAGR']*100:6.2f}%/{mb['MaxDD']*100:5.1f}%  (CAGR/MaxDD)")

    print("\nC) Equal-weight dividend basket (TEL MER GLO MBT BPI), annual rebal, 1995+")
    sub = monthly[DIV_BASKET].loc["1995-01-01":]
    ret = sub.pct_change().clip(-0.95, 3.0)
    eq, dates, w = [1.0], [sub.index[0]], None
    for i in range(1, len(sub)):
        r = ret.iloc[i].fillna(0.0)
        cost = 0.0
        if (i - 1) % 12 == 0:
            w = pd.Series(1 / len(DIV_BASKET), index=DIV_BASKET)
            cost = 0.002
        port_r = (w * r).sum() / w.sum()
        w = w * (1 + r)
        eq.append(eq[-1] * (1 + port_r - cost))
        dates.append(sub.index[i])
    eq = pd.Series(eq, index=dates)
    for label, e, b in [("1995-2021", eq, psei_m.loc["1995-01-01":]),
                        ("2010-2021", eq.loc["2010-01-01":], psei_m.loc["2010-01-01":])]:
        m, mb = metrics(e), metrics(b)
        print(f"   {label}: basket {m['CAGR']*100:5.2f}% (MaxDD {m['MaxDD']*100:5.1f}%) "
              f"vs PSEi {mb['CAGR']*100:5.2f}% (MaxDD {mb['MaxDD']*100:5.1f}%) - price-only;"
              f" basket yield ~3-6% vs index ~2-3% widens the gap further")


if __name__ == "__main__":
    main()
