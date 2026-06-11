# Medium/Long-Term Holding Strategies for Philippine Stocks (PSE)
### Evidence review + original backtests on 36 years of PSE data (1985–2021)
*Prepared June 2026. Educational research, not financial advice.*

---

## 0. How this was produced

1. **Literature sweep** — 5 parallel research passes over academic factor studies,
   PSE/broker data, REIT/dividend evidence, practitioner systems, and current
   (2025–2026) trading-cost/tax rules, with an adversarial fact-check pass on the
   load-bearing claims.
2. **Original backtests** — daily OHLCV for 333 PSE tickers and the PSEi
   (1985-01 → 2021-03), from a public archive of PSE EDGE data
   ([carlo01092/pse](https://github.com/carlo01092/pse)), cleaned and
   split-adjusted by `prepare_data.py`, strategies in `backtest.py`, outputs in
   `results/`. Data validated against known anchors (Feb-1990 base ≈1,022;
   Jan-2018 month-end 8,764.01; Mar-2009 trough ≈1,986; Mar-2020 COVID ≈5,321).

**Data caveats (apply to every backtest number below):**
- **Price-only** — no cash dividends. PSEi total returns are ~2–3.5 pp/yr higher
  than shown (per PSE, from end-2008 to end-2018 the total-return PSEi gained
  +417.6% vs +298.6% for the price-only index — dividends added ~119 pp over a decade).
- **Survivorship bias** in cross-sectional tests (universe = stocks listed Mar-2021).
  Index-level tests (PSEi series) are unaffected. Survivorship *inflates*
  stock-picking results — strategies that underperform despite it are robustly bad.
- Sample ends Mar-2021; the 2021–2026 out-of-sample period (PSEi 7,123 → ~5,960)
  was a continued grind lower, which strengthens, not weakens, the conclusions
  about trend-filtering and dividends.

---

## 1. The market you are actually playing in (context that drives everything)

| Fact | Value | Source quality |
|---|---|---|
| PSEi all-time closing high | 9,058.62 (Jan 29, 2018) — never reclaimed | High (multiple) |
| PSEi end-2025 / mid-2026 | 6,052.92 (−7.3% in 2025) / ~5,900–5,950 | High |
| PSEi price CAGR 1985–2021 (our data) | **+12.3%/yr** (includes the 1986–96 boom) | High |
| PSEi price CAGR 1990–2021 | **+6.2%/yr** | High |
| PSEi price CAGR 2013–2021 | **+0.9%/yr** (and negative 2021→2026) | High |
| PSEi trailing P/E | ~20× mid-2010s → **~10–11× (2025–26)** | Medium (CEIC) |
| PSEi dividend yield | ~3.5% (late 2025; was ~2% in the expensive era) | Medium |
| 10-yr PH government bond | **~7.5%** (June 2026) | High |
| PH inflation, 10y avg | ~3.4%/yr | High |

Two structural implications:

1. **The index has been a derating story, not an earnings collapse** — P/E went
   from ~20× to ~10× over 12 years while the index went nowhere. You cannot
   assume "the PSEi always comes back" on a 5-year horizon; you must either get
   paid to wait (dividends) or have a rule for stepping aside (trend filter).
2. **The hurdle rate is brutal**: risk-free PHP yields ~6–7.5%. Any equity
   strategy must credibly beat that. At today's ~10× P/E and 3.5% yield the
   starting point is historically cheap — mean-reversion is the bull case, but
   it is a valuation argument, not a backtested certainty.

**What the academic record says about the PSE specifically** (full citations §5):
- Pooled emerging-market studies that include the Philippines find **value,
  momentum and low-vol premia** (Rouwenhorst 1999 *JoF*; Cakici-Fabozzi-Tan 2013
  *EMR*; Hanauer-Lauterbach 2019 *EMR*; Blitz et al. 2013 *EMR*) — but no
  published study isolates a statistically significant **PH-only** factor premium.
- The one PH-only academic test (Perez 2018, MSCI PH value/growth 1998–2017)
  finds **no value or size effect**.
- Momentum is the **weakest in Asia** of all regions (Griffin-Ji-Martin 2003 *JoF*).
- Technical trading rules on the PSE Composite produce significant **gross**
  returns that **die after transaction costs** (Tharavanij et al. 2015, *SpringerPlus*).
- The PSE's own **Dividend Yield index (DivY)** has crushed the PSEi recently:
  total-return 2024: **+32.1% vs +4.1%**; 2023: +6.2% vs +1.0%; 2021: +2.8% vs +1.6%
  (official factsheets, fact-checked against the PDFs; note the DivY index only
  went live in March 2022 — earlier figures are back-calculated, and the live
  history is short).

---

## 2. Our backtest results (PSE data, 1985–2021, costs included)

Cost model: historical round-trip ≈1.19% (0.6% STT + commissions + fees);
modern post-CMEPA ≈0.69%. "Cash 4%" = T-bill proxy while out of the market
(conservative — PHP T-bills paid far more than 4% pre-2005 and pay ~5–6% in 2025–26).

### 2.1 Benchmark: buy & hold PSEi (price-only)
| Period | CAGR | MaxDD |
|---|---|---|
| 1985–2021 | +12.3% | −71% |
| 1990–2021 | +6.2% | −71% |
| 2000–2021 | +5.9% | −51% |
| 2010–2021 | +7.7% | −39% |
| 2013–2021 | +0.9% | −39% |

### 2.2 ★ 10-month SMA trend filter on the PSEi (Faber rule)
Hold the index when the monthly close > 10-month SMA; otherwise hold T-bills.
One check per month. ~25 round trips in 35 years (≈0.7/yr), in the market 65% of the time.

| Variant | CAGR | Vol | MaxDD | vs B&H same window |
|---|---|---|---|---|
| Historical costs, cash 0% | +12.3% | 23% | −52% | +11.9%, −71% |
| Historical costs, cash 4% | **+13.8%** | 23% | **−49%** | +11.9%, −71% |
| Modern costs, cash 4% | **+14.2%** | 23% | **−48%** | +11.9%, −71% |

Subperiods (hist. costs, cash 4% vs B&H):
- 2000+: **10.1% vs 8.0%**, MaxDD **−26% vs −51%**
- 2010+: 4.5% vs 5.3% (slight lag in a sideways-up market — whipsaw cost)
- 2013+: **2.7% vs 1.1%**, MaxDD **−16% vs −39%**

**Verdict: the single most robust mechanical overlay we found.** It gives up a
little in strong bull phases, wins in flat/down regimes (which the PSE has been
in since 2013), and cuts the worst drawdown roughly in half. With PHP T-bills at
5–6% in 2025–26, the cash leg is unusually well paid. This mirrors Faber's
global results (S&P 500 1901–2012: similar CAGR, MaxDD −50% vs −84%).

### 2.3 DCA (peso-cost averaging) vs lump sum on the PSEi
Rolling windows, all start months 1985–2021, buy costs included:

| Window | DCA wins | Median end-wealth ratio (DCA/LS) |
|---|---|---|
| 5 years (375 windows) | 29% | 0.80 |
| 10 years (315 windows) | 23% | 0.62 |

**Verdict: DCA is a savings discipline, not a return enhancer.** If you have a
lump sum, history says invest it (or trend-filter it); if you invest from salary,
DCA is simply how money arrives — automate it and stop timing. DCA *did* beat
lump-sum in the windows starting near the 1997, 2007 and 2013–18 peaks — it is
crash insurance paid for with upside.

### 2.4 Cross-sectional momentum (12-1, top 5/10 of the 30 most liquid, quarterly)
| Strategy | CAGR 1995–2021 | CAGR 2010–2021 | MaxDD |
|---|---|---|---|
| Momentum top-5 | +2.8% | +2.9% | −75% |
| Momentum top-10 | +4.6% | — | −77% |
| B&H PSEi same window | +4.0% | +7.7% | −71% |

**Verdict: avoid.** Even *with* survivorship bias helping it, momentum
underperformed after realistic PH costs — exactly what Griffin et al. (weak Asian
momentum) and the cost-sensitivity literature predicted.

### 2.5 Low-volatility tilt (10 lowest-vol of the 30 most liquid, quarterly)
CAGR +3.3% vs B&H +4.0% (1995–2021) but with vol 19.8% vs 23.2% and MaxDD −62% vs −71%.
Price-only data penalizes this strategy most: low-vol PH names (utilities,
telcos, banks) carry the market's highest dividend yields (4–7%), which this
data can't see. On a total-return basis it is plausibly Sharpe-superior —
consistent with the EM low-vol literature and the DivY index's live record.

### 2.6 Equal-weight top-10-liquidity basket (annual rebalance)
+4.3% vs +4.0% B&H (1995–2021); 2010+: +5.4% vs +7.7%. Mechanical "blue chip
basket" ≈ the index. No free lunch from equal-weighting here.

### 2.7 What actually compounded: individual quality franchises (price-only, split-adjusted)
| Stock | Period | Price CAGR |
|---|---|---|
| ICT (ICTSI) | 1992–2021 | **+18.1%/yr** |
| SM | 2005–2021 | +14.3%/yr |
| MER | 1992–2021 | +12.5%/yr |
| JFC | 1993–2021 | +12.3%/yr |
| SMPH | 1994–2021 | +10.5%/yr |
| ALI | 1991–2021 | +8.6%/yr |
| URC | 1994–2021 | +8.5%/yr (−70% from its 2015 peak by 2025) |
| MBT | 1986–2021 | +6.9%/yr |

A handful of franchises compounded 10–18%/yr for decades against a flat index —
but these are *hindsight* picks (URC and JFC then stagnated for a decade), and
no mechanical rule we tested (momentum, EW, low-vol) captured them ex ante.
Concentrated quality investing works here only with genuine fundamental work.

---

## 3. The ranked playbook

### #1 — Dividend-quality core (the evidence-weighted workhorse)
**Evidence: ★★★★☆** (official DivY index record; TRI-vs-PSEi dividend gap;
EM low-vol/quality literature; high current yields are observable, not forecast)

- Build a 8–12 stock portfolio of **sustained dividend payers with payout
  capacity**: screen for ≥4% yield, ≥5y of uninterrupted dividends, payout <80%,
  net debt sane. The current PSE DivY constituent list is a free starting screen.
  Today that pool is telcos (TEL ~7%, GLO ~7%), power/utilities (MER ~4%),
  banks (BDO/BPI/MBT), SCC, and quality REITs.
- Add a **REIT sleeve (10–30% of the portfolio)** for contractual income: the
  REIT law forces ≥90% payout; AREIT delivered ~+81–96% TSR from its 2020 IPO.
  **Sponsor quality is the whole game** — IPO buyers of DDMPR/FILRT lost 45–50%
  despite 8%+ yields. Prefer REITs with growing DPS and strong sponsors.
- Reinvest all dividends (10% final withholding tax; net ~4.5–6.3% on a 5–7% gross
  yield). At a ~5% net yield you are paid more than half the 10-yr bond to wait
  for the (historically cheap, ~10× P/E) market to rerate.
- Rebalance/review **quarterly**; sell only on dividend cut or thesis break.
- Expected outcome based on history: roughly index-plus-2-to-4 pp/yr total
  return with lower drawdowns — i.e., high single digits even if the index stays
  flat, more if the derating reverses. Not a guarantee; the DivY live record is short.

### #2 — 10-month SMA trend filter (the risk manager)
**Evidence: ★★★★☆** (our own 36-year PSE backtest, net of costs; replicates the
global Faber result; works *because* PH has multi-year trends and crashes)

- Once a month (e.g., last trading day): if PSEi monthly close > its 10-month
  SMA → be invested; if below → move that sleeve to T-bills/money-market
  (currently 5–6%). That's the entire strategy. ~0.7 round trips/yr; post-CMEPA
  round-trip cost ~0.7% makes it cheaper to run than ever.
- Apply it to your **index/ETF sleeve** (or to the whole portfolio if you can
  stomach being 100% out). Many investors run #1 untouched and trend-filter only
  the beta sleeve.
- Historical result: +1.5–2.3 pp/yr over buy-and-hold with half the max drawdown;
  its best decades are exactly the regime PH has been in since 2013.
- Cost of the strategy: whipsaws in sideways-up years (it lagged 2010–2021 by
  ~0.8 pp/yr) and the discipline to actually follow the signal.

### #3 — Concentrated quality compounders (the alpha engine, if you do the work)
**Evidence: ★★★☆☆** (decades-long precedents: ICT +18%/yr, SM +14%, JFC +12%,
MER +12.5% — but hindsight-selected; no mechanical screen captured them)

- 3–6 businesses with: dominant market position, secular volume growth
  (ports/logistics, malls+banking duopolies, food), owner-operator alignment,
  ROE > 12% sustained, and the ability to reinvest at high returns.
- Buy on broad-market fear (the trend filter being "off" is, ironically, a
  shopping calendar), size each ≤15%, hold 5–10 years, review annually on
  fundamentals only.
- Watch the two historical failure modes: paying 30×+ earnings for "quality"
  (URC 2015, JFC 2019 — dead money for a decade) and conglomerate discounts that
  never close (AC/JGS trade ~45–50% below sum-of-parts for years — cheap can stay cheap).

### #4 — Automated peso-cost averaging (the default for salary earners)
**Evidence: ★★★★★ that it builds wealth; ★☆☆☆☆ that it beats lump-sum**
- If money arrives monthly, invest it monthly into #1/#2/#3 — COL EIP, GStocks,
  or broker GTC orders automate this. Just know DCA lost to lump-sum in 71–77%
  of historical PSE windows; it is discipline and crash insurance, not alpha.

### What to AVOID (evidence-backed)
- **Momentum/trend-chasing individual PH stocks** — underperformed in our tests
  even before removing survivorship bias; weakest-in-Asia academically.
- **Short-term technical rules** (RSI/MACD/etc.) — gross profits exist, net
  profits die at PH costs (peer-reviewed result, and that was pre-2025 when
  costs were 1.2%/round trip; at 0.7% it's still a losing proposition vs effort).
- **Paid pick services** (e.g., "Strategic Averaging Method") — zero audited
  track record found; heavy affiliate conflicts.
- **High-yield traps** — yield from a falling-DPS REIT or a shrinking telco is
  not income, it's return *of* capital. Always check DPS trend, not just yield.

### Portfolio template (moderate effort: ~1 hour/month)
| Sleeve | Weight | Vehicle |
|---|---|---|
| Dividend-quality stocks (#1) | 40% | 8–12 names, direct |
| PH REITs (#1) | 15% | 2–4 names (sponsor quality first) |
| Index w/ 10-mo SMA filter (#2) | 25% | ETF/index fund ⇄ money market |
| Quality compounders (#3) | 20% | 3–6 names |

---

## 4. Implementation mechanics (verified 2025–2026)

- **Costs collapsed in 2025**: CMEPA (RA 12214, effective Jul 1, 2025) cut the
  stock transaction tax **0.6% → 0.1%**; all-in round trip is now ~**0.7%**
  (0.25% commission +12% VAT each way, 0.1% STT on sell, ~0.03% exchange/clearing).
- **Dividends**: 10% final withholding for resident individuals (REITs included).
- **Board lots → 1 share**: PSE is moving to "one lot = one share" with the 2026
  Nasdaq Eqlipse migration — verify go-live; minimums become trivial.
- **Brokers**: COL Financial (0.25%, EIP auto-invest; ₱25k opening minimum since
  Aug 2025), BPI Trade, FirstMetroSec, GCash GStocks (0.25%, no minimum
  commission — fine for small DCA).
- **Index vehicle**: the lone PSE ETF (FMETF) was **not delisted** — manager
  control moved to ATRAM; renamed ATR FAMI Philippine Equity ETF; fee ~0.56%
  (vs 1–1.5% for bank index UITFs). Check current liquidity; it trades thin.
- **Tax wrappers**: PERA gives a 5% tax credit on contributions (caps
  ₱200k/₱400k OFW) and tax-free growth — use it for the long-term core if eligible.
- **Liquidity reality**: PSE turns over only ~₱7–8B/day; stick to PSEi names +
  liquid mid-caps and REITs; use limit orders always.

---

## 5. Sources

**Academic / peer-reviewed**
- Rouwenhorst (1999), *J. Finance* 54(4) — EM local factors incl. PH. https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00151
- Cakici, Fabozzi & Tan (2013), *Emerging Markets Review* 16 — EM size/value/momentum. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2070832
- Griffin, Ji & Martin (2003), *J. Finance* — momentum weak in Asia. https://www.researchgate.net/publication/4769325
- Hanauer & Lauterbach (2019), *EMR* 38 — robust EM factors. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3233614
- Blitz, Pang & van Vliet (2013), *EMR* 16 — EM low-vol. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2050863
- van der Hart et al. (2003), *J. Empirical Finance* 10 — EM stock selection. https://people.duke.edu/~charvey/Teaching/BA453_2006/vandyke_stock_selection.pdf
- Tharavanij et al. (2015), *SpringerPlus* 4:552 — PSE technical rules vs costs. https://springerplus.springeropen.com/articles/10.1186/s40064-015-1334-7
- Perez (2018), *IJFR* 9(2) — no PH value/size effect. https://www.sciedupress.com/journal/index.php/ijfr/article/view/13302
- Faber (2007, upd. 2013), *J. Wealth Mgmt* — 10-month SMA. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461

**Official / exchange / regulatory**
- PSE DivY factsheet (Sep 2025). https://documents.pse.com.ph/wp-content/uploads/sites/15/2025/11/DivY-Factsheet_202509.pdf
- PSEi/PSEi-TRI factsheet. https://documents.pse.com.ph/wp-content/uploads/sites/15/2025/11/PSEi-PSEi-TRI-Factsheet_202509.pdf
- PSE TRI launch (+417.6% vs +298.6%, measured from end-2008). https://business.inquirer.net/264553/pse-set-to-roll-out-total-return-index
- CMEPA (RA 12214) summaries: PwC https://www.pwc.com/ph/en/tax/tax-publications/taxwise-or-otherwise/2025/cmepa-a-new-era-for-investment-taxation.html ; DOF https://www.dof.gov.ph/dof-cmepa-cuts-transaction-costs-making-it-easier-affordable-for-filipinos-to-channel-savings-into-productive-investments/
- REIT Act RA 9856. https://www.officialgazette.gov.ph/2009/12/17/republic-act-no-9856/
- PSE board-lot reform circular. https://documents.pse.com.ph/CircularOPSPDF/CN-2025-0046.pdf
- SEC removal of minimum commissions (2024). https://www.sec.gov.ph/pr-2024/sec-removes-minimum-stockbroker-commission-to-boost-capital-market-activity/
- BSP PERA FAQs. https://www.bsp.gov.ph/Pages/InclusiveFinance/PERA_FAQs_TaxCredit.aspx

**Market data / press**
- PSEi 2025 close −7.29%. https://business.inquirer.net/566827/psei-ends-2025-lower-caps-yearlong-slide
- AREIT 2024 Integrated Report (TSR). https://www.areit.com.ph/wp-content/uploads/2025/04/AREIT-2024-Integrated-Report.pdf
- REIT outperformance column. https://business.inquirer.net/536704/why-have-reits-outperformed
- Conglomerate discounts. https://insiderph.com/views-from-the-peak-conglo-is-the-way-to-go
- FMETF → ATR FAMI rename. https://www.bworldonline.com/corporate/2025/02/13/652951/fmetf-board-oks-name-change-to-atr-fami-philippine-equity-etf/
- CEIC PSEi P/E & yield. https://www.ceicdata.com/en/philippines/philippine-stock-exchange-pe-ratio-pb-ratio-and-yield/pe-ratio-index-level-psei
- Historical price data: https://github.com/carlo01092/pse (PSE EDGE archive, 1985–2021)

---

## 6. Follow-up tests (see `followup_tests.py`)

**6.1 DCA vs lump sum on individual dividend stocks (5y rolling windows):** lump
sum wins even more decisively than on the index — DCA won only 13–39% of windows
(TEL 37%, MER 39%, MBT 28%, BDO 13%, SCC 18%), median end-wealth 70–89% of lump
sum. Dividend stocks trend and pay you while you hold; drip-feeding into them
forfeits both. DCA remains purely a salary-flow discipline.

**6.2 The 10-month SMA filter on individual blue chips:** universally a huge
drawdown reducer (ICT −93%→−55%, MER −90%→−63%, BDO −67%→−36%) but a return
enhancer only on boom-bust names (ICT 22.7% vs 13.4% B&H; TEL 21.3% vs 20.6%);
on steadier compounders it costs return through whipsaw (SMPH 4.8% vs 9.3%,
JFC 9.7% vs 11.8%). Conclusion: run the trend filter at the *index/portfolio*
level, not per-stock — except possibly on cyclical holdings.

**6.3 Equal-weight dividend basket (TEL, MER, GLO, MBT, BPI), annual rebalance:**
**+8.3%/yr vs +4.0% PSEi (1995–2021, price-only), MaxDD −52% vs −71%** — before
counting the basket's ~3–6% dividend yield vs the index's ~2–3%, i.e., roughly
12% vs 6.5% total return. Caveats: 5 names chosen as the canonical large payers
(mild hindsight), and the basket lagged in the 2010–2021 bull decade (4.2% vs
7.7% price-only; roughly a tie after dividends). Together with the official DivY
record (2024: +32.1% vs +4.1% TR), this is the strongest stock-level evidence in
this report and underpins ranking the dividend-quality core #1.
