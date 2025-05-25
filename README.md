<h1 align="center">FlexCPI: A Python Package for Custom CPI Analysis</h1>
 
<p align="center">
  <a href="https://pypi.org/project/flexcpi/">
    <img src="https://img.shields.io/pypi/v/flexcpi?label=PyPI&logo=pypi&logoColor=white&labelColor=grey&color=blue" alt="PyPI package">
  </a>
</p>

<p align="center">
  <em>FlexCPI is under active development for inflation analysis and customized economic indexing.</em>
</p>

<table align="center">
  <tr>
    <td colspan="2" align="center"><strong>Table of Contents</strong></td>
  </tr>
  <tr>
    <td>1. <a href="#overview">Overview</a></td>
    <td>2. <a href="#installation">Installation</a></td>
  </tr>
  <tr>
    <td>3. <a href="#requirements">Requirements</a></td>
    <td>4. <a href="#bls-api-key-requirement">BLS API Key Requirement</a></td>
  </tr>
  <tr>
    <td>5. <a href="#package-structure">Package Structure</a></td>
    <td>6. <a href="#core-functions">Core Functions</a></td>
  </tr>
  <tr>
    <td>7. <a href="#function-inputsoutputs">Function Inputs/Outputs</a></td>
    <td>8. <a href="#usage-example">Usage Example</a></td>
  </tr>
  <tr>
    <td>9. <a href="#license">License</a></td>
    <td>10. <a href="#contributing">Contributing</a></td>
  </tr>
</table>


---

## Overview

**FlexCPI** is a Python package for creating and analyzing **custom Consumer Price Index (CPI) baskets** using Bureau of Labor Statistics (BLS) data. It allows users to:

- Search CPI series by keyword and region
- Match series to official expenditure weights
- Construct custom CPI indexes using weighted BLS series
- Plot and compare with official CPI indexes

This toolkit is ideal for economic researchers, policy analysts, and students of macroeconomics who want flexible, reproducible CPI constructions.

---

## Installation

Install from **PyPI**:

```bash
pip install flexcpi
```

---
## Requirements

- `pandas`
- `requests`
- `matplotlib`
- `statsmodels`

  > **Important:**  
> Before using most functions in `flexcpi`, you must first load the necessary data tables using the following functions:
>
> ```python
> from flexcpi.toolkit import load_catalog_tables, load_weight_tables
>
> full_catalog = load_catalog_tables()
> table1, table2 = load_weight_tables()
> ```
>
> These data tables are required inputs for key operations like matching series to weights and computing custom CPI indexes.

---


## BLS API Key Requirement

The `flexcpi` package is fundamentally built on top of the U.S. Bureau of Labor Statistics (BLS) data infrastructure.  
It enables users to search, extract, and customize Consumer Price Index (CPI) series directly from BLS.

To access CPI data, users must register for a free BLS API key.

**How to get an API key:**

1. Visit the [BLS Public Data API Registration Page](https://data.bls.gov/registrationEngine/)
2. Fill out your name and email to request an API key.
3. BLS will email you a unique `registrationkey`.

**How to use the API key:**

Pass the key to any function that supports the `api_key` parameter:

```python
custom_cpi_df = compute_custom_cpi_index(matched_df, start_year=2020, end_year=2025, api_key="your_api_key")
```




---



## Package Structure

```
FlexCPI/
│
├── flexcpi/                  
│   ├── __init__.py
│   ├── toolkit.py
│   └── data/
│       ├── cu.series.txt
│       ├── cu.item.txt
│       ├── cu.area.txt
│       ├── bls_cpi_weights_table1.csv
│       └── bls_cpi_weights_table2.csv
│
├── examples/                 
│   └── usage_examples.ipynb
│
├── .github/                
│   └── workflows/
│       └── publish.yml
│
├── pyproject.toml          
├── README.md
└── LICENSE

```

---

## Core Functions

| Function | Purpose |
|---------|---------|
| `load_catalog_tables()` | Load CPI metadata: series, items, and areas |
| `load_weight_tables()` | Load cleaned BLS relative importance weight tables |
| `keyword_search_cpi()` | Search CPI catalog for keyword matches |
| `auto_select_series()` | Automatically select series IDs by keyword from catalog |
| `match_series_ids_to_weights()` | Fuzzy match series IDs to weighted categories |
| `assign_manual_weights()` | Manually assign weights to selected CPI series |
| `fetch_cpi_series_data()` | Fetch monthly CPI values from BLS API |
| `compute_custom_cpi_index()` | Compute CPI index using matched or manual weights |
| `compute_inflation_rate()` | Calculate year-over-year inflation from CPI index |
| `fetch_actual_cpi_series()` | Fetch official CPI series from BLS for comparison |
| `plot_custom_cpi()` | Plot custom CPI and optionally official CPI |
| `plot_inflation_comparison()` | Compare custom YoY inflation to official CPI inflation |
| `export_cpi_data()` | Export custom CPI index and weights to CSV files |
| `forecast_custom_cpi()` | Fit ARIMA model to custom CPI index and forecast future values |


> **Important:**  
> Before using most functions in `flexcpi`, you must first load the necessary data tables:
> Reference Requirements for code instructions
>
> - These data tables are required inputs for key operations like matching series to weights and computing custom CPI indexes.
---

## Function Inputs/Outputs

### `load_catalog_tables()`
- **Inputs:** None

- **Outputs:** `DataFrame` with merged BLS catalog (series, item, area)

- **Description:** Merges CPI series metadata into one DataFrame.
  - **Necessary** to load to use following functions (reference requirements for details)

---

### `load_weight_tables()`
- **Inputs:** None

- **Outputs:** Two `DataFrame`s: Table 1 and Table 2 weights.

- **Description:** Loads and cleans official relative importance weights.
  - **Necessary** to load to use following functions (reference requirements for details)


---

### `keyword_search_cpi(full_catalog, keyword, area_filter=None, max_results=20)`
- **Inputs:** Catalog DataFrame, search keyword, area filter (optional), result limit

- **Outputs:** Filtered `DataFrame` with series_id, item_name, and area_name

- **Description:** Finds matching series from the catalog based on keyword.

---
### `auto_select_series(keywords, full_catalog, area_filter="U.S. city average", max_per_keyword=1)`

- **Inputs:**
  - `keywords` (list of str): Keywords to search in the CPI item names.
  - `full_catalog` (DataFrame): Loaded CPI catalog from `load_catalog_tables()`.
  - `area_filter` (str): Optional filter for CPI region (default "U.S. city average").
  - `max_per_keyword` (int): Max number of series returned per keyword.

- **Outputs:**
  - `list`: A list of matched CPI series IDs.

- **Description:**
  This function provides a simple way to automatically select relevant CPI series based on keyword searches. It filters by area and returns the most relevant series IDs.





---

### `match_series_ids_to_weights(series_ids, full_catalog, weights_df, use='cpi_u_weight', cutoff=0.7)`
- **Inputs:** Series ID list, catalog, weights table, weight type, match cutoff

- **Outputs:** `DataFrame` with series_id, item_name, matched_category, weight, normalized_weight

- **Description:** Matches each series to its category and assigns normalized weights.

---

### `assign_manual_weights(series_ids, weights_dict)`
- **Inputs:**  
  - `series_ids` (list): List of CPI series IDs  
  - `weights_dict` (dict): Dictionary of user-defined weights keyed by series ID  

- **Outputs:**  
  - `DataFrame` with columns: `series_id`, `raw_weight`, and `normalized_weight`  

- **Description:**  
  Allows users to manually specify weights for each CPI series in their basket.  
  The output can be used directly with `compute_custom_cpi_index()`.

---

### `fetch_cpi_series_data(series_ids, start_year=2020, end_year=2025, api_key=None)`
- **Inputs:**
  - `Series ID list`
  - `year range`
  - `API key`

- **Outputs:** `DataFrame` with year, month, value, series_id

- **Description:** Retrieves time series CPI values from the BLS API.

---

### `compute_custom_cpi_index(matched_df, start_year=2020, end_year=2025, api_key=None)`
- **Inputs:**
  - `Matched DataFrame`
  - `year range`
  - `API key`

- **Outputs:** `DataFrame` with weighted CPI values over time

- **Description:** Computes index using weights to form a custom CPI.

---

### `fetch_actual_cpi_series(series_id, start_year, end_year, api_key)`
- **Inputs:**
  - `CPI series ID`
  - `year range`
  - `BLS API key`
 
- **Outputs:** Official CPI `DataFrame` (date and value)

- **Description:** Retrieves a standard CPI series from BLS.

---

### `compute_inflation_rate(cpi_df)`
- **Inputs:**  
  - `cpi_df` (DataFrame): A DataFrame containing at least `["date", "custom_cpi_index"]` columns.

- **Outputs:**  
  - `DataFrame`: The input DataFrame with an additional `yoy_inflation` column (year-over-year % change).

- **Description:**  
  Calculates the year-over-year inflation rate for each month using the custom CPI index.


---

### `plot_custom_cpi(custom_cpi_df, compare_to_actual=False, api_key=None, actual_series_id='CUSR0000SA0', title='Custom CPI Index Over Time')`
- **Inputs:**
  - `Computed custom CPI DataFrame`
  - `compare flag`
  - `optional API key`
  - `actual series ID`
  - `plot title`

- **Outputs:** Matplotlib plot

- **Description:** Visualizes the custom CPI trend and optionally overlays official CPI.

---


### `plot_inflation_comparison(custom_df, compare_to_actual=False, actual_series_id="CUSR0000SA0", api_key=None, title="Custom vs Official YoY Inflation")`
- **Inputs:**
  - `custom_df` (DataFrame): A DataFrame with `date` and `yoy_inflation` columns (e.g. from `compute_inflation_rate()`).
  - `compare_to_actual` (bool): Whether to plot official CPI YoY inflation alongside custom inflation.
  - `actual_series_id` (str): BLS series ID for official CPI (default is "CUSR0000SA0" for All Items, U.S. city average).
  - `api_key` (str): Your BLS API key. Required if `compare_to_actual=True`.
  - `title` (str): Plot title.

- **Outputs:**
  - Displays a matplotlib line plot comparing custom and official YoY inflation.

- **Description:**
  This function creates a visual comparison between the custom year-over-year inflation index and the official BLS CPI inflation index, if enabled.

---

### `export_cpi_data(index_df=custom_index, basket_df=matched_df, out_dir="outputs", base_name="Name")`

**Description:**  
Exports the custom CPI index and basket definition to CSV files for external use or archiving.

**Inputs:**
- `index_df` (`pandas.DataFrame`): Output from `compute_custom_cpi_index()`. Must include `date` and `custom_cpi_index`.
- `basket_df` (`pandas.DataFrame`): Output from `match_series_ids_to_weights()` or `assign_manual_weights()`.
- `out_dir` (`str`, optional): Folder path to save the files. Defaults to the current directory `"."`.
- `base_name` (`str`, optional): Prefix for output filenames. Defaults to `"custom_cpi"`.

**Outputs:**
- Saves two CSV files:
  - `<base_name>_index.csv`: CPI index values with dates.
  - `<base_name>_basket.csv`: Series IDs, item names, matched categories, raw and normalized weights.


---

### `forecast_custom_cpi(custom_cpi_df, forecast_periods=12, order=(1,1,1), plot=True)`

**Description:**  
Forecasts future values of a computed custom CPI index using ARIMA modeling.

**Inputs:**
- `custom_cpi_df` (`pd.DataFrame`): Output from `compute_custom_cpi_index()` containing `"date"` and `"custom_cpi_index"` columns.
- `forecast_periods` (`int`): Number of months to forecast (default is 12).
- `order` (`tuple`): ARIMA model order in the form `(p, d, q)` (default is `(1, 1, 1)`).
- `plot` (`bool`): Whether to plot the forecasted index alongside historical data (default is `True`).

**Output:**
- `pd.DataFrame`: DataFrame containing the original custom CPI index plus forecasted values.

**Behavior:**
- Fits an ARIMA model using the `statsmodels` library to the provided CPI index.
- Automatically extends the time series into the future and appends the forecasted CPI values.
- Optionally generates a line plot showing historical and projected CPI index.


---

## Usage Example


An example Jupyter notebook demonstrating all core functions of the `flexcpi` package is available in the repository:

[![Usage Notebook](https://img.shields.io/badge/Usage%20Notebook-lightgrey?logo=jupyter&logoColor=orange&labelColor=black)](https://github.com/RoryQo/FlexCPI/blob/main/examples/usage_examples.ipynb)

This notebook walks through:
- Loading catalog and weight tables
- Defining a custom CPI basket
- Computing weighted inflation
- Visualizing inflation trends


**Sample Snippet**
```python
from flexcpi import (
    load_catalog_tables, load_weight_tables,
    keyword_search_cpi, match_series_ids_to_weights,
    compute_custom_cpi_index, plot_custom_cpi
)

# Load data
catalog = load_catalog_tables()
table1, _ = load_weight_tables()

# Define your basket
series_ids = ["CUSR0000SAS2RS", "CUSR0000SA0L1", "CUSR0000SA311", "CUSR0000SAS24"]
matched = match_series_ids_to_weights(series_ids, catalog, table1, use="cpi_u_weight")

# Compute index
custom_cpi = compute_custom_cpi_index(matched, start_year=2019, end_year=2024, api_key="YOUR_BLS_KEY")

# Plot
plot_custom_cpi(custom_cpi, compare_to_actual=True, api_key="YOUR_BLS_KEY")
```

---




## License

This package is distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contributing

All contributions are welcome! Open an issue or pull request to:

- Add support for new CPI series or weighting schemes
- Improve performance of the matching logic
- Enhance visualization or reporting capabilities

---


