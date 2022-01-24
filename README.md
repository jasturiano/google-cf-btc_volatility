# BTC Volatility using Python and Google Cloud Functions

The purpose of this exercise is to get the volatility of the Bitcoin currenct by a given dataset.

In order to be scalable and can be deployed over enviroments a Cloud Function design is implemented as follows:

![Payload to BQ](https://github.com/jasturiano/google-cf-btc_volatility/blob/main/images/json_to_gcp.png)


**Steps:**

1. The payload file is automatically downloaded each time the Cloud Function is called (in this case is called every time a new file is placed in the configured GCS bucket)

2. Once we have the json file in GCS, the Cloud Function is going to read the file and upload the data into a BQ table, then is going to make the calculations to get the volatility (Standard Deviation) and Sharped Ratio and insert that new data into another BQ table.


Using this approach we can scalate the architecture easily since we are using a serverless solution and we can promote this code over different environments using CICD (Jenkins, GitHub actions...) easily.

**Variables used in the code**

* URL: http://cf-code-challenge-40ziu6ep60m9.s3-website.eu-central-1.amazonaws.com/ohlcv-btc-usd-history-6min-2020.json
* BUCKET: The GCS bucket where the file will be downloaded
* FILE_NAME: ohlcv-btc-usd history-6min-2020.json
* VOLATILITY_TBL: BigQuery Table that will store mathematical calculations from the initial payload 
* PROJECT: GCP Project ID
