import feedparser
from newspaper import Article
from models import insert_quote

# Leader info with fallback quotes
leaders = {
    "Elon Musk": {
        "query": "Elon Musk AGI",
        "fallback_quote": "If you define AGI as smarter than the smartest human, I think it's probably next year, within two years.",
        "image": "https://tse2.mm.bing.net/th?id=OIF.%2Fz3Lhy3hjoCCcM%2BdpdaUdg&pid=Api",
        "source": "https://www.reuters.com/technology/teslas-musk-predicts-ai-will-be-smarter-than-smartest-human-next-year-2024-04-08/"
    },
    "Sam Altman": {
        "query": "Sam Altman AGI",
        "fallback_quote": "We know how to build AGI. It could be developed this presidential term, and safety is critical.",
        "image": "https://commons.wikimedia.org/wiki/File:Sam_Altman_CropEdit_James_Tamim.jpg",
        "source": "https://blog.samaltman.com/reflections"
    },
    "Geoffrey Hinton": {
        "query": "Geoffrey Hinton AI",
        "fallback_quote": "There's a 10–20% chance AI could surpass humans and lead to extinction. We need safety structures urgently.",
        "image": "https://tse2.mm.bing.net/th?id=OIF.%2Fz3Lhy3hjoCCcM%2BdpdaUdg&pid=Api",
        "source": "https://timesofindia.indiatimes.com/technology/tech-news/godfather-of-ai-geoffrey-hinton-agrees-with-dangerous-label-that-elon-musk-said-for-chatgpt-maker-openai-warns-/articleshow/120722596.cms"
    },
    "Sundar Pichai": {
        "query": "Sundar Pichai AI",
        "fallback_quote": "The AI progress path is steeper now; real AGI needs deeper breakthroughs.",
        "image": "https://tse1.mm.bing.net/th?id=OIF.AQNm%2BnhDO1NwziEWuYHj%2Fg&pid=Api",
        "source": "https://www.linkedin.com/posts/srinipagidyala_google-ceo-sundar-pichai-says-the-progress-activity-7270283730651344896-6qh6"
    },
    "Demis Hassabis": {
        "query": "Demis Hassabis DeepMind",
        "fallback_quote": "AGI could be here in 5–10 years, but society is not ready for its implications.",
        "image": "https://tse2.mm.bing.net/th?id=OIF.4sZfCwZchGEoqWs3u%2BwlBA&pid=Api",
        "source": "https://www.windowscentral.com/software-apps/google-deepmind-ceo-says-agi-is-coming-society-not-ready"
    },
    "Satya Nadella": {
        "query": "Satya Nadella AI",
        "fallback_quote": "AGI claims today are benchmark hacks. True AGI should boost economies significantly.",
        "image": "https://tse2.mm.bing.net/th?id=OIP.u57ra7uGXXGGE0wgKTdKCwHaEK&pid=Api",
        "source": "https://www.geekwire.com/2025/microsoft-ceo-satya-nadella-has-a-formula-to-gauge-the-long-term-success-of-ai-investments/"
    }
}

def fetch_latest_entry(query):
    feed_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)
    return feed.entries[0] if feed.entries else None

def extract_quote(article_url, fallback_text=None):
    try:
        article = Article(article_url)
        article.download()
        article.parse()
        article.nlp()
        return article.summary or article.text[:300]
    except Exception as e:
        print(f"⚠️ Failed to parse article: {e}")
        return fallback_text[:300] if fallback_text else None

def run_scraper():
    for name, meta in leaders.items():
        print(f"🔍 Searching for {name}...")
        entry = fetch_latest_entry(meta['query'])
        url = entry.link if entry else meta['source']
        summary = entry.get('summary', '') if entry else ''
        quote = extract_quote(url, fallback_text=summary)

        if not quote:
            quote = meta['fallback_quote']
            print(f"🔁 Using fallback for {name}")

        insert_quote(
            name=name,
            title="AI Leader",
            quote=quote,
            image=meta['image'],
            source=url
        )
        print(f"✅ Saved quote for {name}")

if __name__ == "__main__":
    run_scraper()
