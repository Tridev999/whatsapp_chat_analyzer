from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time
import helper
import preprocesser
import sentiment
from PIL import Image
fav_image = Image.open("cloud-regular-full.png")
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon=fav_image,
    layout="wide",
)
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
    }
    .hero {
        padding: 1.2rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(128, 128, 128, 0.25);
    }
    .hero-eyebrow {
        margin: 0 0 0.4rem;
        color: #536878;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
    }
    .hero h1 {
        margin: 0;
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        letter-spacing: -0.03em;
    }
    .hero-copy {
        margin: 0.5rem 0 0;
        color: var(--text-color);
        opacity: 0.75;
        font-size: 1rem;
    }
    div[data-testid="stMetric"] {
        padding: 0.8rem 1rem;
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 8px;
        background: transparent;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Chat Analyzer")
    st.caption("A little more insight into the conversations that matter.")
    uploaded_file = st.file_uploader("Start by choosing a WhatsApp .txt export", type=["txt"])
    st.divider()
    st.caption("Your chat is analyzed in this app to create the insights below.")

title_col, link_col = st.columns([5, 1.5], vertical_alignment="center")
with title_col:
    st.markdown(
        """
        <div class="hero">
            <p class="hero-eyebrow">Your conversations, at a glance</p>
            <h1>WhatsApp Chat Analyzer</h1>
            <p class="hero-copy">See the people, moments, and words behind your chats.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with link_col:
    st.link_button(
        "Connect on LinkedIn",
        "https://www.linkedin.com/in/tridev06",
        use_container_width=True,
    )

if uploaded_file is None:
    st.caption("Upload a WhatsApp chat export from the sidebar to get started.")
    st.stop()

if Path(uploaded_file.name).suffix.lower() != ".txt":
    st.caption("Please choose a WhatsApp chat export with a .txt extension.")
    st.stop()

try:
    data = uploaded_file.getvalue().decode("utf-8-sig")
except UnicodeDecodeError:
    st.caption("This file could not be read as UTF-8 text. Please export the chat again and try once more.")
    st.stop()

df = preprocesser.preprocess(data)
if df.empty:
    st.toast("I couldn't find any messages in this file. Check that it is a WhatsApp text export.",icon="⚠️")
    time.sleep(5)
    st.stop()

user_list = sorted(user for user in df["user"].unique().tolist() if user != "group_notification")
user_list.insert(0, "OverAll")
selected_user = st.sidebar.selectbox("Whose chat would you like to explore?", user_list)
display_name = "Everyone" if selected_user == "OverAll" else selected_user

st.caption(f"Showing insights for **{display_name}** · {len(df):,} messages in this export")
with st.expander("Preview the parsed messages"):
    st.dataframe(df, use_container_width=True, hide_index=True)

nummsg, total_words, total_media, links = helper.fetch_stats(df, selected_user)
metric_cols = st.columns(4)
for column, label, value in zip(
    metric_cols,
    ("Messages", "Words", "Media shared", "Links shared"),
    (nummsg, total_words, total_media, links),
):
    with column:
        st.metric(label, f"{value:,}")

overview_tab, words_tab, activity_tab, sentiment_tab = st.tabs(
    ["People", "Words and emojis", "Activity", "Sentiment"]
)

with overview_tab:
    if selected_user == "OverAll":
        st.subheader("Who keeps the conversation going?")
        busy_users, user_percentages = helper.most_busy_users(df)
        if not busy_users.empty:
            chart_col, table_col = st.columns([1.35, 1], gap="large")
            with chart_col:
                fig, ax = plt.subplots(figsize=(8, 4))
                palette = plt.get_cmap("tab10")
                bar_colors = [palette(i % 10) for i in range(len(busy_users))]
                ax.bar(busy_users.index, busy_users.values, color=bar_colors, width=0.65)
                ax.set_ylabel("Messages")
                ax.grid(axis="y", alpha=0.2)
                ax.set_axisbelow(True)
                ax.spines[["top", "right", "left"]].set_visible(False)
                plt.xticks(rotation=25, ha="right")
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            with table_col:
                st.caption("Share of messages by participant")
                st.dataframe(user_percentages.head(5), use_container_width=True, hide_index=True)
        else:
            st.caption("There isn't enough participant data to show a comparison.")
    else:
        st.subheader(f"A closer look at {display_name}")
        st.write("Switch to **OverAll** in the sidebar to compare the most active participants.")

with words_tab:
    st.subheader("Words and reactions that stand out")
    word_col, emoji_col = st.columns(2, gap="large")

    with word_col:
        st.markdown("#### Word cloud")
        word_cloud = helper.word_cloud(df, selected_user)
        if word_cloud is None:
            st.caption("There isn't enough text here to build a word cloud.")
        else:
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.imshow(word_cloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("#### Most common words")
        common_words = helper.most_common_words(df, selected_user)
        if common_words.empty:
            st.caption("No common words to show for this selection.")
        else:
            fig, ax = plt.subplots(figsize=(6, 5))
            palette = plt.get_cmap("tab20")
            bar_colors = [palette(i % 20) for i in range(len(common_words))]
            ax.barh(
                common_words[0].iloc[::-1],
                common_words[1].iloc[::-1],
                color=bar_colors,
            )
            ax.set_xlabel("Messages")
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.grid(axis="x", alpha=0.2)
            ax.set_axisbelow(True)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    with emoji_col:
        st.markdown("#### Emoji mood")
        emoji_df = helper.emoji_helper(df, selected_user)
        if emoji_df.empty:
            st.caption("No emojis found in this chat selection yet.")
        else:
            pie_col, table_col = st.columns([1, 1.2])
            with pie_col:
                top_emojis = emoji_df.head(5)
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.pie(
                    top_emojis["Frequency"],
                    labels=top_emojis["Emoji"],
                    autopct="%1.0f%%",
                    startangle=90,
                    colors=sns.color_palette("Set2", len(top_emojis)),
                )
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)
            with table_col:
                st.dataframe(emoji_df.head(10), use_container_width=True, hide_index=True)

with activity_tab:
    st.subheader("When the chat comes alive")
    monthly_timeline = helper.monthly_timeline(df, selected_user)
    daily_timeline = helper.dialy_timeline(df, selected_user)
    timeline_col, busy_days_col = st.columns([1.4, 1], gap="large")

    with timeline_col:
        st.markdown("#### Messages over time")
        if monthly_timeline.empty:
            st.caption("There isn't enough date information to draw a timeline.")
        else:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(
                monthly_timeline["time"],
                monthly_timeline["message"],
                color="#8094a8",
                linestyle="-",
                linewidth=2,
                marker="o",
                markersize=5,
            )
            ax.scatter(
                monthly_timeline["time"],
                monthly_timeline["message"],
                c=range(len(monthly_timeline)),
                cmap="tab10",
                s=35,
                zorder=3,
            )
            ax.set_ylabel("Messages")
            ax.grid(axis="y", alpha=0.2)
            ax.spines[["top", "right", "left"]].set_visible(False)
            plt.xticks(rotation=30, ha="right")
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    with busy_days_col:
        st.markdown("#### Busiest days")
        if daily_timeline.empty:
            st.caption("There isn't enough date information to rank days.")
        else:
            busiest_days = daily_timeline.head(5).sort_values("message")
            fig, ax = plt.subplots(figsize=(6, 4))
            palette = plt.get_cmap("Set2")
            bar_colors = [palette(i % 8) for i in range(len(busiest_days))]
            ax.barh(busiest_days["daytime"], busiest_days["message"], color=bar_colors)
            ax.set_xlabel("Messages")
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.grid(axis="x", alpha=0.2)
            ax.set_axisbelow(True)
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

    month_col, weekday_col = st.columns(2, gap="large")
    busy_months = helper.most_busy_month(df, selected_user)
    busy_days = helper.most_busy_day(df, selected_user)
    with month_col:
        st.markdown("#### Most active months")
        fig, ax = plt.subplots(figsize=(6, 4))
        palette = plt.get_cmap("tab20")
        bar_colors = [palette(i % 20) for i in range(len(busy_months))]
        ax.bar(busy_months["month_name"], busy_months["message"], color=bar_colors)
        ax.set_ylabel("Messages")
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="y", alpha=0.2)
        ax.set_axisbelow(True)
        plt.xticks(rotation=25, ha="right")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with weekday_col:
        st.markdown("#### Most active weekdays")
        fig, ax = plt.subplots(figsize=(6, 4))
        palette = plt.get_cmap("Set2")
        bar_colors = [palette(i % 8) for i in range(len(busy_days))]
        ax.bar(busy_days["day_name"], busy_days["message"], color=bar_colors)
        ax.set_ylabel("Messages")
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.grid(axis="y", alpha=0.2)
        ax.set_axisbelow(True)
        plt.xticks(rotation=25, ha="right")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.markdown("#### Activity by day and hour")
    user_heatmap = helper.activity_heatmap(df, selected_user)
    if user_heatmap.empty:
        st.caption("There isn't enough activity data to build a heatmap.")
    else:
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.heatmap(user_heatmap, linewidths=0.3, ax=ax)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Day of week")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with sentiment_tab:
    st.subheader("Sentiment across the conversation")
    st.caption(
        "Classifies messages as positive, neutral, or negative. "
        "The sentiment model may need to download the first time you run it."
    )

    if st.button("Analyze sentiment"):
        with st.spinner("Analyzing messages. The first run may take a little longer..."):
            sentiment_df = sentiment.analyze_sentiment(df, selected_user)

        analyzed_df = sentiment_df[sentiment_df["sentiment"] != "Not analyzed"]
        if analyzed_df.empty:
            st.caption("There are no text messages available for sentiment analysis.")
        else:
            sentiment_counts = (
                analyzed_df["sentiment"]
                .value_counts()
                .reindex(["positive", "neutral", "negative"], fill_value=0)
            )
            metric_columns = st.columns(3)
            sentiment_colors = {
                "positive": "#4C9F70",
                "neutral": "#D6A84F",
                "negative": "#C96B67",
            }
            for column, label in zip(metric_columns, sentiment_counts.index):
                with column:
                    st.metric(label.title(), f"{sentiment_counts[label]:,}")

            chart_col, messages_col = st.columns([1, 1.5], gap="large")
            with chart_col:
                fig, ax = plt.subplots(figsize=(6, 4))
                visible_counts = sentiment_counts[sentiment_counts > 0]
                ax.bar(
                    visible_counts.index,
                    visible_counts.values,
                    color=[sentiment_colors[label] for label in visible_counts.index],
                    width=0.65,
                )
                ax.set_ylabel("Messages")
                ax.grid(axis="y", alpha=0.2)
                ax.set_axisbelow(True)
                ax.spines[["top", "right", "left"]].set_visible(False)
                fig.tight_layout()
                st.pyplot(fig, use_container_width=True)
                plt.close(fig)

            with messages_col:
                st.markdown("#### Analyzed messages")
                st.dataframe(
                    analyzed_df[["date", "user", "message", "sentiment", "confidence"]],
                    use_container_width=True,
                    hide_index=True,
                )
    else:
        st.caption("Choose Analyze sentiment when you're ready to run the model.")
