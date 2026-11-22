# Retail customer analytics (UCI Online Retail II)

Customer and revenue analysis of a UK online retailer, using the public UCI *Online Retail II* dataset (2 years of transactions, Dec 2009 to Dec 2011). Python (pandas), run on Google Colab. Script: `analysis.py`.

## What it does
- Cleans the data (removes cancellations and non-positive quantities/prices) and measures seasonality, geography and order value.
- - Segments customers with RFM (recency, frequency, monetary) scoring.
  - - Measures cohort retention, revenue concentration (Pareto) and frequent product pairs.
   
    - ## Key findings
    - | Metric | Result |
    - |---|---|
    - | Rows | 1,067,371 raw, 1,041,670 after cleaning; 5,878 customers with an ID (77% of rows) |
    - | Seasonality | Oct to Dec is 38.3% of revenue |
    - | Geography | UK is 85.2% of revenue; then Ireland (3.2%), Netherlands (2.6%), Germany (2.1%), France (1.7%) |
    - | Order value | Mean GBP 479.95, median GBP 305.25 per invoice (large baskets: many buyers are trade customers) |
    - | Repeat rate | 72.4% of customers ordered more than once |
    - | Concentration | The top 20% of customers generate 77.2% of customer revenue |
    - | RFM | "Champions" are 1,482 customers (25%) and about 70% of revenue; 824 "at risk" customers (about 369 days since last order) still represent about GBP 1.6M of past revenue |
    - | Retention | About 20% of a cohort buys again in months 1 to 3; 13.5% in month 6 |
   
    - ## What a small online brand can take from this
    - 1. Revenue is concentrated: protect and reward the best customers before chasing new ones.
      2. 2. The at-risk group is large and valuable: a win-back campaign has a clear target list.
         3. 3. Plan stock and marketing for Q4, which carries over a third of annual revenue.
            4. 4. Frequent product pairs suggest bundles.
              
               5. ## Caveats
               6. - This is a trade-heavy gift-ware business, so order values are far above a consumer fashion shop; do not read the numbers as a benchmark for consumer clothing.
                  - - Some top "products" (for example "Manual" and "POSTAGE") are non-product lines and should be excluded; this is a known issue to fix.
                    - - Descriptive analysis only: no causal claims, no forecasting yet.
                     
                      - ## Run it
                      - Open a Colab notebook and run: `!pip -q install tabulate openpyxl && wget -q https://raw.githubusercontent.com/abirhossain-dev/retail-customer-analytics/main/analysis.py && python analysis.py`
                     
                      - Next steps: exclude non-product lines, add charts, add a CLV estimate and a simple demand forecast.
                     
                      - Author: MD Abir Hossain, MSc IT with Data Analytics (University of the West of Scotland).
                      - 
