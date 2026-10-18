# Replication of Card and Krueger (1994), "Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania"

This repository replicates three tables and one figure from Card and Krueger (1994, AER):

- Table 2: selected means in Wave 1 and Wave 2, New Jersey vs. Pennsylvania.
- Table 3: average FTE employment before and after the New Jersey minimum-wage increase.
- Table 4: reduced-form models for the change in FTE employment.
- Figure 1: distribution of starting wage rates in February 1992 and November 1992.

## Replication process

1. Raw data: `data/raw/public.csv` (410 fast-food stores, 46 columns).
2. Cleaning: `code/clean.py` constructs FTE employment, wage groups, the initial wage gap, price variables, region dummies, and the analysis sample.
3. Tables: `code/tables.py` reproduces Table 2, Table 3, Table 4, and one independent extension.
4. Figure: `code/figure.py` reproduces Figure 1 and saves the underlying plotting data.
5. Report: `code/make_report.py` writes `report_final.md`, which can be exported to `report.pdf`.
6. `code/run_all.py` runs all steps in order.

## How to run

```bash
pip install -r requirements.txt
python code/run_all.py