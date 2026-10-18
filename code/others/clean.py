from pathlib import Path
import pandas as pd
from utils import load_public_csv, construct_variables


def main():
    root = Path(__file__).resolve().parents[1]
    raw = root / "data" / "raw" / "public.csv"
    outdir = root / "data" / "processed"
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_public_csv(raw)
    df = construct_variables(df)
    df.to_csv(outdir / "analysis.csv", index=False)

    table4_mask = (
        df["FTE1"].notna()
        & df["FTE2_adj"].notna()
        & df["WAGE_ST"].notna()
        & df["WAGE_ST2"].notna()
        & df["GAP"].notna()
    )

    flow = pd.DataFrame(
        {
            "step": [
                "raw rows",
                "FTE1 nonmissing",
                "FTE2_adj nonmissing",
                "balanced FTE sample",
                "Table 4 sample (FTE and wages both waves, GAP nonmissing)",
            ],
            "N": [
                len(df),
                int(df["FTE1"].notna().sum()),
                int(df["FTE2_adj"].notna().sum()),
                int(df["balanced"].sum()),
                int(table4_mask.sum()),
            ],
        }
    )
    flow.to_csv(outdir / "sample_flow.csv", index=False)
    print(f"Saved processed data to {outdir / 'analysis.csv'}")
    print(flow.to_string(index=False))


if __name__ == "__main__":
    main()
