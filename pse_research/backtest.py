"""Backtests of medium/long-term holding strategies on PSE historical data.

Data: pse_research/data/ (built by prepare_data.py), price-only, 1985-2021.

Strategies tested (monthly decisions only - practical for a retail investor):
  1. Buy & hold PSEi (benchmark), full period + subperiods
  2. 10-month SMA trend filter on PSEi (Faber rule), with PH trading costs
  3. Peso-cost averaging (DCA) vs lump sum on PSEi, rolling windows
  4. Cross-sectional momentum (12-1) on the 30 most liquid stocks, quarterly
  5. Low-volatility tilt on the same liquid universe, quarterly
  6. Equal-weight top-10-liquidity blue-chip basket, annual rebalance

Cost model (round-trip, % of traded value):
  historical (pre-Jul 2025): sell 0.6% STT + 0.28% comm+VAT + 0.015% fees = 0.895%
                             buy 0.295% -> round trip ~1.19%
  modern (post-CMEPA):       sell 0.395%, buy 0.295% -> round trip ~0.69%
Cash earns the `cash_rate` annual yield when out of the market (T-bill proxy).
"""

import os

import numpy as np
import pandas as pd

DATA = os.path.join(os.path.dirname(__file__), "data")
OUTD = os.path.join(os.path.dirname(__file__), "results")

COST_HIST = {"buy": 0.00295, "sell": 0.00895}
COST_MODERN = {"buy": 0.00295, "sell": 0.00395}


def load():
    monthly = pd.read_csv(os.path.join(DATA, "monthly_close.csv"), index_col=0, parse_dates=True)
    turnover = pd.read_csv(os.path.join(DATA, "monthly_turnover.csv"), index_col=0, parse_dates=True)
    psei_d = pd.read_csv(os.path.join(DATA, "psei_daily.csv"), index_col=0, parse_dates=True)["close"]
    return monthly, turnover, psei_d


def metrics(series, freq=12):
    """series: equity curve (monthly). Returns dict of performance stats."""
    s = series.dropna()
    ret = s.pct_change().dropna()
    years = (s.index[-1] - s.index[0]).days / 365.25
    cagr = (s.iloc[-1] / s.iloc[0]) ** (1 / years) - 1
    vol = ret.std() * np.sqrt(freq)
    dd = (s / s.cummax() - 1).min()
    sharpe = (ret.mean() * freq) / vol if vol > 0 else np.nan
    return {"CAGR": cagr, "AnnVol": vol, "Sharpe0": sharpe, "MaxDD": dd, "Years": years}


def fmt(d):
    return (f"CAGR {d['CAGR']*100:6.2f}%  Vol {d['AnnVol']*100:5.1f}%  "
            f"Sharpe {d['Sharpe0']:5.2f}  MaxDD {d['MaxDD']*100:6.1f}%  ({d['Years']:.1f}y)")


# ---------------------------------------------------------------- strategy 2
def sma_timing(psei_m, n=10, costs=COST_HIST, cash_rate=0.0):
    """Long PSEi when monthly close > n-month SMA, else cash. Signal acted on
    next month's close (no lookahead)."""
    sma = psei_m.rolling(n).mean()
    signal = (psei_m > sma).shift(1).fillna(False)  # position held during month t
    ret = psei_m.pct_change()
    cash_m = (1 + cash_rate) ** (1 / 12) - 1
    strat = pd.Series(np.where(signal, ret, cash_m), index=psei_m.index)
    # costs on switches
    switches = signal.astype(int).diff().fillna(0)
    strat[switches == 1] -= costs["buy"]
    strat[switches == -1] -= costs["sell"]
    eq = (1 + strat.iloc[n:]).cumprod()
    n_trades = int(switches.abs().sum())
    time_in = signal.iloc[n:].mean()
    return eq, n_trades, time_in


# ---------------------------------------------------------------- strategy 3
def dca_vs_lumpsum(psei_m, window_years, buy_cost=0.00295):
    """For each starting month, invest 1 unit/month for window vs all upfront.
    Returns DataFrame of end-wealth ratios (DCA / lump sum)."""
    n = window_years * 12
    rows = []
    for i in range(len(psei_m) - n):
        px = psei_m.iloc[i:i + n + 1].values
        if np.any(~np.isfinite(px)):
            continue
        end = px[-1]
        # DCA: invest 1 peso net of buy cost each month
        shares_dca = np.sum((1 - buy_cost) / px[:-1])
        wealth_dca = shares_dca * end
        # lump sum: n pesos at month 0
        wealth_ls = n * (1 - buy_cost) / px[0] * end
        rows.append({"start": psei_m.index[i], "dca": wealth_dca, "ls": wealth_ls,
                     "ratio": wealth_dca / wealth_ls,
                     "dca_gain": wealth_dca / n - 1, "ls_gain": wealth_ls / n - 1})
    return pd.DataFrame(rows).set_index("start")


# ------------------------------------------------------- cross-sectional base
def liquid_universe(turnover, date, top=30, lookback=12):
    """Top `top` tickers by median monthly turnover over the prior `lookback`
    months (data strictly before `date` - no lookahead)."""
    hist = turnover.loc[:date].iloc[-(lookback + 1):-1]
    if len(hist) < lookback // 2:
        return []
    med = hist.median()
    med = med[med > 0].drop(labels=["PSEI", "PSE"], errors="ignore")
    return med.nlargest(top).index.tolist()


def cross_sectional(monthly, turnover, rank_fn, n_pick, start="1995-01-01",
                    rebalance_months=3, costs=COST_HIST):
    """Generic quarterly-rebalanced equal-weight portfolio of n_pick stocks."""
    dates = monthly.loc[start:].index
    ret = monthly.pct_change()
    equity, eq_dates = [1.0], [dates[0]]
    holdings = []
    for i, dt in enumerate(dates[:-1]):
        nxt = dates[i + 1]
        if i % rebalance_months == 0:
            univ = liquid_universe(turnover, dt)
            scores = rank_fn(monthly, dt, univ)
            new = list(scores.nlargest(n_pick).index) if len(scores) >= n_pick else holdings
            churn = (len(set(holdings) - set(new)) + len(set(new) - set(holdings))) / max(n_pick, 1)
            cost = churn / 2 * (costs["buy"] + costs["sell"])
            holdings = new
        else:
            cost = 0.0
        if not holdings:
            equity.append(equity[-1]); eq_dates.append(nxt); continue
        r = ret.loc[nxt, holdings].astype(float)
        r = r.fillna(0.0).clip(-0.95, 3.0).mean()  # clip residual data errors
        equity.append(equity[-1] * (1 + r - cost))
        eq_dates.append(nxt)
    return pd.Series(equity, index=eq_dates)


def momentum_score(monthly, dt, univ):
    """12-1 momentum: return from t-12 to t-1."""
    hist = monthly.loc[:dt]
    if len(hist) < 13:
        return pd.Series(dtype=float)
    p1, p12 = hist.iloc[-2], hist.iloc[-13]
    score = (p1 / p12 - 1).replace([np.inf, -np.inf], np.nan)
    return score[univ].dropna() if univ else pd.Series(dtype=float)


def lowvol_score(monthly, dt, univ):
    """Negative 36m volatility (higher score = lower vol)."""
    hist = monthly.loc[:dt].iloc[-37:-1]
    if len(hist) < 24:
        return pd.Series(dtype=float)
    vol = hist.pct_change().std()
    score = -vol
    return score[univ].dropna() if univ else pd.Series(dtype=float)


def liquidity_score(monthly, dt, univ):
    """Rank = liquidity itself (equal-weight the biggest liquid names)."""
    return pd.Series({s: -i for i, s in enumerate(univ)})


def main():
    os.makedirs(OUTD, exist_ok=True)
    monthly, turnover, psei_d = load()
    psei_m = monthly["PSEI"].dropna()
    out = []

    print("=" * 78)
    print("1) BUY & HOLD PSEi (price-only; add ~2-3%/yr dividends for total return)")
    for label, start in [("1985-2021", None), ("1990-2021", "1990-01-01"),
                         ("2000-2021", "2000-01-01"), ("2010-2021", "2010-01-01"),
                         ("2013-2021", "2013-01-01")]:
        s = psei_m if start is None else psei_m.loc[start:]
        m = metrics(s)
        out.append({"strategy": f"B&H PSEi {label}", **m})
        print(f"   {label}: {fmt(m)}")

    print("\n2) 10-MONTH SMA TREND FILTER ON PSEi (Faber rule, monthly check)")
    for cash, costs, lbl in [(0.0, COST_HIST, "hist costs, cash 0%"),
                             (0.04, COST_HIST, "hist costs, cash 4%"),
                             (0.04, COST_MODERN, "modern costs, cash 4%")]:
        eq, trades, tim = sma_timing(psei_m, 10, costs, cash)
        m = metrics(eq)
        out.append({"strategy": f"SMA10 PSEi ({lbl})", **m,
                    "trades": trades, "time_in_mkt": tim})
        print(f"   {lbl:24s}: {fmt(m)}  round-trips {trades//2}, in-market {tim*100:.0f}%")
    # matching B&H from same start (after SMA warmup)
    eq, _, _ = sma_timing(psei_m, 10, COST_HIST, 0.0)
    bh_same = metrics(psei_m.loc[eq.index[0]:])
    print(f"   B&H same window         : {fmt(bh_same)}")
    out.append({"strategy": "B&H PSEi (SMA window)", **bh_same})

    print("\n3) DCA (PESO-COST AVERAGING) vs LUMP SUM on PSEi, rolling windows")
    for w in (5, 10):
        df = dca_vs_lumpsum(psei_m, w)
        winrate = (df["ratio"] > 1).mean()
        print(f"   {w}y windows (n={len(df)}): DCA beats lump sum in {winrate*100:.0f}% "
              f"of windows; median end-wealth ratio {df['ratio'].median():.3f}")
        print(f"      median DCA total gain {df['dca_gain'].median()*100:6.1f}% | "
              f"median LS total gain {df['ls_gain'].median()*100:6.1f}%")
        df.to_csv(os.path.join(OUTD, f"dca_vs_ls_{w}y.csv"))
        out.append({"strategy": f"DCA-vs-LS {w}y", "CAGR": np.nan, "AnnVol": np.nan,
                    "Sharpe0": np.nan, "MaxDD": np.nan, "Years": w,
                    "dca_winrate": winrate, "median_ratio": df["ratio"].median()})

    print("\n4) 12-1 MOMENTUM, top-5 of 30 most-liquid, quarterly rebal, hist costs")
    mom = cross_sectional(monthly, turnover, momentum_score, 5)
    m = metrics(mom); out.append({"strategy": "Momentum 12-1 top5", **m})
    print(f"   momentum top5 : {fmt(m)}")
    mom10 = cross_sectional(monthly, turnover, momentum_score, 10)
    m = metrics(mom10); out.append({"strategy": "Momentum 12-1 top10", **m})
    print(f"   momentum top10: {fmt(m)}")
    bh95 = metrics(psei_m.loc["1995-01-01":])
    print(f"   B&H PSEi 1995+: {fmt(bh95)}")

    print("\n5) LOW-VOLATILITY top-10 of 30 most-liquid, quarterly, hist costs")
    lv = cross_sectional(monthly, turnover, lowvol_score, 10)
    m = metrics(lv); out.append({"strategy": "LowVol top10", **m})
    print(f"   low-vol top10 : {fmt(m)}")

    print("\n6) EQUAL-WEIGHT TOP-10 LIQUIDITY BASKET, annual rebal, hist costs")
    ew = cross_sectional(monthly, turnover, liquidity_score, 10, rebalance_months=12)
    m = metrics(ew); out.append({"strategy": "EW top10 liquid", **m})
    print(f"   EW blue chips : {fmt(m)}")

    pd.DataFrame(out).to_csv(os.path.join(OUTD, "summary.csv"), index=False)
    # save equity curves for the report
    pd.DataFrame({"momentum_top5": mom, "momentum_top10": mom10, "lowvol": lv,
                  "ew_liquid": ew}).to_csv(os.path.join(OUTD, "equity_curves.csv"))
    print("\nSaved results/ summary.csv, equity_curves.csv, dca_vs_ls_*.csv")


if __name__ == "__main__":
    main()
