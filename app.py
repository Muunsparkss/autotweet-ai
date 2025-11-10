import os
import sys
import requests
import tweepy
import schedule
import time
import re
import random
import json
import feedparser
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# --- Load environment variables ---
load_dotenv()
TEST_MODE = True  # Set to False to post live tweets

# --- Twitter Authentication ---
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
twitter_api = tweepy.API(auth)

# --- RSS Sources (user can modify freely) ---
RSS_SOURCES = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.reutersagency.com/feed/?best-topics=technology",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
]

# --- Gemini Setup ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Load Config (Prompt + Schedule) ---
def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load config.json: {e}")
        return {
            "custom_prompt": "Write a short, engaging tweet (under 250 characters) based on the article title and summary.",
            "posts_per_day": 3
        }

CONFIG = load_config()

# --- Load Keywords ---
def load_keywords(filepath="keywords.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print("⚠️ keywords.txt not found. All news will be considered relevant.")
        return []

KEYWORDS = load_keywords()

# --- Check if news matches keywords ---
def is_relevant_article(title):
    if not KEYWORDS:
        return True
    title_lower = title.lower()
    return any(word in title_lower for word in KEYWORDS)

# --- Fetch latest relevant news from RSS sources ---
def fetch_latest_article():
    random.shuffle(RSS_SOURCES)
    for rss_url in RSS_SOURCES:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue
        for entry in feed.entries:
            if is_relevant_article(entry.title):
                return entry
    print("⚠️ No relevant news found in any source.")
    return None

# --- Generate tweet text using Gemini ---
def generate_tweet(article):
    base_prompt = CONFIG.get("custom_prompt", "")
    prompt = f"""
    {base_prompt}

    Title: {article['title']}
    Summary: {article['summary']}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip() if response.text else None

# --- Extract or download article image ---
def fetch_article_image(article):
    try:
        os.makedirs("images", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"images/image_{timestamp}.jpg"

        # Try RSS images first
        img_url = None
        if "media_content" in article:
            img_url = article["media_content"][0]["url"]
        elif "media_thumbnail" in article:
            img_url = article["media_thumbnail"][0]["url"]
        elif "links" in article:
            for l in article["links"]:
                if "image" in l.get("type", ""):
                    img_url = l["href"]
                    break

        # Fallback: scrape article for og:image
        if not img_url:
            headers = {"User-Agent": "Mozilla/5.0"}
            page = requests.get(article["link"], headers=headers, timeout=10).text
            soup = BeautifulSoup(page, "html.parser")

            og = soup.find("meta", property="og:image")
            if og and og.get("content"):
                img_url = og["content"]
            else:
                for img in soup.find_all("img"):
                    src = img.get("src")
                    if src and src.startswith("http") and "logo" not in src and "icon" not in src:
                        img_url = src
                        break

        if not img_url:
            print("⚠️ No valid image found for this article.")
            return None

        img_data = requests.get(img_url, timeout=10).content
        with open(filename, "wb") as f:
            f.write(img_data)

        print(f"🖼️ Downloaded image: {filename}")
        return filename

    except Exception as e:
        print(f"⚠️ Image extraction failed: {e}")
        return None

# --- Post tweet (with optional image) ---
def post_tweet():
    article = fetch_latest_article()
    if not article:
        print("⚠️ No relevant news found. Retrying with a new source...")
        article = fetch_latest_article()
        if not article:
            print("🚫 Still no article found after retry.")
            return

    tweet_text = generate_tweet({
        "title": article.title,
        "summary": article.get("summary", ""),
        "link": article.link
    })

    image_path = fetch_article_image(article)

    if not tweet_text:
        print("🚫 Gemini returned an empty tweet.")
        return

    if TEST_MODE:
        print("\n🧪 TEST MODE — Tweet Preview:")
        print(tweet_text)
        if image_path:
            print(f"🖼️ Image saved locally: {image_path}")
    else:
        if image_path:
            twitter_api.update_status_with_media(status=tweet_text, filename=image_path)
        else:
            twitter_api.update_status(status=tweet_text)
        print("✅ Tweet posted successfully!")

# --- Dynamic scheduling based on config ---
def setup_schedule():
    posts_per_day = CONFIG.get("posts_per_day", 3)
    if posts_per_day <= 0:
        print("⚠️ Invalid posts_per_day in config.json. Defaulting to 3.")
        posts_per_day = 3

    interval = 24 / posts_per_day
    base_hour = 9  # start at 9:00 AM
    for i in range(posts_per_day):
        post_time = f"{int((base_hour + i * interval) % 24):02d}:00"
        schedule.every().day.at(post_time).do(post_tweet)
        print(f"🕒 Scheduled post at {post_time}")

setup_schedule()

print("🤖 Generic Twitter Bot started...")

if __name__ == "__main__":
    if "test" in sys.argv:
        print("🔍 Running immediate test post...")
        post_tweet()
    else:
        print("🤖 Scheduler started...")
        while True:
            schedule.run_pending()
            time.sleep(60)
