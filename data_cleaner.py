import pandas as pd


def clean_dataframe(df):

    df = df.copy()

    # Replace empty strings with NA
    df.replace("", pd.NA, inplace=True)

    # Replace None with NA
    df.fillna(pd.NA, inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Try converting date columns
    for column in df.columns:

        if "date" in column.lower():

            try:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )
            except:
                pass

    # Convert amount columns to numeric

    for column in df.columns:

        if (
            "amount" in column.lower()
            or "revenue" in column.lower()
            or "value" in column.lower()
            or "gst" in column.lower()
        ):

            try:
                df[column] = (
                    df[column]
                    .astype(str)
                    .str.replace(",", "")
                )

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

            except:
                pass

    return df


def get_data_quality_report(df):

    total_missing = int(df.isna().sum().sum())

    report = []

    if total_missing > 0:

        report.append(
            f"⚠️ Dataset contains {total_missing} missing values."
        )

    duplicate_rows = int(df.duplicated().sum())

    if duplicate_rows > 0:

        report.append(
            f"⚠️ Found {duplicate_rows} duplicate rows."
        )

    if len(report) == 0:

        report.append(
            "✅ Data quality looks good."
        )

    return "\n".join(report)