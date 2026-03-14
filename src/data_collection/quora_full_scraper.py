import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# -------- CONFIG --------
TOPIC_URLS = [
    "https://www.quora.com/topic/Python-programming",
    "https://www.quora.com/topic/Machine-Learning",
    "https://www.quora.com/topic/Artificial-Intelligence",
    "https://www.quora.com/topic/Data-Science",
    "https://www.quora.com/topic/Web-Development"
]

MAX_SCROLL = 5
MAX_QUESTIONS_PER_TOPIC = 8
OUTPUT_FILE = "data/raw/quora_structured_data.csv"
# ------------------------

print("Launching browser...")
driver = webdriver.Chrome()
driver.get("https://www.quora.com/")

print("Login manually within 40 seconds...")
time.sleep(40)

all_data = []
seen_texts = set()

for topic_url in TOPIC_URLS:

    print(f"\nOpening topic: {topic_url}")
    driver.get(topic_url)
    time.sleep(random.uniform(4, 7))

    # Scroll topic page
    for _ in range(MAX_SCROLL):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(random.uniform(3, 6))

    print("Collecting question links...")

    question_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/What')]")
    question_links = list(set([q.get_attribute("href") for q in question_elements]))

    print(f"Found {len(question_links)} question links.")

    for q_url in question_links[:MAX_QUESTIONS_PER_TOPIC]:
        try:
            print("Opening:", q_url)
            driver.get(q_url)
            time.sleep(random.uniform(4, 8))

            # Scroll to load answers
            for _ in range(3):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(random.uniform(3, 6))

            # Extract all divs
            all_divs = driver.find_elements(By.TAG_NAME, "div")

            for div in all_divs:
                text = div.text.strip()

                # Filter meaningful answer-sized text
                if len(text) > 300 and "Upvote" not in text and "Comment" not in text:

                    if text not in seen_texts:
                        seen_texts.add(text)

                        all_data.append({
                            "topic_url": topic_url,
                            "question_url": q_url,
                            "answer_text": text
                        })

        except Exception as e:
            print("Error:", e)
            continue

print("\nSaving data...")

df = pd.DataFrame(all_data)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved {len(df)} total records.")
driver.quit()