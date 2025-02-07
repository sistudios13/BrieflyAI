import requests
from dotenv import load_dotenv
import os
from transformers import pipeline
from newspaper import Article
from fastapi import FastAPI

app = FastAPI()

load_dotenv()

API_KEY = os.getenv("API_KEY")
url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + API_KEY

@app.get("/")
def home():
    return {'message' : 'Welcome to BrieflyAI!'}

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
        return None  # Return None to handle epty input
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
        return {"error": "No valid news to summarize"}

    summaries = ' '.join(summary_list)
    output = summarize_news(summaries, 160)
    return output


@app.get('/news')
def see_news():
    output = summarize_again(6)
    if isinstance(output, dict) and "error" in output:
        return output

    summarized_news = output[0]['summary_text'] if output else "No summary available"
    return {'news': str(summarized_news)}
