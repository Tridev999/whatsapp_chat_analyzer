
import pandas as pd
import streamlit as st
from transformers import pipeline
# Pretrained sentiment model
MODEL_NAME = "airzipm/sentiment-analysis-muril-v2"
@st.cache_resource
def load_model():
    """Load pretrained model once and cache it."""
    model = pipeline(
        "text-classification",
        model=MODEL_NAME,
        device=-1
    )
    return model


def analyze_sentiment(df,selected_user):
    """
    Input: WhatsApp DataFrame with 'user' and 'message'.
    Output: DataFrame with sentiment and confidence columns.
    """
    if selected_user != 'OverAll':
        df = df[df["user"]==selected_user]
    df = df.copy().reset_index(drop=True)
    # Default values for messages we don't analyze
    df["sentiment"] = "Not analyzed"
    df["confidence"] = float("nan")

    # Exclude system notifications and media messages
    messages = df["message"].fillna("").astype(str)

    valid_mask = (
        df["user"].fillna("").ne("group_notification")
        & messages.str.strip().ne("")
        & ~messages.str.contains(
            r"<Media omitted>|image omitted|video omitted|"
            r"audio omitted|sticker omitted|"
            r"This message was deleted",
            case=False,
            regex=True,
            na=False
        )
    )

    valid_indices = df.index[valid_mask].tolist()

    if not valid_indices:
        return df

    model = load_model()

    # Process in batches to reduce memory usage
    batch_size = 16

    for start in range(0, len(valid_indices), batch_size):
        batch_indices = valid_indices[start:start + batch_size]

        batch_messages = (
            messages.loc[batch_indices]
            .str.strip()
            .tolist()
        )

        predictions = model(
            batch_messages,
            truncation=True,
            max_length=512,
            batch_size=batch_size
        )

        for idx, prediction in zip(batch_indices, predictions):
            df.at[idx, "sentiment"] = (
                prediction["label"].lower()
            )
            df.at[idx, "confidence"] = round(
                prediction["score"] * 100, 2
            )

    return df
