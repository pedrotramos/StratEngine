import argparse
import httpx
import os
import pandas as pd
import yfinance as yf
from pymongo import MongoClient
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument(
    "--incremental_load",
    type=lambda x: x.lower() == "true",
    default=True,
    help="A boolean flag to indicate if the load should be incremental. Default is True.",
)
args = parser.parse_args()

response = httpx.get(
    url="https://brapi.dev/api/quote/list",
    params={"type": "stock", "token": os.getenv("BRAPI_TOKEN")},
)

br_stocks_df = pd.json_normalize(response.json()["stocks"])
br_stocks_df = br_stocks_df[~br_stocks_df["stock"].str.endswith("F")]

df = yf.download(
    tickers=[f"{t}.SA" for t in br_stocks_df["stock"].to_list()],
    start="2024-01-01",
    interval="1d",
)

df = (
    df.stack(0, future_stack=True)
    .reset_index()
    .rename(columns={"^BVSP": "IBOV", "^GSPC": "SP500"})
    .melt(id_vars=["Date", "Price"], var_name="Ticker", value_name="Value")
    .pivot(index=["Date", "Ticker"], columns=["Price"], values=["Value"])
    .stack(0, future_stack=True)
    .reset_index()
    .drop(columns=["level_2"])
)

df["Return"] = df.groupby("Ticker", group_keys=False)["Close"].apply(
    lambda x: x.pct_change()
)

df = df.rename(columns={c: c.lower() for c in df.columns})

data = df.to_dict(orient="records")

client = MongoClient(os.getenv("MONGODB_URI"))

db = client.qam
collection = db.stocks

if not args.incremental_load:
    collection.delete_many({})
    collection.insert_many(data)
else:
    for record in tqdm(data, desc="Inserting incremental records", unit="record"):
        collection.update_one(
            {"date": record["date"], "ticker": record["ticker"]},
            {"$set": record},
            upsert=True,
        )
