
from pathlib import Path
import math
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIRS = [
    BASE_DIR / "data",
    BASE_DIR / "dataset",
    BASE_DIR / "dataset" / "csv",
]


def load_dataset(filename):
    for folder in DATA_DIRS:
        path = folder / filename
        if path.exists():
            return pd.read_csv(path)
    raise FileNotFoundError(
        f"{filename} not found in data/ or dataset/csv/"
    )


def haversine(lat1, lon1, lat2, lon2):
    """Calculate straight-line distance in kilometres."""
    radius = 6371.0

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return radius * 2 * math.atan2(
        math.sqrt(a), math.sqrt(1 - a)
    )


def optimize_route(max_stops=None):
    bins = load_dataset("smart_bins.csv")
    hotspots = load_dataset("hotspot_prediction.csv")

    required = {"latitude", "longitude"}
    missing = required - set(bins.columns)

    if missing:
        raise ValueError(
            f"smart_bins.csv is missing columns: {sorted(missing)}"
        )

    # Match hotspot risk by zone when possible.
    if "zone" in bins.columns and "zone" in hotspots.columns:
        risk_column = next(
            (
                column for column in
                ["risk_score", "threat_score", "hotspot_risk"]
                if column in hotspots.columns
            ),
            None,
        )

        if risk_column:
            risks = hotspots[["zone", risk_column]].copy()
            risks[risk_column] = pd.to_numeric(
                risks[risk_column], errors="coerce"
            )
            risks = risks.groupby("zone", as_index=False)[
                risk_column
            ].max()

            bins = bins.merge(risks, on="zone", how="left")
            if risk_column != "risk_score":
                bins = bins.rename(
                    columns={risk_column: "risk_score"}
                )

    if "risk_score" not in bins.columns:
        fill_column = next(
            (column for column in
             ["fill_percent", "capacity_percent", "fill_level",
              "bin_fill_percent"]
             if column in bins.columns),
            None,
        )
        if fill_column:
            bins["risk_score"] = pd.to_numeric(
                bins[fill_column], errors="coerce"
            ).fillna(0)
        else:
            bins["risk_score"] = 0

    bins["latitude"] = pd.to_numeric(
        bins["latitude"], errors="coerce"
    )
    bins["longitude"] = pd.to_numeric(
        bins["longitude"], errors="coerce"
    )
    bins["risk_score"] = pd.to_numeric(
        bins["risk_score"], errors="coerce"
    ).fillna(0)

    bins = bins.dropna(subset=["latitude", "longitude"])

    if bins.empty:
        raise ValueError(
            "No valid bin coordinates found in smart_bins.csv."
        )

    # Process highest-risk bins first.
    bins = bins.sort_values("risk_score", ascending=False)

    if max_stops is not None:
        bins = bins.head(max_stops)

    remaining = bins.to_dict("records")
    route = []
    current = None
    total_distance = 0.0

    # Nearest-neighbour route, starting with the highest-risk bin.
    while remaining:
        if current is None:
            next_stop = remaining.pop(0)
        else:
            next_stop = min(
                remaining,
                key=lambda stop: haversine(
                    current["latitude"],
                    current["longitude"],
                    stop["latitude"],
                    stop["longitude"],
                ),
            )
            remaining.remove(next_stop)

            total_distance += haversine(
                current["latitude"],
                current["longitude"],
                next_stop["latitude"],
                next_stop["longitude"],
            )

        next_stop["route_order"] = len(route) + 1
        route.append(next_stop)
        current = next_stop

    result = pd.DataFrame(route)
    output_dir = BASE_DIR / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "optimized_routes.csv"
    result.to_csv(output_path, index=False)

    print(f"Route created: {len(route)} stops")
    print(f"Estimated straight-line distance: {total_distance:.2f} km")
    print(f"Saved to: {output_path}")

    return result
