import requests
import pandas as pd
import time

TAGS = [
    "python",
    "machine-learning",
    "deep-learning",
    "data-science",
    "artificial-intelligence",
    "web-development"
]

BASE_URL = "https://api.stackexchange.com/2.3/questions"
all_records = []

for tag in TAGS:
    print(f"Fetching tag: {tag}")
    
    for page in range(1, 6):
        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": tag,
            "site": "stackoverflow",
            "pagesize": 100,
            "page": page,
            "filter": "withbody"
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        for item in data.get("items", []):
            if "owner" not in item:
                continue

            record = {
                "question_id": item.get("question_id"),
                "question_title": item.get("title"),
                "question_body": item.get("body"),
                "user_id": item["owner"].get("user_id"),
                "display_name": item["owner"].get("display_name"),
                "tags": ",".join(item.get("tags", [])),
                "upvotes": item.get("score")
            }

            all_records.append(record)

        time.sleep(1)

df = pd.DataFrame(all_records)
df.to_csv("data/raw/stack_overflow_raw.csv", index=False)

print("Total records:", len(df))