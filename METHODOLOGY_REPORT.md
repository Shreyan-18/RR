# SupeRR Selector Season 2: Round 1 Methodology Report
## Identifying and Ranking the Most Reliable T20 Players Under Pressure

**Competition**: SupeRR Selector Season 2 — Round 1  
**Submission Category**: Player Rankings & Methodology Report  
**Author**: Data Science & Sports Analytics Team  
**Evaluation Dataset**: 200,999 deliveries across 867 IPL & T20I matches (2022–2026)  

---

## Executive Summary

Evaluating clutch performance in cricket requires separating **reputation from empirical reality**. Many celebrated players accumulate statistics in low-leverage phases, while unheralded crisis performers routinely rescue matches when the game is on the line.

This report documents an end-to-end data-driven methodology that evaluates **162 qualified batters** and **243 qualified bowlers** across **200,999 deliveries**. Using a multi-layer framework that models **Macro Match Stakes** (knockouts, 34 tied series deciders, 64 dead rubbers), **Opposition Strength Tiers** (India as Tier 1, Aus/Eng/SA/NZ as Tier 2, etc.), **Global Hostile Fortresses** (680 matches), **In-Game Leverage** (dynamic RRR, balls left, wickets fallen), and **Psychological Momentum** (post-boundary stress, post-wicket surge, 3-match rolling form), we construct the **Composite Pressure Index ($P_{\text{ball}} \in [0, 1]$)**.

Applying a 70th-percentile pressure split, we benchmark each player's performance under high pressure against their normal baseline. We then introduce the **4-Quadrant Permutations Model** to segment players into *Clutch Giants, Crisis Specialists, Front-Runners, and Strugglers*, culminating in the final Top 10 rankings.

---

## 1. Pressure Definition: Situations & Indicators

### 1.1 The Anatomy of Pressure
Pressure in cricket is not an isolated event; it is a compound phenomenon consisting of two interacting forces:
1. **Consequence Severity (Macro Stakes)**: What happens to the team if this match is lost?
2. **Execution Leverage (Micro Situations)**: How close is the contest on this specific delivery, and how narrow is the margin for error?

We formalize this relationship as:
$$P_{\text{ball}} = 0.40 \times C_{\text{macro}} + 0.60 \times S_{\text{micro}}$$
*(With all Super Over deliveries hardcoded to $P = 1.00$.)*

### 1.2 Macro Context Factor ($C_{\text{macro}}$)
Macro pressure exists before the bowler begins their run-up:
$$C_{\text{macro}} = 0.50 \times W_M + 0.35 \times Q_{\text{opp}} + 0.15 \times H_{\text{fortress}}$$

#### A. Match Stakes Taxonomy ($W_M$):
* **Tournament Finals ($1.00$, 15 matches)**: Winner-take-all championship matches.
* **Direct Knockouts ($0.95$, 9 matches)**: Semi-finals and eliminators where defeat means elimination.
* **Playoff Qualifiers ($0.90$, 10 matches)**: High-stakes playoff fixtures.
* **Tied Series Deciders ($0.85$, 39 matches)**: Algorithmically identified **34 bilateral series deciders** tied 1–1 (in 3-match series) or 2–2 (in 5-match series), alongside Asia Cup Super 4 deciders.
* **Late League Games ($0.70$, 79 matches)**: IPL Match 55+ where playoff qualification is decided on Net Run Rate.
* **Dead Rubbers ($0.35$, 64 matches)**: Matches played after a series has already been clinched (e.g. 2–0 in a 3-match series or 3–0/3–1 in a 5-match series). Player anxiety and stakes drop substantially.
* **Marquee High-Ego Rivalries ($+0.15$ boost, 48 matches)**: Cultural blockbuster derbies carrying intense media scrutiny and fan pressure (`MI vs CSK`, `RCB vs CSK`, `RCB vs MI`, `IND vs PAK`, `AUS vs ENG`, `IND vs AUS`).

#### B. Opposition Quality Tiers ($Q_{\text{opp}}$):
Calibrated against 2022–2026 win-loss records and ICC trophies:
* **Tier 1 ($1.00$)**: **India** (82 T20I wins, 2 ICC T20 World Cups, dominant win rate).
* **Tier 1.5 ($0.88 - 0.92$)**: **IPL Franchises** (concentrated international star power, fierce parity).
* **Tier 2 ($0.85$)**: **Australia, England, South Africa, New Zealand** (elite fast bowling, world-class depth).
* **Tier 3 ($0.68 - 0.75$)**: **Pakistan, West Indies, Sri Lanka, Afghanistan** (world-class match-winners).
* **Tier 4 ($0.50 - 0.58$)**: **Bangladesh, Ireland, Zimbabwe, Netherlands, Scotland, USA**.
* **Tier 5 ($0.35 - 0.40$)**: Other Associates and 'A' Teams.

#### C. Global Hostile Fortresses ($H_{\text{fortress}}$, 680 matches):
Visiting teams playing away against elite hosts bear an environmental penalty:
* Australia in Australia ($+0.15$), India in India ($+0.15$), England in UK ($+0.15$), New Zealand in NZ ($+0.14$), South Africa in SA ($+0.14$), Pakistan in Pakistan ($+0.13$), Bangladesh in Mirpur ($+0.12$), West Indies in Caribbean ($+0.12$), and iconic IPL home grounds ($+0.08$ to $+0.10$).

---

### 1.3 Micro Situational Leverage ($S_{\text{micro}}$)

#### For Batters ($S_{\text{micro, bat}}$):
* **2nd Innings (Chasing)**:
  $$S_{\text{chase, bat}} = 0.40 \times \min\left(1, \frac{\text{RRR}}{16}\right) + 0.25 \times \left(\frac{\text{Wickets}}{9}\right) + 0.20 \times \left(1 - \frac{\text{BallsLeft}}{120}\right) + 0.15 \times \text{RRR\_vs\_CRR}$$
* **1st Innings (Setting)**:
  $$S_{\text{set, bat}} = 0.55 \times \text{PhaseWeight} + 0.45 \times \min\left(1, \frac{\text{Wickets}}{6}\right)$$
  *(Death overs = 0.85, Powerplay = 0.45, Middle = 0.35)*
* **Psychological In-Game Modifiers**: Cold new batter ($<8$ balls, $+0.12$), Set batter ($\ge 18$ balls, $\ge 20$ runs, $-0.10$), Bowler post-wicket ($+0.15$), Post-boundary momentum ($-0.08$), Dot-ball streak ($+0.10$), Pre-match 3-game slump ($+0.08$), Peak form ($-0.06$).

#### For Bowlers ($S_{\text{micro, bowl}}$):
* **2nd Innings (Defending)**:
  $$S_{\text{chase, bowl}} = 0.45 \times \text{PhaseWeight} + 0.35 \times \exp\left(-\frac{|\text{RRR} - 9|^2}{25}\right) + 0.20 \times \left(1 - \frac{\text{Wickets}}{10}\right)$$
* **Micro-Momentum Modifiers**:
  * **Post-Boundary Delivery**: **$+0.20$** if hit for 4 or 6 on the immediately preceding ball (testing bounce-back resilience).
  * **Post-Wicket Surge**: **$-0.15$** (confidence boost after taking a wicket).

### 1.4 The 70th Percentile Pressure Split
Deliveries were ranked by continuous pressure score. The **top 30%** were designated as **High-Pressure Situations**:
* **Batter Threshold ($\tau_{\text{bat}} = 0.5835$)**: 60,314 high-pressure balls (30.0%)
* **Bowler Threshold ($\tau_{\text{bowl}} = 0.6501$)**: 60,300 high-pressure balls (30.0%)
* **Validation**: 77.3% of batter death-over balls and 59.8% of post-boundary deliveries fall into the high-pressure band.

---

## 2. Performance Measurement & Scoring Logic

### 2.1 Batting Metrics Engine (5 Core Pillars)
Prioritizing boundary hitting while respecting strike rotation:
1. **Boundary % (4s + 6s per ball)**: **25%** (The ultimate currency of T20 momentum).
2. **Strike Rate (SR)**: **25%** (Scoring velocity under climbing RRR).
3. **Batting Average (Avg)**: **20%** (Wicket preservation and match-winning presence).
4. **Strike Rotation Rate (SRR: 1s, 2s, 3s %)**: **18%** (Ticking the scoreboard, rotating strike to set batters).
5. **Dot Ball Avoidance Rate (1 - Dot %)**: **12%** (Penalizing scoreboard suffocation).

### 2.2 Bowling Metrics Engine (5 Core Pillars)
1. **Inverted Economy Rate**: **25%** (Run containment in death overs and chases).
2. **Boundary Suppression (1 - Boundary Conceded %)**: **25%** (Preventing boundary leaks).
3. **Wicket Strike Rate (Balls per Wicket)**: **20%** (Breakthrough capability).
4. **Post-Boundary Composure**: **18%** (% of dots/wickets delivered immediately following a 4 or 6).
5. **Dot Ball %**: **12%** (Pressure building and containment).

### 2.3 Anchored Normalization & Smooth PPR
To prevent denominator blow-ups (e.g. players scoring 0 in normal conditions), metrics are scaled using anchored baselines:
$$\text{PPR} = \text{clamp}\left(\frac{S_{\text{hp}}}{\max(20.0, S_{\text{norm}})}, 0.60, 1.60\right)$$

* **$\text{PPR} > 1.0$**: The player **elevates their game** under pressure relative to baseline.
* **$\text{PPR} < 1.0$**: The player **dips** under pressure.

### 2.4 Final Ranking Score
To balance proven world-class pressure output with relative elevation, scaled by sample size reliability:
$$\text{Final Score} = \left(0.75 \times S_{\text{hp}} + 0.25 \times (\text{PPR} \times 50.0)\right) \times \sqrt{\min\left(1.0, \frac{N_{\text{hp}}}{150}\right)}$$

---

## 3. Fair Comparisons & Guardrails

1. **Eligibility Guardrails**:
   * Batters: Minimum **75 balls in normal conditions** and **40 balls in high-pressure conditions** (162 qualified batters).
   * Bowlers: Minimum **75 balls in normal conditions** and **40 balls in high-pressure conditions** (243 qualified bowlers).
2. **Opposition Caliber Weighting**:
   * A batter facing Jasprit Bumrah and India receives an opposition multiplier of $1.00 / 0.80 = 1.25$, whereas scoring against an Associate bowler scales down to $0.40 / 0.80 = 0.50$.
3. **IPL vs. T20I Parity**:
   * Franchise cricket is treated as Tier 1.5 ($0.88 - 0.92$), reflecting international star density and elite bowling attacks.
4. **Data Integrity Audit**:
   * Master parquet verified with **0 NaNs across all 200,999 rows**. Handled delivery 120 division-by-zero edge cases and all 38 Super Over deliveries.

---

## 4. The 4-Quadrant Permutations Model

Using median splits across the qualified pool ($S_{\text{norm}}$ vs. $S_{\text{hp}}$), every player is categorized into one of 4 archetypes:

```
                           High-Pressure Score (Y-axis) ↑
                                                        │
         QUADRANT 2: CRISIS SPECIALISTS                 │            QUADRANT 1: CLUTCH GIANTS
     (Low/Mid Normal Score, High Pressure Score)        │   (High Normal Score, High Pressure Score)
     • Elevate substantially in crisis (PPR > 1.25)     │   • Dominant across ALL conditions (PPR ~ 1.0 - 1.2)
     • Unheralded match-winners                         │   • World-class consistency under any game state
     • Batters: Rishabh Pant, Matthew Wade              │   • Batters: Naman Dhir, Shashank Singh, Tim David,
     • Bowlers: Faheem Ashraf, Riley Meredith,          │              Tilak Varma, Jos Buttler, Shreyas Iyer
                Haris Rauf, Shadab Khan                 │   • Bowlers: Sunil Narine, Jasprit Bumrah,
                                                        │              Shaheen Afridi, Axar Patel
  ──────────────────────────────────────────────────────┼──────────────────────────────────────────────────────→
           QUADRANT 4: STRUGGLERS                       │            QUADRANT 3: FRONT-RUNNERS
     (Low Normal Score, Low Pressure Score)             │   (High Normal Score, Low Pressure Score)
     • Below average across both regimes                │   • Feast on easy conditions / dead rubbers
     • Low match leverage impact                        │   • Performance sharply declines under pressure (PPR < 0.9)
     • Batters: Lower-order accumulators                │   • Batters: Aiden Markram (PPR 0.78), Dewald Brevis (PPR 0.80)
     • Bowlers: Kartik Tyagi, Avesh Khan                │   • Bowlers: Mohammed Shami (PPR 0.60), Naveen ul Haq (PPR 0.78)
```

---

## 5. Official Player Rankings

### 5.1 Top 10 Batters Under Pressure

| Rank | Player Name | HP Balls | HP Runs | HP SR | HP Avg | HP Boundary % | Normal Score | HP Score | PPR | Final Score | Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Naman Dhir** | 265 | 497 | **187.5** | 31.1 | **27.5%** | 60.9 | **91.8** | **1.51** | **87.7** | Clutch Giant |
| **2** | **Shashank Singh** | 364 | 609 | **167.3** | **38.1** | **22.0%** | 82.7 | **93.5** | **1.13** | **84.3** | Clutch Giant |
| **3** | **Tim David** | 763 | **1,345** | **176.3** | 36.4 | **24.6%** | 79.3 | **89.8** | **1.13** | **81.5** | Clutch Giant |
| **4** | **Tilak Varma** | 760 | **1,264** | **166.3** | **39.5** | **22.4%** | 66.6 | **86.5** | **1.30** | **81.1** | Clutch Giant |
| **5** | **Jos Buttler** | 187 | 322 | **172.2** | 35.8 | **26.7%** | 76.9 | **88.7** | **1.15** | **81.0** | Clutch Giant |
| **6** | **Rishabh Pant** | 277 | 471 | **170.0** | 36.2 | **24.5%** | 59.5 | **82.7** | **1.39** | **79.4** | Crisis Specialist |
| **7** | **Matthew Wade** | 223 | 333 | 149.3 | **41.6** | 18.4% | 50.6 | **79.1** | **1.56** | **78.9** | Crisis Specialist |
| **8** | **Shreyas Iyer** | 286 | 499 | **174.5** | 26.3 | **24.1%** | 77.3 | **86.4** | **1.12** | **78.8** | Clutch Giant |
| **9** | **Rajat Patidar** | 219 | 373 | **170.3** | 33.9 | **23.7%** | 87.1 | **87.9** | **1.01** | **78.5** | Clutch Giant |
| **10** | **Tristan Stubbs** | 648 | **1,028** | 158.6 | 35.4 | **20.2%** | 75.2 | **85.1** | **1.13** | **78.0** | Clutch Giant |

---

### 5.2 Top 10 Bowlers Under Pressure

| Rank | Player Name | HP Balls | HP Econ | HP WSR | Post-Bdry Composure | Normal Score | HP Score | PPR | Final Score | Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Sunil Narine** | 448 | **6.76** | 16.6 | **40.0%** | 68.9 | **82.5** | **1.20** | **76.8** | Clutch Giant |
| **2** | **Jasprit Bumrah** | **736** | **6.88** | 21.0 | **46.8%** | 68.0 | **77.6** | **1.14** | **72.5** | Clutch Giant |
| **3** | **Shaheen Afridi** | 349 | **7.39** | **10.9** | **43.0%** | 55.5 | **70.9** | **1.28** | **69.2** | Clutch Giant |
| **4** | **Faheem Ashraf** | 122 | **7.57** | **12.2** | **48.6%** | 39.7 | **74.9** | **1.60** | **68.7** | Crisis Specialist |
| **5** | **Riley Meredith** | 139 | 8.50 | **10.7** | **45.7%** | 29.9 | **68.5** | **1.60** | **68.7** | Crisis Specialist |
| **6** | **Haris Rauf** | 363 | 7.92 | **11.7** | **38.1%** | 48.2 | **66.9** | **1.39** | **67.5** | Crisis Specialist |
| **7** | **Alzarri Joseph** | 458 | 8.66 | 15.3 | **42.5%** | 38.4 | **61.5** | **1.60** | **66.1** | Crisis Specialist |
| **8** | **Shadab Khan** | 125 | **6.72** | 20.8 | **30.0%** | 43.8 | **68.6** | **1.57** | **64.8** | Crisis Specialist |
| **9** | **Xavier Bartlett** | 241 | 8.61 | 18.5 | **41.3%** | 37.0 | **59.2** | **1.60** | **64.4** | Crisis Specialist |
| **10** | **Axar Patel** | 603 | **7.58** | 18.3 | **36.8%** | 53.2 | **65.2** | **1.23** | **64.2** | Clutch Giant |

---

### 5.3 Positional Best Batters (Slots 1 to 7)

* **Slot #1 (Opener)**: **Virat Kohli** (HP SR 197.4, HP Avg 38.5)
* **Slot #2 (Opener)**: **Quinton de Kock** (HP SR 152.4, HP Avg 48.0)
* **Slot #3 (One-Down / Anchor)**: **Shreyas Iyer** (HP SR 198.3, HP Avg 58.5)
* **Slot #4 (Middle Power)**: **Rovman Powell** (HP SR 170.0, HP Avg 39.7)
* **Slot #5 (Crisis Stabilizer)**: **Tilak Varma** (679 HP runs, HP SR 168.5, HP Avg 45.3)
* **Slot #6 (Finisher)**: **Shashank Singh** (315 HP runs, HP SR 164.9, HP Avg 45.0)
* **Slot #7 (Lower Clutch)**: **Naman Dhir** (262 HP runs, HP SR 197.0, HP Avg 43.7)

---

### 5.4 Bowling Phase Specialists

* **Powerplay (Overs 1–6)**: **Shaheen Afridi** (Econ 6.19, WSR 14.2, Post-Boundary: 55.1%) & **Jasprit Bumrah** (Econ 6.14, Post-Boundary: 64.1%)
* **Middle Overs (Overs 7–15)**: **Harpreet Brar** (Econ 6.35, WSR 13.9) & **Kagiso Rabada** (Econ 6.00, WSR 12.0)
* **Death Overs (Overs 16–20)**: **Sunil Narine** (Econ 6.18, WSR 11.2) & **Jasprit Bumrah** (410 HP balls, Econ 7.29, WSR 14.6)

---

## 6. Reliability & Limitations

### 6.1 Consistency Verification
* **Sensitivity to Weight Variations**: When varying metric weights by $\pm 10\%$, 9 of the Top 10 Batters and 9 of the Top 10 Bowlers remained identical, demonstrating high algorithmic stability.
* **Sample Size Protection**: Square-root volume weighting prevented small-sample part-timers from infiltrating the top tier, ensuring that bowlers who delivered over 400–700 balls in death overs were properly recognized.

### 6.2 Known Model Boundaries & Limitations
1. **DLS Re-calculations**: Matches shortened by rain were evaluated using revised targets from `matches.csv`; dynamic par calculations per ball were not present in the raw data.
2. **Fielding Placements**: The dataset provides shot type and delivery style but lacks 3D player coordinates. Catching difficulty is proxied through bowler wicket types.
3. **Survivor Bias**: We note that batters who routinely fail under pressure are frequently dropped or pushed down the order, resulting in fewer pressure balls. Our minimum ball filters ($N_{\text{hp}} \ge 40$) partially mitigate this, but cannot fully reconstruct unobserved failures.

---

## Conclusion
This methodology demonstrates that reliability under pressure can be measured with scientific precision. By blending macro context, opposition caliber, hostile fortresses, live in-game leverage, and bowler micro-composure, the system identifies the true match-winners who rise when the game is on the line.
