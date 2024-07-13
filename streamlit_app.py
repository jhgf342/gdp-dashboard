import streamlit as st
import time
import requests
import json
from datetime import datetime, timedelta
import speech_recognition as sr

# Function to fetch news from Google News
def fetch_news(api_key, query, num_articles):
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=relevancy&pageSize={num_articles}&from={(datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')}&to={datetime.now().strftime('%Y-%m-%d')}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    
    articles = response.json().get('articles', [])
    relevant_articles = [article for article in articles[:num_articles] if query.lower() in article['title'].lower() or query.lower() in article['description'].lower()]
    return relevant_articles

# Function to recognize speech using the microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please speak the news topic...")
        audio = recognizer.listen(source)
        try:
            topic = recognizer.recognize_google(audio)
            st.write(f"You said: {topic}")
            return topic
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand your speech.")
        except sr.RequestError:
            st.error("Could not request results; check your network connection.")
        return None

# Streamlit app
def main():
    st.set_page_config(page_title="InfoLive - AI News Anchor", layout="wide")
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: white;
            color: black;
            margin-left: 30px;
            font-size: 1em;
        }
        header {
            font-family: 'Times New Roman', cursive;
            font-size: 5em;
            padding: 10px 20px;
            height: 120px;
            text-align: left;
            background-color: rgba(255, 165, 56, 1);
            color: orangered;
            position: sticky;
            top: 0;
            width: 100%;
        }
        p{
                font-size: 1.5em;
        }
        h1 {
            font-family: 'Bebas Neue', cursive;
            font-size: 3em;
            color: orangered;
        }
        .container {
            width: 60%;
            margin: auto;
            padding: 10px;
        }
        .news-article {
            margin-bottom: 30px;
        }
        footer {
            background-color: rgba(255, 165, 56, 0.8);
            color: orangered;
            padding: 10px 20px;
            text-align: center;
            position: fixed;
            bottom: 0;
            width: 100%;}
        hr{
                height: 20px;
                background-color: rgb(255, 165, 56)
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<header>AI News Anchor - InfoLive</header>', unsafe_allow_html=True)
    st.title("InfoLive - AI News Anchor")
    st.markdown("<p>Meet 'InfoLive', your digital news companion! With lightning-fast updates and insightful analysis, InfoLive delivers the latest headlines straight to your screen. Stay informed, stay connected, and navigate the complexities of the modern world with ease, thanks to InfoLive's unparalleled news delivery capabilities!</p>", unsafe_allow_html=True)

    st.sidebar.header("Demonstration")
    api_key_news = 'ad00a306c6a4404a9fe801b405df2c5d'
    num_articles = st.sidebar.slider("Number of Articles", 0, 4, 4)

    if st.sidebar.button("Get News"):
        topic = recognize_speech()
        if api_key_news and topic:
            news_articles = fetch_news(api_key_news, topic, num_articles)
            if news_articles:
                script = " ".join([f"{article['title']}. {article['description']}" for article in news_articles])

                st.header("Latest News")
                for i, article in enumerate(news_articles):
                    st.markdown(f"""
                        <div class="news-article">
                            <h2>{i+1}. {article['title']}</h2>
                            <p>{article['description']}</p>
                            <a href="{article['url']}" target="_blank">Read more</a>
                        </div>
                    """, unsafe_allow_html=True)

                # Sample video display
                st.header("Generated News Video")
                if "sports" in topic.lower():
                    st.video('1720835456951.mp4')
                elif "tech" in topic.lower() or "technology" in topic.lower():
                    st.video('1720835881769.mp4')
                elif "politics" in topic.lower():
                    st.video("1720835980469.mp4")
            else:
                st.error("No relevant articles found.")
        else:
            st.error("Please provide all required inputs.")


