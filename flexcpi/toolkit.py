import pandas as pd
import requests
import matplotlib.pyplot as plt
from importlib.resources import files
from difflib import get_close_matches

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

# === Matching ===

def match_series_ids_to_weights(series_ids, full_catalog, weights_df, use="cpi_u_weight", cutoff=0.7):
    full_catalog["series_id"] = full_catalog["series_id"].astype(str).str.strip()
    full_catalog["item_name"] = full_catalog["item_name"].astype(str).str.strip().str.lower()
    weights_df["category"] = weights_df["category"].astype(str).str.strip().str.lower()

    results = []
    for sid in series_ids:
        row = full_catalog[full_catalog["series_id"] == sid]
        if row.empty:
            print(f"[SKIP] Series ID not found in catalog: {sid}")
            continue

        item_name = row["item_name"].values[0]
        substring_matches = weights_df[weights_df["category"].apply(lambda x: x in item_name or item_name in x)]
        if not substring_matches.empty:
            best_match = substring_matches.iloc[0]
            weight = best_match[use]
        else:
            match = get_close_matches(item_name, weights_df["category"], n=1, cutoff=cutoff)
            if not match:
                print(f"[MISS] No match for: {item_name.title()} (Series ID: {sid})")
                continue
            weight = weights_df.loc[weights_df["category"] == match[0], use].values[0]

        results.append({
            "series_id": sid,
            "item_name": item_name,
            "matched_category": match[0] if not substring_matches.empty else best_match["category"],
            "weight": weight
        })

    df = pd.DataFrame(results)
    total = df["weight"].sum()
    df["normalized_weight"] = df["weight"] / total if total > 0 else 0
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
