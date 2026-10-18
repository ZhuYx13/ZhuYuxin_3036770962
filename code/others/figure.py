from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def distribution(df, wage_col, state_value, bins, labels):
    s = df.loc[df["STATE"] == state_value, wage_col].dropna()
    if len(s) == 0:
        return np.zeros(len(labels)), 0
    cats = pd.cut(s, bins=bins, labels=labels, right=False)
    counts = cats.value_counts().reindex(labels).fillna(0)
    return (counts / len(s) * 100).values, len(s)


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "processed" / "analysis.csv")
    outdir = root / "outputs" / "figures"
    outdir.mkdir(parents=True, exist_ok=True)

    bins = np.arange(4.20, 5.61, 0.10)
    labels = [f"{x:.2f}" for x in np.arange(4.25, 5.56, 0.10)]

    waves = [
        ("February 1992", "WAGE_ST"),
        ("November 1992", "WAGE_ST2"),
    ]

    fig, axes = plt.subplots(2, 1, figsize=(8, 10))
    data_rows = []

    for ax, (title, col) in zip(axes, waves):
        nj, n_nj = distribution(df, col, 1, bins, labels)
        pa, n_pa = distribution(df, col, 0, bins, labels)
        x = np.arange(len(labels))

        ax.bar(x - 0.2, nj, width=0.4, color="black", label="New Jersey")
        ax.bar(
            x + 0.2,
            pa,
            width=0.4,
            color="white",
            edgecolor="black",
            hatch="///",
            label="Pennsylvania",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45)
        ax.set_ylabel("Percent of Stores")
        ax.set_xlabel("Wage Range")
        ax.set_title(title)
        ax.legend()

        for lab, v_nj, v_pa in zip(labels, nj, pa):
            data_rows.append(
                {"wave": title, "wage_bin": lab, "NJ_percent": v_nj, "PA_percent": v_pa,
                 "N_NJ": n_nj, "N_PA": n_pa}
            )

    plt.tight_layout()
    fig.savefig(outdir / "figure1.png", dpi=200)
    pd.DataFrame(data_rows).to_csv(outdir / "figure1_data.csv", index=False)
    print(f"Saved figure to {outdir / 'figure1.png'}")


if __name__ == "__main__":
    main()