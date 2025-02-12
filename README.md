# Asset Management System Design

This project is a simplified version of a system I designed for an asset management firm. The goal was to modernize their tech stack, boosting operational efficiency and enabling them to scale their investment universe.

### The problems

The company in question was managing 3 funds focused exclusively in stocks and the team used a systematic approach to define which assets they were going to buy and which ones they were going to short. The issue was that their system was basically a Cron Job that executed a few Python and R scripts, saving CSV files as the output of each step. This means they had a completely sequential data pipeline.

This setup was enough for them to analyze the stocks available in the brazilian stock market, but they were considering expanding to other markets such as the US. This would cause the investment universe to grow by a factor of 100x at least and their current architecture was not ready to handle the increase in volume.

Additionally, they only had a single data provider, which posed a huge risk. After all, if the data provider went out of business or simply went offline for a day, the firm was not able to trade.
