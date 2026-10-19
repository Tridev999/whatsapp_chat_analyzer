
# -------------------------------
# SENTIMENT ANALYSIS SECTION
# -------------------------------
from turtle import st
import streamlit as st
import pandas as pd
import time
from transformers import pipeline
from sentiment import analyze_sentiment
st.header("AI Sentiment Analysis")

if st.button("Analyze Chat Sentiment"):
    
    with st.spinner("Analyzing WhatsApp messages..."):
        result_df = analyze_sentiment(df, selected_user)

    # Store results so they survive Streamlit reruns
    st.session_state["sentiment_results"] = result_df

# Display saved results
if "sentiment_results" in st.session_state:

    result_df = st.session_state["sentiment_results"]

    analyzed_df = result_df[
        result_df["sentiment"] != "Not analyzed"
    ]

    st.subheader("Sentiment Distribution")

    if not analyzed_df.empty:
        counts = analyzed_df["sentiment"].value_counts()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Positive",
            int(counts.get("positive", 0))
        )
        col2.metric(
            "Negative",
            int(counts.get("negative", 0))
        )
        col3.metric(
            "Neutral",
            int(counts.get("neutral", 0))
        )

        st.bar_chart(counts)

    st.subheader("Message Sentiment Predictions")
    st.dataframe(
        result_df[
            ["date", "user", "message", "sentiment", "confidence"]
        ],
        use_container_width=True
    )

    st.download_button(
        "Download Sentiment Results",
        data=result_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="sentiment_results.csv",
        mime="text/csv"
    )
