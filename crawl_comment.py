import pandas as pd
from apify_client import ApifyClient


df = pd.read_csv('bosch_review_link.csv')
array = df.values.tolist()  ## Chuyen df thanh mang 2 chieu
post_link_array = [item[0] for item in array] ## Tao mang mot chieu chua cac post_link


client = ApifyClient("apify_api_FtqJLdhXTlNiZ4duyEnosWABlkbZmz3Im0wO") #Apify Client Token

# Prepare the Actor input
run_input = {
    "startUrls": [{"url": url, "method": "GET"} for url in post_link_array],  # Chuyển đổi từng URL thành định dạng đúng
    "resultsLimit": 100,
    "includeNestedComments": True,
    "viewOption": "RANKED_UNFILTERED"
}

# Run the Actor and wait for it to finish
run = client.actor("us5srxAYnsrkgUv2v").call(run_input=run_input)

if run:
# Fetch and print Actor results from the run's dataset (if there are any)
    print("Crawl data successfully")
    print("Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"]+ "\n")




