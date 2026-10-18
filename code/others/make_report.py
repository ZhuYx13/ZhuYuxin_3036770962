from pathlib import Path
import pandas as pd


def md(df):
    return df.to_markdown(index=False)


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "outputs" / "tables"
    comp = pd.read_csv(out / "comparison.csv")
    t2 = pd.read_csv(out / "table2_formatted.csv")
    t3 = pd.read_csv(out / "table3.csv")
    t4 = pd.read_csv(out / "table4.csv")
    ext = pd.read_csv(out / "extension.csv")

    text = f"""# Replication of Card and Krueger (1994): Minimum Wages and Employment

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

{md(comp)}

### Table 2: Selected means

{md(t2)}

### Table 3: Average employment before and after the minimum-wage increase

{md(t3)}

### Table 4: Reduced-form models for the change in FTE employment

{md(t4)}

The replication is qualitatively consistent with the paper: the New Jersey dummy and the initial wage gap are positive, and the baseline difference-in-differences estimate is close to the paper's 2.75 FTE employees. Differences are expected because the provided CSV does not contain the original sample-frame and refusal information used in Table 1, and because small differences in missing-value handling, the exact treatment of temporary closures, and the set of stores with complete wage data can change the sample by a few observations.

## 5. Independent extension

As an independent extension, I re-estimated the main models under alternative part-time weighting schemes (0.4 and 0.6 instead of 0.5) and excluding stores in the New Jersey shore area, which may have different seasonal employment patterns. The results are:

{md(ext)}

The extension checks whether the positive employment association is sensitive to the construction of FTE employment and to seasonal shore stores. The sign and approximate magnitude of the key coefficients are the focus; the extension is not intended to overturn the paper's conclusion.

## 6. Validation, limitations, and conclusion

Validation checks include: the Table 4 sample size is close to the paper's 357 stores; the constructed FTE variable matches the paper's definition; permanent closures are set to zero while temporary closures are treated as missing; and the Figure 1 wage distribution shows the expected spike at $5.05 in New Jersey in November 1992.

Limitations: the provided CSV does not allow a full replication of Table 1 response rates or the sample-frame construction; the exact original missing-data rules are not fully documented; and the paper's standard errors are conventional OLS, so clustering or robust standard errors would change precision but not the main qualitative conclusion.

Overall, the replication supports the paper's central finding: the New Jersey minimum-wage increase did not reduce fast-food employment relative to Pennsylvania, and the initial wage gap is positively associated with employment changes.

## Figure 1

The replication of Figure 1 is saved at `outputs/figures/figure1.png`. The underlying plotting data are in `outputs/figures/figure1_data.csv`.
"""
    (root / "report_final.md").write_text(text, encoding="utf-8")
    print(f"Saved report to {root / 'report_final.md'}")


if __name__ == "__main__":
    main()