import argparse
import os
import pandas as pd
from pendulum import from_format
from pymongo import MongoClient

parser = argparse.ArgumentParser(
    description="Process stock data for a given date range."
)
parser.add_argument(
    "--start_date",
    type=str,
    required=True,
    help="The start date in YYYY-MM-DD format",
)
parser.add_argument(
    "--end_date",
    type=str,
    required=True,
    help="The end date in YYYY-MM-DD format",
)

args = parser.parse_args()
start_date = from_format(args.start_date, "YYYY-MM-DD")
end_date = from_format(args.end_date, "YYYY-MM-DD")

client = MongoClient(os.getenv("MONGODB_URI"))

db = client.qam

indexes_collection = db.indexes

ibov_data = indexes_collection.find(
    {
        "date": {
            "$gte": from_format("2025-01-12", "YYYY-MM-DD"),
            "$lte": from_format("2025-01-19", "YYYY-MM-DD"),
        },
        "ticker": "IBOV",
    }
)

ibov_df = pd.json_normalize(ibov_data)

ibov_df["cumulative_return"] = (1 + ibov_df["return"]).groupby(
    ibov_df["ticker"]
).cumprod() - 1
threshold = ibov_df["cumulative_return"].to_list()[-1]

stocks_collection = db.stocks

stocks_data = stocks_collection.find(
    {
        "date": {
            "$gte": from_format("2025-01-12", "YYYY-MM-DD"),
            "$lte": from_format("2025-01-19", "YYYY-MM-DD"),
        }
    }
)

stocks_df = pd.json_normalize(stocks_data)
stocks_df["cumulative_return"] = (1 + stocks_df["return"]).groupby(
    stocks_df["ticker"]
).cumprod() - 1
stocks_df = stocks_df[stocks_df["date"] == stocks_df["date"].max()]
stocks_df = stocks_df[stocks_df["cumulative_return"] > threshold].sort_values(
    by="cumulative_return", ascending=False
)

stocks_df = stocks_df.head(40)

stocks_df["portfolio_pct"] = 1 / len(stocks_df)

stocks_df = stocks_df[["ticker", "portfolio_pct"]]
data = stocks_df.to_dict(orient="records")

db = client.qam
collection = db.portfolio

collection.delete_many({})
collection.insert_many(data)
