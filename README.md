# 🤖 AutoTweet AI — Smart Twitter News Bot

AutoTweet AI is a fully automated **AI-powered Twitter bot** built with **Python**, **Gemini AI**, and **RSS feeds**.  
It automatically fetches the latest news from configurable sources, summarizes them into short, human-like tweets, and posts them to Twitter — optionally including an image from the article.

---

## 🚀 Features

✅ **AI-Powered Tweets** — Uses Google Gemini to generate natural, engaging summaries.  
✅ **RSS Integration** — Pulls the latest articles from any RSS feeds you define.  
✅ **Keyword Filtering** — Only posts news relevant to your chosen topics.  
✅ **Dynamic Scheduling** — Post 2–5 times a day, automatically spaced throughout the day.  
✅ **Image Extraction** — Scrapes each article for an image to include in your tweet.  
✅ **Customizable Prompt** — You can modify the AI prompt in `config.json` to change tone or style.  
✅ **Test Mode** — Preview tweets locally before posting to Twitter.

---

## 🧩 How It Works

1. The bot reads the latest articles from RSS sources you define.
2. It filters articles based on keywords from `keywords.txt`.
3. For each relevant article:
   - It generates a tweet summary using **Gemini AI**.
   - It extracts an image from the article (if available).
   - It posts the tweet via the Twitter API.
4. The process repeats automatically throughout the day, based on your schedule.

---

## ⚙️ Installation

### 1️⃣ Clone this repository
```bash
git clone https://github.com/yourusername/autotweet-ai.git
cd autotweet-ai
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables

Create a `.env` file in the project root and add your credentials:

```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
GEMINI_API_KEY=your_gemini_api_key
```

### 4️⃣ Configure your bot

Edit `config.json` to customize the AI prompt and posting schedule:

```json
{
  "custom_prompt": "You are a journalist. Write a short tweet (under 250 characters) summarizing the article in a human, engaging tone. Include 2–3 relevant hashtags.",
  "posts_per_day": 3
}
```

Add your topic keywords in `keywords.txt`:

```
football
AI
technology
startups
```

---

## 🧠 Usage

### ▶️ Run in test mode (no tweets posted)

```bash
python app.py test
```

### 🚀 Run live mode (posts tweets automatically)

```bash
python app.py
```

---

## 📅 Scheduling

* The bot automatically schedules tweets evenly across the day based on `posts_per_day`.
* For example:

  * `2` posts/day → 09:00 and 21:00
  * `3` posts/day → 09:00, 15:00, 21:00
  * `4` posts/day → 09:00, 13:00, 17:00, 21:00

---

## 🖼️ Image Extraction

If available, the bot includes an article image in the tweet by:

1. Checking RSS metadata (`media_content`, `media_thumbnail`)
2. Falling back to scraping the page’s `<meta property="og:image">` tag

All images are saved in the `/images` folder.

---

## 💡 Example Output

🧪 **Test Mode Preview**

```
AI-driven innovation continues in European football clubs as new analytics systems reshape coaching strategies. #AI #Football #Innovation
🖼️ Image saved locally: images/image_2025-11-10_09-00-00.jpg
```

✅ **Live Tweet Example**

> *"OpenAI announces major Gemini update, integrating advanced multimodal capabilities. #AI #TechNews"*

---

## 🛠️ File Structure

```
project/
│
├── app.py             # Main bot script
├── config.json        # User configuration (prompt, schedule)
├── keywords.txt       # Keywords for filtering relevant news
├── .env               # API keys and tokens
├── requirements.txt   # Python dependencies
└── images/            # Downloaded article images
```

---

## 🧰 Technologies Used

* **Python 3.9+**
* **Tweepy** – Twitter API
* **Google Gemini AI** – Tweet text generation
* **Feedparser** – RSS feed parsing
* **BeautifulSoup** – Web scraping
* **Schedule** – Automated post scheduling
* **dotenv** – Secure environment variable management

---

## ⚠️ Important Notes

* Keep `TEST_MODE = True` while testing to prevent real tweets.
* Gemini occasionally generates empty or partial responses — these are skipped automatically.
* To post live, set:

  ```python
  TEST_MODE = False
  ```

---

## 🧑‍💻 Contributing

Pull requests are welcome!
If you’d like to add new features (e.g. multiple topics, Telegram/Discord notifications, or a web dashboard), feel free to fork and submit a PR.

---

## 🌐 Connect With Me

If you liked this project, give it a ⭐ on GitHub and share it on LinkedIn!

📩 **GitHub:** [Muunsparkss](https://github.com/Muunsparkss)
💼 **LinkedIn:** [Mehmet Sedat YILDIZ](https://www.linkedin.com/in/mehmet-sedat-y%C4%B1ld%C4%B1z/)

---

### 🏁 Ready to Automate Your Twitter Feed?

> “Your Twitter never sleeps — let AI do the talking.” 🚀

````