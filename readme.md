# WhatsApp Chat Analyzer 📊

Ever wondered what your WhatsApp conversations can tell you about your messaging habits? This project explores that idea by turning exported WhatsApp chats into useful insights through data analysis and machine learning.

I built this project using Python and Streamlit to make chat analysis simple and interactive. Users can explore messaging activity, identify communication patterns, visualize sentiment, and better understand the trends hidden in their conversations.

## What can it do?
- **Chat Statistics:** Get an overview of conversations, message counts, and messaging activity.
- **User Analysis:** Explore individual participation and see who contributes most to a group chat.
- **Activity Trends:** Understand when people are most active and how messaging patterns change over time.
- **Sentiment Analysis:** Use a pretrained transformer-based model to classify messages as positive, negative, or neutral.
- **Hinglish Support:** Analyze supported messages written in English, Hindi, and Romanized Hinglish.
- **Interactive Visualizations:** Explore chat data through charts and an easy-to-use dashboard.

## Tools and Technologies

- **Python** – Core programming language
- **Pandas** – Data cleaning and analysis
- **Streamlit** – Interactive web dashboard
- **Hugging Face Transformers** – Pretrained NLP model for sentiment classification
- **MuRIL-based sentiment model** – Sentiment analysis for supported multilingual messages
- **Matplotlib / Seaborn** – Visualizations, if used in the project

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

### 4. Analyze your chat

Export a WhatsApp conversation as a `.txt` file, upload it to the application, and explore the available statistics and sentiment insights.

The first sentiment-analysis run may take some time because the pretrained model needs to download.

## Why I Built This

I wanted to work on a practical project that combines data analysis with machine learning instead of just learning these concepts separately. Working on this analyzer helped me gain hands-on experience with data preprocessing, exploratory data analysis, NLP, pretrained transformer models, and interactive dashboard development.

It also helped me understand that real-world text data can be messy and that machine learning predictions need to be interpreted carefully.

## Future Improvements

- Add an AI chatbot to answer questions about chat statistics.
- Evaluate sentiment predictions using precision, recall, F1-score, and a confusion matrix.
- Add more interactive visualizations and communication trends.
- Try to increase the sentiment analysis with more accuracy with english + hinglish
## About Me

I'm a Computer Science student interested in Data Science, Machine Learning, and building practical applications that solve real-world problems.

---

*Built with Python, curiosity, and a desire to turn raw data into meaningful insights.*