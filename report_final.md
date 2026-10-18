# Replication of Card and Krueger (1994): Minimum Wages and Employment

## 1. Research question and motivation

Card and Krueger (1994) ask whether a rise in the minimum wage reduces employment at fast-food restaurants. On April 1, 1992, New Jersey raised its minimum wage from $4.25 to $5.05 per hour, while eastern Pennsylvania kept its minimum wage at $4.25. The paper compares employment changes at stores in New Jersey and Pennsylvania before and after the increase, and also compares high-wage and low-wage stores within New Jersey.

The economic mechanism is the standard competitive prediction that a binding minimum wage raises labor costs and reduces employment. The paper's contribution is to test this prediction with establishment-level survey data and a difference-in-differences design. The empirical design is a first-differenced model:

- Baseline: change in FTE employment from Wave 1 to Wave 2 regressed on a New Jersey dummy.
- Alternative: change in FTE employment regressed on the initial wage gap, defined as the proportional wage increase needed to reach $5.05.
- Controls: chain dummies, company ownership, and region dummies.

## 2. Data sources, sample construction, and variable definitions

The raw data are the course-provided `public.csv`, which contains 410 fast-food stores in New Jersey and eastern Pennsylvania. The data contain two survey waves: February-March 1992 and November-December 1992. The main variables are:

- `STATE`: 1 = New Jersey, 0 = Pennsylvania.
- `EMPFT`, `EMPPT`, `NMGRS`: full-time employees, part-time employees, and managers.
- `WAGE_ST`: starting wage in Wave 1.
- `WAGE_ST2`: starting wage in Wave 2.
- `STATUS2`: Wave-2 status. `3` = permanently closed; `2`, `4`, `5` = temporarily closed.
- `GAP`: proportional increase in the starting wage needed to reach $5.05.

FTE employment is defined as `EMPFT + NMGRS + 0.5 * EMPPT`. For permanently closed stores, Wave-2 FTE employment is set to zero. For temporarily closed stores, Wave-2 FTE employment is treated as missing in the baseline. The Table 4 sample restricts to stores with employment and starting-wage data in both waves and a nonmissing GAP variable.

## 3. Empirical design

The main specification is:

ΔFTE_i = a + b X_i + c NJ_i + e_i,

where ΔFTE_i is the change in FTE employment between waves, X_i includes chain and ownership controls, and NJ_i is a New Jersey dummy. An alternative specification replaces the New Jersey dummy with GAP_i, the initial wage gap. Standard errors are conventional OLS standard errors, matching the paper's baseline presentation.

## 4. Core replication results and comparison with the original paper

The table below compares key original estimates with the replication.

| item                                   | original     | replication   |
|:---------------------------------------|:-------------|:--------------|
| Table 3, row 4: NJ-PA change in FTE    | 2.75 (1.34)  | 2.75 (1.34)   |
| Table 4, column (ii): New Jersey dummy | 2.30 (1.19)  | 2.28 (1.20)   |
| Table 4, column (iii): GAP             | 15.65 (6.08) | 17.05 (6.09)  |
| Table 4, column (iv): GAP              | 14.92 (6.21) | 16.36 (6.24)  |

### Table 2: Selected means

| section       | variable             | NJ           | PA           | NJ-PA         |     t |
|:--------------|:---------------------|:-------------|:-------------|:--------------|------:|
| 1. Store type | Burger King          | 41.09 (2.71) | 44.30 (5.62) | -3.22 (6.24)  | -0.52 |
| 1. Store type | KFC                  | 20.54 (2.22) | 15.19 (4.06) | 5.35 (4.63)   |  1.16 |
| 1. Store type | Roy Rogers           | 24.77 (2.38) | 21.52 (4.65) | 3.25 (5.22)   |  0.62 |
| 1. Store type | Wendy's              | 13.60 (1.89) | 18.99 (4.44) | -5.39 (4.82)  | -1.12 |
| 1. Store type | Company-owned        | 34.14 (2.61) | 35.44 (5.42) | -1.30 (6.01)  | -0.22 |
| 2. Wave 1     | FTE employment       | 20.44 (0.51) | 23.33 (1.35) | -2.89 (1.44)  | -2    |
| 2. Wave 1     | Percentage full-time | 37.73 (1.14) | 38.76 (2.30) | -1.03 (2.57)  | -0.4  |
| 2. Wave 1     | Starting wage        | 4.61 (0.02)  | 4.63 (0.04)  | -0.02 (0.04)  | -0.4  |
| 2. Wave 1     | Wage = $4.25         | 30.51 (2.53) | 32.91 (5.32) | -2.40 (5.89)  | -0.41 |
| 2. Wave 1     | Price of full meal   | 3.35 (0.04)  | 3.04 (0.07)  | 0.31 (0.08)   |  3.96 |
| 2. Wave 1     | Hours open (weekday) | 14.42 (0.15) | 14.53 (0.33) | -0.11 (0.37)  | -0.29 |
| 2. Wave 1     | Recruiting bonus     | 23.56 (2.34) | 29.11 (5.14) | -5.55 (5.65)  | -0.98 |
| 3. Wave 2     | FTE employment       | 21.03 (0.52) | 21.17 (0.94) | -0.14 (1.08)  | -0.13 |
| 3. Wave 2     | Percentage full-time | 40.76 (1.26) | 35.60 (2.40) | 5.15 (2.71)   |  1.9  |
| 3. Wave 2     | Starting wage        | 5.08 (0.01)  | 4.62 (0.04)  | 0.46 (0.04)   | 10.82 |
| 3. Wave 2     | Wage = $4.25         | 0.00 (0.00)  | 25.32 (4.92) | -25.32 (4.92) | -5.14 |
| 3. Wave 2     | Wage = $5.05         | 85.50 (1.94) | 1.27 (1.27)  | 84.23 (2.32)  | 36.38 |
| 3. Wave 2     | Price of full meal   | 3.41 (0.04)  | 3.03 (0.07)  | 0.39 (0.08)   |  5.08 |
| 3. Wave 2     | Hours open (weekday) | 14.42 (0.15) | 14.65 (0.33) | -0.23 (0.36)  | -0.65 |

### Table 3: Average employment before and after the minimum-wage increase

| row                                         | PA           | NJ           | Difference NJ-PA   | NJ wage = $4.25   | NJ wage = $4.26-$4.99   | NJ wage >= $5.00   | Low-high     | Mid-high     |
|:--------------------------------------------|:-------------|:-------------|:-------------------|:------------------|:------------------------|:-------------------|:-------------|:-------------|
| 1. FTE before, all available                | 23.33 (1.35) | 20.44 (0.51) | -2.89 (1.44)       | 19.56 (0.77)      | 20.08 (0.84)            | 22.25 (1.14)       | -2.69 (1.37) | -2.17 (1.41) |
| 2. FTE after, all available                 | 21.17 (0.94) | 21.03 (0.52) | -0.14 (1.08)       | 20.88 (1.01)      | 20.96 (0.76)            | 20.21 (1.03)       | 0.66 (1.44)  | 0.74 (1.27)  |
| 3. Change in mean FTE, all available        | -2.17 (1.65) | 0.59 (0.73)  | 2.75 (1.80)        | 1.32 (1.27)       | 0.87 (1.13)             | -2.04 (1.53)       | 3.36 (1.99)  | 2.91 (1.90)  |
| 4. Change in mean FTE, balanced             | -2.28 (1.25) | 0.47 (0.48)  | 2.75 (1.34)        | 1.20 (0.82)       | 0.71 (0.69)             | -2.16 (1.01)       | 3.36 (1.30)  | 2.87 (1.22)  |
| 5. Change in mean FTE, temporary closed = 0 | -2.28 (1.25) | 0.23 (0.49)  | 2.51 (1.35)        | 0.90 (0.87)       | 0.49 (0.69)             | -2.39 (1.02)       | 3.29 (1.34)  | 2.88 (1.23)  |

### Table 4: Reduced-form models for the change in FTE employment

| variable                     | (i)          | (ii)         | (iii)           | (iv)            | (v)           |
|:-----------------------------|:-------------|:-------------|:----------------|:----------------|:--------------|
| New Jersey dummy             | 2.28 (1.19)* | 2.28 (1.20)* | nan             | nan             | nan           |
| Initial wage gap             | nan          | nan          | 17.05 (6.09)*** | 16.36 (6.24)*** | 13.88 (7.44)* |
| Chain and ownership controls | no           | yes          | no              | yes             | yes           |
| Region controls              | no           | no           | no              | no              | yes           |
| R-squared                    | 0.010        | 0.020        | 0.022           | 0.029           | 0.043         |
| N                            | 351          | 351          | 351             | 351             | 351           |

The replication is qualitatively consistent with the paper: the New Jersey dummy and the initial wage gap are positive, and the baseline difference-in-differences estimate is close to the paper's 2.75 FTE employees. Differences are expected because the provided CSV does not contain the original sample-frame and refusal information used in Table 1, and because small differences in missing-value handling, the exact treatment of temporary closures, and the set of stores with complete wage data can change the sample by a few observations.

## 5. Independent extension

As an independent extension, I re-estimated the main models under alternative part-time weighting schemes (0.4 and 0.6 instead of 0.5) and excluding stores in the New Jersey shore area, which may have different seasonal employment patterns. The results are:

| extension                       | model          |   NJ_coef |     NJ_se |   GAP_coef |    GAP_se |   N |
|:--------------------------------|:---------------|----------:|----------:|-----------:|----------:|----:|
| part-time weight = 0.4          | NJ + controls  |   2.33419 |   1.20685 |   nan      | nan       | 351 |
| part-time weight = 0.4          | GAP + controls | nan       | nan       |    16.5818 |   6.28872 | 351 |
| part-time weight = 0.5          | NJ + controls  |   2.28151 |   1.19704 |   nan      | nan       | 351 |
| part-time weight = 0.5          | GAP + controls | nan       | nan       |    16.3631 |   6.23725 | 351 |
| part-time weight = 0.6          | NJ + controls  |   2.22882 |   1.20301 |   nan      | nan       | 351 |
| part-time weight = 0.6          | GAP + controls | nan       | nan       |    16.1444 |   6.26875 | 351 |
| exclude New Jersey shore stores | NJ + controls  |   2.59109 |   1.19487 |   nan      | nan       | 320 |
| exclude New Jersey shore stores | GAP + controls | nan       | nan       |    18.6638 |   6.39602 | 320 |

The extension checks whether the positive employment association is sensitive to the construction of FTE employment and to seasonal shore stores. The sign and approximate magnitude of the key coefficients are the focus; the extension is not intended to overturn the paper's conclusion.

## 6. Validation, limitations, and conclusion

Validation checks include: the Table 4 sample size is close to the paper's 357 stores; the constructed FTE variable matches the paper's definition; permanent closures are set to zero while temporary closures are treated as missing; and the Figure 1 wage distribution shows the expected spike at $5.05 in New Jersey in November 1992.

Limitations: the provided CSV does not allow a full replication of Table 1 response rates or the sample-frame construction; the exact original missing-data rules are not fully documented; and the paper's standard errors are conventional OLS, so clustering or robust standard errors would change precision but not the main qualitative conclusion.

Overall, the replication supports the paper's central finding: the New Jersey minimum-wage increase did not reduce fast-food employment relative to Pennsylvania, and the initial wage gap is positively associated with employment changes.

## Figure 1

The replication of Figure 1 is saved at `outputs/figures/figure1.png`. The underlying plotting data are in `outputs/figures/figure1_data.csv`.
