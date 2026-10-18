from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from utils import mean_se, stars


def table2(df):
    rows = []

    def add(section, variable, series, wave, percent=False):
        nj = series[df["STATE"] == 1]
        pa = series[df["STATE"] == 0]
        m_nj, se_nj, n_nj = mean_se(nj)
        m_pa, se_pa, n_pa = mean_se(pa)
        diff = m_nj - m_pa
        se_diff = np.sqrt(se_nj**2 + se_pa**2) if n_nj > 0 and n_pa > 0 else np.nan
        t = diff / se_diff if se_diff and se_diff > 0 else np.nan

        if percent:
            m_nj *= 100
            se_nj *= 100
            m_pa *= 100
            se_pa *= 100
            diff *= 100
            se_diff *= 100

        rows.append(
            {
                "section": section,
                "variable": variable,
                "wave": wave,
                "nj_mean": m_nj,
                "nj_se": se_nj,
                "n_nj": n_nj,
                "pa_mean": m_pa,
                "pa_se": se_pa,
                "n_pa": n_pa,
                "diff": diff,
                "se_diff": se_diff,
                "t": t,
            }
        )

    for label, cond in [
        ("Burger King", df["CHAIN"] == 1),
        ("KFC", df["CHAIN"] == 2),
        ("Roy Rogers", df["CHAIN"] == 3),
        ("Wendy's", df["CHAIN"] == 4),
        ("Company-owned", df["CO_OWNED"] == 1),
    ]:
        add("1. Store type", label, cond.astype(float), "Wave 1", percent=True)

    add("2. Wave 1", "FTE employment", df["FTE1"], "Wave 1")
    add("2. Wave 1", "Percentage full-time", df["pct_full1"], "Wave 1")
    add("2. Wave 1", "Starting wage", df["WAGE_ST"], "Wave 1")
    add("2. Wave 1", "Wage = $4.25", df["wage_eq_425_1"].astype(float), "Wave 1", percent=True)
    add("2. Wave 1", "Price of full meal", df["price_full1"], "Wave 1")
    add("2. Wave 1", "Hours open (weekday)", df["HRSOPEN"], "Wave 1")
    add("2. Wave 1", "Recruiting bonus", df["BONUS"], "Wave 1", percent=True)

    add("3. Wave 2", "FTE employment", df["FTE2_adj"], "Wave 2")
    add("3. Wave 2", "Percentage full-time", df["pct_full2"], "Wave 2")
    add("3. Wave 2", "Starting wage", df["WAGE_ST2"], "Wave 2")
    add("3. Wave 2", "Wage = $4.25", df["wage_eq_425_2"].astype(float), "Wave 2", percent=True)
    add("3. Wave 2", "Wage = $5.05", df["wage_eq_505_2"].astype(float), "Wave 2", percent=True)
    add("3. Wave 2", "Price of full meal", df["price_full2"], "Wave 2")
    add("3. Wave 2", "Hours open (weekday)", df["HRSOPEN2"], "Wave 2")

    return pd.DataFrame(rows)


def format_table2(t2):
    out = []
    for _, r in t2.iterrows():
        out.append(
            {
                "section": r["section"],
                "variable": r["variable"],
                "NJ": f"{r['nj_mean']:.2f} ({r['nj_se']:.2f})",
                "PA": f"{r['pa_mean']:.2f} ({r['pa_se']:.2f})",
                "NJ-PA": f"{r['diff']:.2f} ({r['se_diff']:.2f})",
                "t": f"{r['t']:.2f}" if pd.notna(r["t"]) else "",
            }
        )
    return pd.DataFrame(out)


def table3(df):
    groups = {
        "PA": df["STATE"] == 0,
        "NJ": df["STATE"] == 1,
        "NJ_low": (df["STATE"] == 1) & df["wage_low"],
        "NJ_mid": (df["STATE"] == 1) & df["wage_mid"],
        "NJ_high": (df["STATE"] == 1) & df["wage_high"],
    }

    row_defs = [
        ("1. FTE before, all available", lambda d: d["FTE1"]),
        ("2. FTE after, all available", lambda d: d["FTE2_adj"]),
        ("3. Change in mean FTE, all available", None),
        ("4. Change in mean FTE, balanced", lambda d: d["delta_bal"]),
        ("5. Change in mean FTE, temporary closed = 0", lambda d: d["delta_bal_zero_temp"]),
    ]

    results = {}
    for rlabel, func in row_defs:
        vals = {}
        for gname, mask in groups.items():
            d = df[mask]
            if rlabel.startswith("3."):
                m1, se1, n1 = mean_se(d["FTE1"])
                m2, se2, n2 = mean_se(d["FTE2_adj"])
                mean = m2 - m1
                se = np.sqrt(se1**2 + se2**2) if n1 > 0 and n2 > 0 else np.nan
                n = min(n1, n2)
            else:
                mean, se, n = mean_se(func(d))
            vals[gname] = (mean, se, n)
        results[rlabel] = vals

    rows = []
    for rlabel, vals in results.items():
        def fmt(g):
            m, se, n = vals[g]
            return f"{m:.2f} ({se:.2f})" if pd.notna(se) else f"{m:.2f} (NA)"

        def diff(g1, g2):
            m1, se1, n1 = vals[g1]
            m2, se2, n2 = vals[g2]
            d = m1 - m2
            se = np.sqrt(se1**2 + se2**2) if n1 > 0 and n2 > 0 else np.nan
            return f"{d:.2f} ({se:.2f})" if pd.notna(se) else f"{d:.2f} (NA)"

        rows.append(
            {
                "row": rlabel,
                "PA": fmt("PA"),
                "NJ": fmt("NJ"),
                "Difference NJ-PA": diff("NJ", "PA"),
                "NJ wage = $4.25": fmt("NJ_low"),
                "NJ wage = $4.26-$4.99": fmt("NJ_mid"),
                "NJ wage >= $5.00": fmt("NJ_high"),
                "Low-high": diff("NJ_low", "NJ_high"),
                "Mid-high": diff("NJ_mid", "NJ_high"),
            }
        )

    return pd.DataFrame(rows), results


def table4(df):
    sample = df[
        df["FTE1"].notna()
        & df["FTE2_adj"].notna()
        & df["WAGE_ST"].notna()
        & df["WAGE_ST2"].notna()
        & df["GAP"].notna()
    ].copy()
    sample["delta"] = sample["FTE2_adj"] - sample["FTE1"]
    sample["NJ"] = (sample["STATE"] == 1).astype(float)
    sample["chain"] = sample["CHAIN"].astype("category")
    sample["region"] = sample["region"].astype("category")

    models = {
        "(i)": "delta ~ NJ",
        "(ii)": "delta ~ NJ + C(chain) + CO_OWNED",
        "(iii)": "delta ~ GAP",
        "(iv)": "delta ~ GAP + C(chain) + CO_OWNED",
        "(v)": "delta ~ GAP + C(chain) + CO_OWNED + C(region)",
    }

    rows = []
    for mname, formula in models.items():
        res = smf.ols(formula, data=sample).fit()
        for var in ["NJ", "GAP"]:
            if var in res.params.index:
                rows.append(
                    {
                        "model": mname,
                        "variable": var,
                        "coef": res.params[var],
                        "se": res.bse[var],
                        "t": res.tvalues[var],
                        "p": res.pvalues[var],
                        "r2": res.rsquared,
                        "n": int(res.nobs),
                    }
                )
    return pd.DataFrame(rows), sample


def format_table4(t4):
    models = ["(i)", "(ii)", "(iii)", "(iv)", "(v)"]
    rows = []

    def get(m, var):
        sub = t4[(t4["model"] == m) & (t4["variable"] == var)]
        if len(sub) == 0:
            return ""
        r = sub.iloc[0]
        return f"{r['coef']:.2f} ({r['se']:.2f}){stars(r['p'])}"

    rows.append({"variable": "New Jersey dummy", **{m: get(m, "NJ") for m in models}})
    rows.append({"variable": "Initial wage gap", **{m: get(m, "GAP") for m in models}})
    rows.append(
        {
            "variable": "Chain and ownership controls",
            "(i)": "no",
            "(ii)": "yes",
            "(iii)": "no",
            "(iv)": "yes",
            "(v)": "yes",
        }
    )
    rows.append(
        {
            "variable": "Region controls",
            "(i)": "no",
            "(ii)": "no",
            "(iii)": "no",
            "(iv)": "no",
            "(v)": "yes",
        }
    )
    rows.append(
        {
            "variable": "R-squared",
            **{m: f"{t4[t4['model'] == m]['r2'].iloc[0]:.3f}" for m in models if len(t4[t4["model"] == m]) > 0},
        }
    )
    rows.append(
        {
            "variable": "N",
            **{m: f"{int(t4[t4['model'] == m]['n'].iloc[0])}" for m in models if len(t4[t4["model"] == m]) > 0},
        }
    )
    return pd.DataFrame(rows)


def extension(df):
    rows = []

    for weight in [0.4, 0.5, 0.6]:
        d = df.copy()
        d["FTE1_w"] = d["EMPFT"] + d["NMGRS"] + weight * d["EMPPT"]
        d["FTE2_w_raw"] = d["EMPFT2"] + d["NMGRS2"] + weight * d["EMPPT2"]
        d["FTE2_w"] = d["FTE2_w_raw"]
        d.loc[d["STATUS2"] == 3, "FTE2_w"] = 0.0
        d.loc[d["STATUS2"].isin([2, 4, 5]), "FTE2_w"] = np.nan
        d["delta"] = d["FTE2_w"] - d["FTE1_w"]

        sample = d[
            d["FTE1_w"].notna()
            & d["FTE2_w"].notna()
            & d["WAGE_ST"].notna()
            & d["WAGE_ST2"].notna()
            & d["GAP"].notna()
        ].copy()
        sample["NJ"] = (sample["STATE"] == 1).astype(float)
        sample["chain"] = sample["CHAIN"].astype("category")

        res = smf.ols("delta ~ NJ + C(chain) + CO_OWNED", data=sample).fit()
        rows.append(
            {
                "extension": f"part-time weight = {weight}",
                "model": "NJ + controls",
                "NJ_coef": res.params.get("NJ", np.nan),
                "NJ_se": res.bse.get("NJ", np.nan),
                "GAP_coef": np.nan,
                "GAP_se": np.nan,
                "N": int(res.nobs),
            }
        )

        res = smf.ols("delta ~ GAP + C(chain) + CO_OWNED", data=sample).fit()
        rows.append(
            {
                "extension": f"part-time weight = {weight}",
                "model": "GAP + controls",
                "NJ_coef": np.nan,
                "NJ_se": np.nan,
                "GAP_coef": res.params.get("GAP", np.nan),
                "GAP_se": res.bse.get("GAP", np.nan),
                "N": int(res.nobs),
            }
        )

    d = df[df["SHORE"] != 1].copy()
    sample = d[
        d["FTE1"].notna()
        & d["FTE2_adj"].notna()
        & d["WAGE_ST"].notna()
        & d["WAGE_ST2"].notna()
        & d["GAP"].notna()
    ].copy()
    sample["delta"] = sample["FTE2_adj"] - sample["FTE1"]
    sample["NJ"] = (sample["STATE"] == 1).astype(float)
    sample["chain"] = sample["CHAIN"].astype("category")

    res = smf.ols("delta ~ NJ + C(chain) + CO_OWNED", data=sample).fit()
    rows.append(
        {
            "extension": "exclude New Jersey shore stores",
            "model": "NJ + controls",
            "NJ_coef": res.params.get("NJ", np.nan),
            "NJ_se": res.bse.get("NJ", np.nan),
            "GAP_coef": np.nan,
            "GAP_se": np.nan,
            "N": int(res.nobs),
        }
    )

    res = smf.ols("delta ~ GAP + C(chain) + CO_OWNED", data=sample).fit()
    rows.append(
        {
            "extension": "exclude New Jersey shore stores",
            "model": "GAP + controls",
            "NJ_coef": np.nan,
            "NJ_se": np.nan,
            "GAP_coef": res.params.get("GAP", np.nan),
            "GAP_se": res.bse.get("GAP", np.nan),
            "N": int(res.nobs),
        }
    )

    return pd.DataFrame(rows)


def comparison(t3_results, t4):
    vals = t3_results["4. Change in mean FTE, balanced"]
    m_nj, se_nj, n_nj = vals["NJ"]
    m_pa, se_pa, n_pa = vals["PA"]
    rep_diff = m_nj - m_pa
    rep_se = np.sqrt(se_nj**2 + se_pa**2)

    def get_t4(model, var):
        sub = t4[(t4["model"] == model) & (t4["variable"] == var)]
        if len(sub) == 0:
            return np.nan, np.nan
        r = sub.iloc[0]
        return r["coef"], r["se"]

    nj_ii = get_t4("(ii)", "NJ")
    gap_iii = get_t4("(iii)", "GAP")
    gap_iv = get_t4("(iv)", "GAP")

    rows = [
        {
            "item": "Table 3, row 4: NJ-PA change in FTE",
            "original": "2.75 (1.34)",
            "replication": f"{rep_diff:.2f} ({rep_se:.2f})",
        },
        {
            "item": "Table 4, column (ii): New Jersey dummy",
            "original": "2.30 (1.19)",
            "replication": f"{nj_ii[0]:.2f} ({nj_ii[1]:.2f})",
        },
        {
            "item": "Table 4, column (iii): GAP",
            "original": "15.65 (6.08)",
            "replication": f"{gap_iii[0]:.2f} ({gap_iii[1]:.2f})",
        },
        {
            "item": "Table 4, column (iv): GAP",
            "original": "14.92 (6.21)",
            "replication": f"{gap_iv[0]:.2f} ({gap_iv[1]:.2f})",
        },
    ]
    return pd.DataFrame(rows)


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "processed" / "analysis.csv")
    outdir = root / "outputs" / "tables"
    outdir.mkdir(parents=True, exist_ok=True)

    t2 = table2(df)
    t2.to_csv(outdir / "table2.csv", index=False)
    format_table2(t2).to_csv(outdir / "table2_formatted.csv", index=False)

    t3_fmt, t3_results = table3(df)
    t3_fmt.to_csv(outdir / "table3.csv", index=False)

    t4_num, t4_sample = table4(df)
    t4_num.to_csv(outdir / "table4_numeric.csv", index=False)
    format_table4(t4_num).to_csv(outdir / "table4.csv", index=False)

    ext = extension(df)
    ext.to_csv(outdir / "extension.csv", index=False)

    comp = comparison(t3_results, t4_num)
    comp.to_csv(outdir / "comparison.csv", index=False)

    print(f"Saved tables to {outdir}")
    print(comp.to_string(index=False))


if __name__ == "__main__":
    main()