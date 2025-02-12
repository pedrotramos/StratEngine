# Asset Management System Design

This project is a simplified version of a system I designed for an asset management firm. The goal was to modernize their tech stack, boosting operational efficiency and enabling them to scale their investment universe.

## The problems

The company was managing three stock-focused funds, using a systematic approach to decide which assets to buy and which to short. The problem? Their entire system was just a Cron Job running a few Python and R scripts, with each step outputting CSV files. In other words, they had a completely sequential data pipeline.

This setup worked fine for analyzing stocks in the Brazilian market, but they were eyeing an expansion into markets like the US. That would increase their investment universe by at least 100x—way more than their current architecture could handle.

On top of that, they relied on a single data provider, which was a major risk. If that provider went out of business or even just went offline for a day, the firm wouldn’t be able to trade at all.
