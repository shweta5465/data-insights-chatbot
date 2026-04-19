import pandas as pd

def load_data():
    df = pd.read_csv("data/sales_data.csv", encoding="latin1")
    return df

def get_summary(df):
    summary = {
        "total_rows": len(df),
        "columns": list(df.columns),
        "sample": df.head(5).to_string()
    }
    return summary

def get_stats(df):
    return df.describe().to_string()