import requests
from dotenv import load_dotenv
import os
from transformers import pipeline


load_dotenv()


API_KEY = os.getenv("API_KEY")
url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + API_KEY

def get_news():
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles')
    news_list = []
    for item in articles:
        news_list.append(
            {
            "title" : item['title'],
            "content" : item['content']
            }
        )

    return news_list

news = get_news()[0:3]
sentence = [i['content'] for i in news]

sentences = ' '.join(sentence[:2])

print(sentences)
summarizer = pipeline(task='summarization')

summary = summarizer(sentences, max_length=100, min_length=20, do_sample=False)
print(summary[0]["summary_text"])