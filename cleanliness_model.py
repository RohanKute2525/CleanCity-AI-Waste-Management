from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent


def load_dataset(name):

    files = list(BASE_DIR.rglob(name))

    if not files:
        raise FileNotFoundError(
            f"{name} not found"
        )

    file_path = files[0]

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    return pd.read_excel(file_path)


def calculate_cleanliness_score():

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------

    bins = load_dataset(
        "smart_bins.csv"
    )

    complaints = load_dataset(
        "complaints.csv"
    )

    hotspots = load_dataset(
        "hotspot_prediction.csv"
    )

    waste = load_dataset(
        "waste_detection.csv"
    )


    # --------------------------------------------------
    # BIN SCORE
    # --------------------------------------------------

    fill_column = None

    for column in [
        "fill_percent",
        "fill_level",
        "bin_fill_percent",
        "avg_fill_percent",
        "fill_percentage"
    ]:

        if column in bins.columns:

            fill_column = column
            break


    if fill_column:

        fill = pd.to_numeric(
            bins[fill_column],
            errors="coerce"
        ).mean()

        if pd.isna(fill):
            fill = 50

    else:

        fill = 50


    bin_score = max(
        0,
        min(
            100,
            100 - fill
        )
    )


    # --------------------------------------------------
    # COMPLAINT SCORE
    # --------------------------------------------------

    complaint_count = len(
        complaints
    )

    complaint_score = max(
        0,
        100 - (
            complaint_count / 20
        )
    )


    # --------------------------------------------------
    # HOTSPOT SCORE
    # --------------------------------------------------

    hotspot_count = 0

    if "hotspot_label" in hotspots.columns:

        labels = (
            hotspots["hotspot_label"]
            .astype(str)
            .str.lower()
        )

        hotspot_count = int(
            labels.str.contains(
                "high|hotspot|true|yes",
                regex=True
            ).sum()
        )


    hotspot_score = max(
        0,
        100 - (
            hotspot_count / 5
        )
    )


    # --------------------------------------------------
    # WASTE SCORE
    # --------------------------------------------------

    waste_count = len(
        waste
    )

    waste_score = max(
        0,
        100 - (
            waste_count / 20
        )
    )


    # --------------------------------------------------
    # FINAL AI SCORE
    # --------------------------------------------------

    final_score = (

        bin_score * 0.40

        + complaint_score * 0.20

        + hotspot_score * 0.25

        + waste_score * 0.15

    )


    final_score = round(
        max(
            0,
            min(
                100,
                final_score
            )
        ),
        1
    )


    # --------------------------------------------------
    # RATING
    # --------------------------------------------------

    if final_score >= 90:

        rating = "Excellent"

    elif final_score >= 75:

        rating = "Good"

    elif final_score >= 60:

        rating = "Moderate"

    elif final_score >= 40:

        rating = "Poor"

    else:

        rating = "Critical"


    return {

        "score": final_score,

        "rating": rating,

        "bin_score": round(
            bin_score,
            1
        ),

        "complaint_score": round(
            complaint_score,
            1
        ),

        "hotspot_score": round(
            hotspot_score,
            1
        ),

        "waste_score": round(
            waste_score,
            1
        )

    }


if __name__ == "__main__":

    result = calculate_cleanliness_score()

    print()
    print("=" * 50)
    print("CLEAN CITY AI - CLEANLINESS SCORE")
    print("=" * 50)

    print(
        "Overall Score:",
        result["score"]
    )

    print(
        "Rating:",
        result["rating"]
    )

    print(
        "Bin Score:",
        result["bin_score"]
    )

    print(
        "Complaint Score:",
        result["complaint_score"]
    )

    print(
        "Hotspot Score:",
        result["hotspot_score"]
    )

    print(
        "Waste Score:",
        result["waste_score"]
    )

    print("=" * 50)
