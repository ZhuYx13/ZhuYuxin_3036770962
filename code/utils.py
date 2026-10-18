from pathlib import Path
import numpy as np
import pandas as pd

NUMERIC_COLS = [
    "SHEET", "CHAIN", "CO_OWNED", "STATE", "SOUTHJ", "CENTRALJ", "NORTHJ",
    "PA1", "PA2", "SHORE", "NCALLS", "EMPFT", "EMPPT", "NMGRS", "WAGE_ST",
    "INCTIME", "FIRSTINC", "BONUS", "PCTAFF", "MEALS", "OPEN", "HRSOPEN",
    "PSODA", "PFRY", "PENTREE", "NREGS", "NREGS11", "TYPE2", "STATUS2",
    "DATE2", "NCALLS2", "EMPFT2", "EMPPT2", "NMGRS2", "WAGE_ST2",
    "INCTIME2", "FIRSTIN2", "SPECIAL2", "MEALS2", "OPEN2R", "HRSOPEN2",
    "PSODA2", "PFRY2", "PENTREE2", "NREGS2", "NREGS112",
]


def load_public_csv(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def construct_variables(df):
    df = df.copy()
    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Full-time-equivalent employment: full-time + managers + 0.5 * part-time
    df["FTE1"] = df["EMPFT"] + df["NMGRS"] + 0.5 * df["EMPPT"]
    df["FTE2_raw"] = df["EMPFT2"] + df["NMGRS2"] + 0.5 * df["EMPPT2"]

    # Permanent closures: Wave-2 employment = 0.
    # Temporary closures: missing in the baseline.
    df["STATUS2"] = pd.to_numeric(df["STATUS2"], errors="coerce")
    df["FTE2_adj"] = df["FTE2_raw"]
    df.loc[df["STATUS2"] == 3, "FTE2_adj"] = 0.0
    df.loc[df["STATUS2"].isin([2, 4, 5]), "FTE2_adj"] = np.nan

    # Robustness: set temporary closures to zero as well.
    df["FTE2_zero_temp"] = df["FTE2_raw"]
    df.loc[df["STATUS2"].isin([2, 3, 4, 5]), "FTE2_zero_temp"] = 0.0

    df["balanced"] = df["FTE1"].notna() & df["FTE2_adj"].notna()
    df["balanced_zero_temp"] = df["FTE1"].notna() & df["FTE2_zero_temp"].notna()
    df["delta_bal"] = df["FTE2_adj"] - df["FTE1"]
    df["delta_bal_zero_temp"] = df["FTE2_zero_temp"] - df["FTE1"]

    # New Jersey initial wage groups
    w = df["WAGE_ST"]
    df["wage_low"] = np.isclose(w, 4.25, atol=1e-6)
    df["wage_mid"] = (w > 4.25 + 1e-9) & (w < 5.00 - 1e-9)
    df["wage_high"] = w >= 5.00 - 1e-9

    # Initial wage gap: proportional increase needed to reach $5.05.
    df["GAP"] = np.nan
    pa = df["STATE"] == 0
    nj = df["STATE"] == 1
    df.loc[pa, "GAP"] = 0.0
    df.loc[nj & (w >= 5.05 - 1e-9), "GAP"] = 0.0
    mask = nj & w.notna() & (w < 5.05 - 1e-9)
    df.loc[mask, "GAP"] = (5.05 - w[mask]) / w[mask]

    # Prices and log price change
    df["price_full1"] = df["PSODA"] + df["PFRY"] + df["PENTREE"]
    df["price_full2"] = df["PSODA2"] + df["PFRY2"] + df["PENTREE2"]
    df["log_price_change"] = np.where(
        (df["price_full1"] > 0) & (df["price_full2"] > 0),
        np.log(df["price_full2"]) - np.log(df["price_full1"]),
        np.nan,
    )

    # Percentage full-time workers
    den1 = df["EMPFT"] + df["NMGRS"] + df["EMPPT"]
    den2 = df["EMPFT2"] + df["NMGRS2"] + df["EMPPT2"]
    df["pct_full1"] = np.where(den1 > 0, (df["EMPFT"] + df["NMGRS"]) / den1 * 100, np.nan)
    df["pct_full2"] = np.where(den2 > 0, (df["EMPFT2"] + df["NMGRS2"]) / den2 * 100, np.nan)

    df["wage_eq_425_1"] = np.isclose(df["WAGE_ST"], 4.25, atol=1e-6)
    df["wage_eq_425_2"] = np.isclose(df["WAGE_ST2"], 4.25, atol=1e-6)
    df["wage_eq_505_2"] = np.isclose(df["WAGE_ST2"], 5.05, atol=1e-6)

    def region(row):
        if row["STATE"] == 1:
            if row.get("SOUTHJ", 0) == 1:
                return "NJ_South"
            if row.get("CENTRALJ", 0) == 1:
                return "NJ_Central"
            if row.get("NORTHJ", 0) == 1:
                return "NJ_North"
            return "NJ_Other"
        if row.get("PA1", 0) == 1:
            return "PA_Philadelphia"
        if row.get("PA2", 0) == 1:
            return "PA_Easton"
        return "PA_Other"

    df["region"] = df.apply(region, axis=1)
    df["chain"] = df["CHAIN"].astype("Int64").astype(str)
    return df


def mean_se(s):
    s = pd.Series(s).dropna()
    n = len(s)
    if n == 0:
        return np.nan, np.nan, 0
    return float(s.mean()), float(s.std(ddof=1) / np.sqrt(n)), int(n)


def stars(p):
    if pd.isna(p):
        return ""
    if p < 0.01:
        return "***"
    if p < 0.05:
        return "**"
    if p < 0.10:
        return "*"
    return ""
