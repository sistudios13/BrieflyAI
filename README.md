# **BrieflyAI** 📰⚡  
🚀 **Summarize the latest news in seconds using AI!**  

BrieflyAI fetches top headlines, scrapes full articles, and generates concise AI-powered summaries. Built with **FastAPI and HTMX**, it delivers news updates quickly and efficiently.  

## **🌟 Features**  
- ✅ **Fetches top headlines** from NewsAPI  
- ✅ **Scrapes full news articles** for complete context  
- ✅ **Summarizes articles** using `facebook/bart-large-cnn`  
- ✅ **FastAPI backend** for high-speed requests  
- ✅ **HTMX integration** for instant updates  

## **📦 Installation**  
### 1️⃣ Clone the repository  
```sh
git clone https://github.com/yourusername/brieflyai.git
cd brieflyai
```
### 2️⃣ Install dependencies
```sh
pip install -r requirements.txt
```
### 3️⃣ Set up your .env file
Create a .env file and add your API key:
```sh
API_KEY=your_newsapi_key_here
```
### 5️⃣ Open the frontends
Navigate to ```http://127.0.0.1:8000``` and start summarizing!

## 🛠 Technologies Used  

- **FastAPI** - Handles API requests  
- **HTMX** - Enables dynamic UI updates  
- **NewsAPI** - Provides real-time news  
- **Newspaper3k** - Scrapes full news articles  
- **Hugging Face Transformers** - Summarizes content  

## ⚠️ Disclaimer  
**Summaries are AI-generated and may not always be accurate. Please verify with original sources.**  
