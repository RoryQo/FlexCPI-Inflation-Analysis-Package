
<h1 align="center">FlexCPI: Custom Consumer Price Index Toolkit</h1>
 
<p align="center">
  <a href="https://test.pypi.org/project/flexcpi/">
    <img src="https://img.shields.io/badge/test%20PyPI-flexcpi-blue" alt="Test PyPI">
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
    <td>3. <a href="#package-structure">Package Structure</a></td>
    <td>4. <a href="#core-functions">Core Functions</a></td>
  </tr>
  <tr>
    <td>5. <a href="#usage-example">Usage Example</a></td>
    <td>6. <a href="#requirements">Requirements</a></td>
  </tr>
  <tr>
    <td>7. <a href="#license">License</a></td>
    <td>8. <a href="#contributing">Contributing</a></td>
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

## Installation

Install from **Test PyPI**:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple flexcpi
```

---

## Requirements

- `pandas`
- `requests`
- `matplotlib`

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

## Package Structure

```
flexcpi/
├── __init__.py
├── toolkit.py
└── data/
    ├── cu.series.txt
    ├── cu.item.txt
    ├── cu.area.txt
    ├── bls_cpi_weights_table1.csv
    └── bls_cpi_weights_table2.csv
```

---

## Core Functions

| Function | Purpose |
|---------|---------|
| `load_catalog_tables()` | Load CPI metadata: series, items, and areas |
| `load_weight_tables()` | Load cleaned BLS relative importance weight tables |
| `keyword_search_cpi()` | Search CPI catalog for keyword matches |
| `match_series_ids_to_weights()` | Fuzzy match series IDs to weighted categories |
| `fetch_cpi_series_data()` | Fetch monthly CPI values from BLS API |
| `compute_custom_cpi_index()` | Compute CPI index using matched weights |
| `fetch_actual_cpi_series()` | Fetch official CPI series from BLS for comparison |
| `plot_custom_cpi()` | Plot custom CPI and optionally official CPI |


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

### `match_series_ids_to_weights(series_ids, full_catalog, weights_df, use='cpi_u_weight', cutoff=0.7)`
- **Inputs:** Series ID list, catalog, weights table, weight type, match cutoff
- **Outputs:** `DataFrame` with series_id, item_name, matched_category, weight, normalized_weight
- **Description:** Matches each series to its category and assigns normalized weights.

---

### `fetch_cpi_series_data(series_ids, start_year=2020, end_year=2025, api_key=None)`
- **Inputs:** Series ID list, year range, optional API key
- **Outputs:** `DataFrame` with year, month, value, series_id
- **Description:** Retrieves time series CPI values from the BLS API.

---

### `compute_custom_cpi_index(matched_df, start_year=2020, end_year=2025, api_key=None)`
- **Inputs:** Matched DataFrame, year range, API key
- **Outputs:** `DataFrame` with weighted CPI values over time
- **Description:** Computes index using weights to form a custom CPI.

---
### `fetch_actual_cpi_series(series_id, start_year, end_year, api_key)`
- **Inputs:** CPI series ID, year range, BLS API key
- **Outputs:** Official CPI `DataFrame` (date and value)
- **Description:** Retrieves a standard CPI series from BLS.

---

### `plot_custom_cpi(custom_cpi_df, compare_to_actual=False, api_key=None, actual_series_id='CUSR0000SA0', title='Custom CPI Index Over Time')`
- **Inputs:** Computed custom CPI DataFrame, compare flag, optional API key, actual series ID, plot title
- **Outputs:** Matplotlib plot
- **Description:** Visualizes the custom CPI trend and optionally overlays official CPI.

---

## Usage Example

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


