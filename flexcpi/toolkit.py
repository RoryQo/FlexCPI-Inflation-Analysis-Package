import pandas as pd
import requests
import matplotlib.pyplot as plt
from importlib.resources import files
from difflib import get_close_matches
import difflib


# === Data Loading ===

def load_catalog_tables():
    base_path = files("flexcpi.data")
    catalog_df = pd.read_csv(base_path / "cu.series.txt", sep="\\t", engine="python", on_bad_lines='skip')
    item_df = pd.read_csv(base_path / "cu.item.txt", sep="\\t", engine="python", on_bad_lines='skip')
    area_df = pd.read_csv(base_path / "cu.area.txt", sep="\\t", engine="python", on_bad_lines='skip')
    catalog_df.columns = catalog_df.columns.str.strip()
    item_df.columns = item_df.columns.str.strip()
    area_df.columns = area_df.columns.str.strip()
    full_catalog = catalog_df.merge(item_df, on="item_code").merge(area_df, on="area_code")
    return full_catalog

def load_weight_tables():
    base_path = files("flexcpi.data")
    table1 = pd.read_csv(base_path / "bls_cpi_weights_table1.csv")
    table2 = pd.read_csv(base_path / "bls_cpi_weights_table2.csv")
    for table in [table1, table2]:
        table["category"] = table["category"].str.strip().str.lower()
        table["cpi_u_weight"] = table["cpi_u_weight"].astype(float)
    return table1, table2

# === Searching ===

def keyword_search_cpi(full_catalog, keyword, area_filter=None, max_results=20):
    """
    Search CPI catalog for a keyword in item or area name, with optional area filtering.

    Parameters:
        full_catalog (pd.DataFrame): Merged catalog of CPI series, items, and areas.
        keyword (str): Search term (case-insensitive).
        area_filter (str, optional): Only return results from this area (e.g., "U.S. city average").
        max_results (int): Max number of results to return.

    Returns:
        pd.DataFrame: Matching series with readable item and area names.
    """
    mask = full_catalog["item_name"].str.contains(keyword, case=False, na=False) | \
           full_catalog["area_name"].str.contains(keyword, case=False, na=False)

    if area_filter:
        area_mask = full_catalog["area_name"].str.contains(area_filter, case=False, na=False)
        mask &= area_mask

    return full_catalog.loc[mask, ["series_id", "item_name", "area_name"]].drop_duplicates().head(max_results)




def auto_select_series(keywords, full_catalog, area_filter="U.S. city average", max_per_keyword=1):
    """
    Automatically selects series IDs from CPI catalog based on keyword matches.

    Parameters:
        keywords (list of str): List of item keywords to search for.
        full_catalog (pd.DataFrame): The CPI full catalog loaded with `load_catalog_tables()`.
        area_filter (str): Area filter for CPI data (default "U.S. city average").
        max_per_keyword (int): Max number of series to return per keyword.

    Returns:
        list: Series IDs corresponding to matched keywords.
    """
    selected_series = []
    for keyword in keywords:
        matches = full_catalog[
            full_catalog["item_name"].str.contains(keyword, case=False, na=False) &
            full_catalog["area_name"].str.contains(area_filter, case=False, na=False)
        ]
        matches = matches[["series_id", "item_name", "area_name"]].drop_duplicates()
        selected_series.extend(matches["series_id"].head(max_per_keyword).tolist())
    return selected_series


# === Matching ===


def match_series_ids_to_weights(series_ids, full_catalog, weights_df, use="cpi_u_weight", cutoff=0.7):
    """
    Match series IDs to CPI weight categories using substring and fuzzy matching.

    Parameters:
        series_ids (list): List of CPI series IDs (e.g. CUSR0000SAS2RS).
        full_catalog (DataFrame): CPI catalog merged with item and area descriptions.
        weights_df (DataFrame): Cleaned weight table with columns: 'category', 'cpi_u_weight', 'cpi_w_weight'.
        use (str): Which weight column to use ('cpi_u_weight' or 'cpi_w_weight').
        cutoff (float): Fuzzy match cutoff (between 0 and 1).

    Returns:
        DataFrame: Matches with raw and normalized weights.
    """
    # Clean inputs
    full_catalog["series_id"] = full_catalog["series_id"].astype(str).str.strip()
    full_catalog["item_name"] = full_catalog["item_name"].astype(str).str.strip().str.lower()
    weights_df["category"] = weights_df["category"].astype(str).str.strip().str.lower()

    results = []

    for sid in series_ids:
        row = full_catalog[full_catalog["series_id"] == sid]
        if row.empty:
            print(f"[SKIP] Series ID not found in catalog: {sid}")
            continue

        item_name = row["item_name"].values[0].lower()

        # Step 1: Substring match
        substring_matches = weights_df[weights_df["category"].apply(lambda x: x in item_name or item_name in x)]
        if not substring_matches.empty:
            best_match = substring_matches.iloc[0]
            matched_category = best_match["category"]
            weight = best_match[use]
        else:
            # Step 2: Fuzzy match fallback
            match = difflib.get_close_matches(item_name, weights_df["category"], n=1, cutoff=cutoff)
            if match:
                matched_category = match[0]
                weight = weights_df.loc[weights_df["category"] == matched_category, use].values[0]
            else:
                print(f"[MISS] No match for: {item_name.title()} (Series ID: {sid})")
                continue

        results.append({
            "series_id": sid,
            "item_name": item_name,
            "matched_category": matched_category,
            "weight": weight
        })

    # Build results DataFrame
    df = pd.DataFrame(results)
    total = df["weight"].sum()

    if total == 0:
        raise ValueError("Total weight is zero. Check fuzzy match cutoff or input series.")

    df["normalized_weight"] = df["weight"] / total
    return df

# === Fetch CPI Series Data ===

def assign_manual_weights(series_ids, weights_dict):
    """
    Assign user-defined weights to a list of CPI series.

    Parameters:
        series_ids (list): List of BLS series IDs (e.g., ["CUSR0000SAS2RS", "CUSR0000SA0L1"]).
        weights_dict (dict): Dictionary mapping series_id -> raw weight value 
                             (e.g., {"CUSR0000SAS2RS": 0.4, "CUSR0000SA0L1": 0.6}).

    Returns:
        pd.DataFrame: DataFrame with series_id, raw weight, and normalized weight.

    Raises:
        ValueError: If any series_id is not in the provided weights_dict or if weights sum to zero.
    """
    import pandas as pd

    # Validate input
    missing = [sid for sid in series_ids if sid not in weights_dict]
    if missing:
        raise ValueError(f"The following series_ids are missing weights: {missing}")

    # Build DataFrame
    df = pd.DataFrame({
        "series_id": series_ids,
        "raw_weight": [weights_dict[sid] for sid in series_ids]
    })

    total = df["raw_weight"].sum()
    if total == 0:
        raise ValueError("Total weight must be greater than zero.")

    df["normalized_weight"] = df["raw_weight"] / total
    return df


# === Fetch CPI Series Data ===

def fetch_cpi_series_data(series_ids, start_year=2020, end_year=2025, api_key=None):
    headers = {'Content-type': 'application/json'}
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year)
    }
    if api_key:
        payload["registrationkey"] = api_key

    response = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    rows = []
    for series in data['Results']['series']:
        sid = series['seriesID']
        for entry in series['data']:
            if entry['period'].startswith("M"):
                rows.append({
                    "series_id": sid,
                    "year": int(entry['year']),
                    "month": int(entry['period'][1:]),
                    "value": float(entry['value'])
                })
    return pd.DataFrame(rows)

# === Custom CPI Index Construction ===

def compute_custom_cpi_index(matched_df, start_year=2020, end_year=2025, api_key=None):
    cpi_df = fetch_cpi_series_data(matched_df["series_id"].tolist(), start_year, end_year, api_key)
    weights = dict(zip(matched_df["series_id"], matched_df["normalized_weight"]))
    cpi_df["weight"] = cpi_df["series_id"].map(weights)
    cpi_df["weighted_value"] = cpi_df["value"] * cpi_df["weight"]
    grouped = cpi_df.groupby(["year", "month"])["weighted_value"].sum().reset_index(name="custom_cpi_index")
    grouped["date"] = pd.to_datetime(grouped["year"].astype(str) + "-" + grouped["month"].astype(str).str.zfill(2) + "-01")
    return grouped.sort_values("date")

# === Plotting ===

def fetch_actual_cpi_series(series_id, start_year, end_year, api_key):
    response = requests.post(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        json={
            "seriesid": [series_id],
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": api_key
        },
        headers={"Content-type": "application/json"}
    )
    response.raise_for_status()
    data = response.json()
    series_data = data["Results"]["series"][0]["data"]
    df = pd.DataFrame(series_data)
    df["value"] = df["value"].astype(float)
    df["date"] = pd.to_datetime(df["year"] + "-" + df["period"].str[1:] + "-01")
    return df[["date", "value"]].sort_values("date")

def plot_custom_cpi(custom_cpi_df, compare_to_actual=False, api_key=None, actual_series_id="CUSR0000SA0", title="Custom CPI Index Over Time"):
    plt.figure(figsize=(10, 6))
    plt.plot(custom_cpi_df["date"], custom_cpi_df["custom_cpi_index"], label="Custom CPI", linewidth=2)
    if compare_to_actual:
        start_year = custom_cpi_df["date"].dt.year.min()
        end_year = custom_cpi_df["date"].dt.year.max()
        actual_df = fetch_actual_cpi_series(actual_series_id, start_year, end_year, api_key)
        plt.plot(actual_df["date"], actual_df["value"], label="Official CPI", linestyle='--')
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("CPI Index")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# === Plotting infl ===

import matplotlib.pyplot as plt

def plot_inflation_comparison(custom_df, compare_to_actual=False, actual_series_id="CUSR0000SA0", api_key=None, title="Custom vs Official YoY Inflation"):
    """
    Plot YoY inflation from custom CPI, optionally comparing to official CPI series.

    Parameters:
        custom_df (pd.DataFrame): Must contain 'date' and 'yoy_inflation' columns.
        compare_to_actual (bool): If True, also fetch and plot official CPI inflation.
        actual_series_id (str): BLS series ID for the official CPI (default: All items).
        api_key (str): BLS API key, required if compare_to_actual is True.
        title (str): Title for the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(custom_df["date"], custom_df["yoy_inflation"], label="Custom YoY Inflation", linewidth=2)

    if compare_to_actual:
        actual_df = fetch_actual_cpi_series(actual_series_id, 
                                            start_year=custom_df["date"].dt.year.min(), 
                                            end_year=custom_df["date"].dt.year.max(), 
                                            api_key=api_key)
        actual_df["yoy_inflation"] = actual_df["value"].pct_change(periods=12) * 100
        plt.plot(actual_df["date"], actual_df["yoy_inflation"], label="Official YoY Inflation", linestyle='--')

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Year-over-Year Inflation (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Inflation ===

def compute_inflation_rate(cpi_df):
    """
    Compute year-over-year (YoY) inflation rates from a custom CPI index DataFrame.

    Parameters:
        cpi_df (pd.DataFrame): Must include columns ['date', 'custom_cpi_index']

    Returns:
        pd.DataFrame: Original DataFrame with added 'yoy_inflation' column (in %)
    """
    cpi_df = cpi_df.sort_values("date").copy()
    cpi_df["yoy_inflation"] = cpi_df["custom_cpi_index"].pct_change(periods=12) * 100
    return cpi_df


# === Export ===

def export_cpi_data(index_df, basket_df, out_dir=".", base_name="custom_cpi"):
    """
    Save custom CPI index and basket definition to CSV.

    Parameters:
        index_df (DataFrame): Output from compute_custom_cpi_index().
        basket_df (DataFrame): Output from match_series_ids_to_weights().
        out_dir (str): Folder to save into.
        base_name (str): File name prefix.
    """
    import os
    index_path = os.path.join(out_dir, f"{base_name}_index.csv")
    basket_path = os.path.join(out_dir, f"{base_name}_basket.csv")
    index_df.to_csv(index_path, index=False)
    basket_df.to_csv(basket_path, index=False)
    print(f"Saved index to {index_path}")
    print(f"Saved basket to {basket_path}")

