import requests
from dotenv import load_dotenv
import os
from transformers import pipeline
from newspaper import Article
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import time

app = FastAPI()
app.mount("/home", StaticFiles(directory="frontend"), name="frontend")
load_dotenv()

cached_news = None
last_updated = 0
CACHE_DURATION = 600 #10 mins 

API_KEY = os.getenv("API_KEY")
url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + API_KEY

@app.get("/api", response_class=HTMLResponse)
def home():
    return '<p>Welcome to BrieflyAI!</p>' 

def get_news():
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch news:", response.status_code)
        return []
    data = response.json()
    articles = data.get('articles')
    news_list = []
    for item in articles:
        if item['url'] is not None:
            news_list.append(
                {
                "url" : item['url']
                }
            )

    return news_list


def summarize_news(article, length):
    if article == "":
        return None  # Return None to handle empty input
    summarizer = pipeline(task='summarization', model='facebook/bart-large-cnn')
    summary = summarizer(article, max_length=length, min_length=80, do_sample=True, temperature=0.7)
    return summary if summary else None



def scrape_news(a):
    article = Article(a['url'])
    try:
        article.download()
        article.parse()
        summary = summarize_news(article.text, 100)
        return summary
    except Exception as e:
        print(f"Failed to scrape {a['url']}: {str(e)}")
        return None


def summarize_again(count):
    # Summarize all the summaries
    news = get_news()[:count]
    summary_list = []
    for article in news:
        summary = scrape_news(article)
        if summary is not None:
            summary_list.append(summary[0]['summary_text'])

    if not summary_list:
        return "<p>No Valid News</p>"

    summaries = ' '.join(summary_list)
    output = summarize_news(summaries, 160)
    return output


@app.get('/api/news', response_class=HTMLResponse)
def see_news():
    # output = summarize_again(6)
    # if isinstance(output, dict) and "error" in output:
    #     return output

    # summarized_news = output[0]['summary_text'] if output else "No summary available"
    # return f"<p>{str(summarized_news)}</p>"

    global cached_news, last_updated

    if cached_news and (time.time() - last_updated < CACHE_DURATION):
        return cached_news

    try:
        output = summarize_again(6)
        summarized_news = output[0]['summary_text']
        cached_news = summarized_news  # Store in cache
        last_updated = time.time()  # Update timestamp
        return f"<p>{summarized_news}</p>"
    except Exception as e:
        return f"<p>Error: {e}</p>"
