import feedparser
from newspaper import Article
from models import insert_quote

leaders = {
    "Elon Musk": "Elon Musk AGI",
    "Sam Altman": "Sam Altman AGI",
    "Geoffrey Hinton": "Geoffrey Hinton AI",
    "Sundar Pichai": "Sundar Pichai AI",
    "Demis Hassabis": "Demis Hassabis DeepMind",
    "Satya Nadella": "Satya Nadella AI"
}

def fetch_latest_entry(query):
    """Fetch RSS entry from Google News based on search query."""
    feed_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)
    return feed.entries[0] if feed.entries else None

def extract_quote(article_url, fallback_text=None):
    """Extract article summary using newspaper3k or fallback to summary."""
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
    """Fetch latest statements for each AI leader and store in DB."""
    for name, query in leaders.items():
        print(f"🔍 Searching for {name}...")
        entry = fetch_latest_entry(query)
        if not entry:
            print(f"⚠️ No articles found for {name}")
            continue

        url = entry.link
        summary = entry.get("summary", "")
        print(f"📰 URL: {url}")

        quote = extract_quote(url, fallback_text=summary)
        if quote:
            insert_quote(
                name=name,
                title="AI Leader",
                quote=quote,
                image=f"https://via.placeholder.com/100?text={name.replace(' ', '+')}",
                source=url
            )
            print(f"✅ Inserted quote for {name}")
        else:
            print(f"❌ Skipped {name}, no usable quote.")

if __name__ == "__main__":
    run_scraper()
