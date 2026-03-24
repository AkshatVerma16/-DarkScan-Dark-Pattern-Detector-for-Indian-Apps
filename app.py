import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from google_play_scraper import reviews, Sort, search
import time
import os
import json
import re
from datetime import datetime

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────

st.set_page_config(
    page_title="DarkScan — Detect Dark Patterns in Any App",
    page_icon="🔍",
    layout="wide"
)

# ─────────────────────────────────────────
# DARK PATTERN KEYWORDS
# ─────────────────────────────────────────

dark_pattern_keywords = {
    "fake_urgency": [
        "hurry", "limited time", "only left", "expires",
        "selling fast", "act now", "dont miss", "last chance",
        "ending soon", "few left", "almost gone", "rush",
        "deal ends", "offer ends", "running out", "grab now",
        "before it", "going fast", "2 people", "3 people",
        "viewing this", "popular", "high demand", "book fast",
        "prices rising", "filling up", "almost full"
    ],
    "hidden_costs": [
        "hidden", "extra charge", "surprise", "checkout",
        "added fee", "unexpected", "delivery charge",
        "packaging", "not mentioned", "showed later",
        "final price", "different price", "convenience fee",
        "platform fee", "handling fee", "service fee",
        "taxes added", "charges added", "more than expected",
        "charged more", "paid more", "extra money",
        "not disclosed", "total changed", "price changed",
        "misleading price", "actual price", "real price"
    ],
    "trick_question": [
        "pre selected", "pre checked", "auto selected",
        "automatically added", "insurance", "opted in",
        "checked by default", "already selected", "sneaky",
        "without asking", "without permission", "auto added",
        "default selected", "ticked", "pre ticked",
        "forced", "added itself", "came with", "included without",
        "donation", "tip added", "tip included", "auto tip"
    ],
    "fake_scarcity": [
        "only one left", "only 1 left", "limited seats",
        "limited rooms", "high demand", "popular item",
        "selling out", "almost sold", "few seats", "hurry up",
        "last room", "last seat", "last item", "almost booked",
        "nearly full", "only few", "running low", "scarcity",
        "exclusive", "rare", "limited stock", "low stock"
    ],
    "forced_subscription": [
        "auto renewal", "auto renew", "auto renewed",
        "cancel difficult", "cant cancel", "hard to cancel",
        "subscription trap", "charged automatically",
        "renewed without", "forced subscription",
        "keep charging", "still charging", "deducted",
        "money deducted", "amount deducted", "recurring",
        "charged every", "monthly charge", "annual charge",
        "pro subscription", "gold subscription", "one subscription"
    ],
    "roach_motel": [
        "cant unsubscribe", "no cancel option", "delete account",
        "hard to delete", "no way to cancel", "stuck in",
        "cant remove", "trapped", "no exit", "wont let me cancel",
        "difficult to remove", "no refund", "wont refund",
        "refused refund", "denied refund", "no response",
        "ignoring", "no customer support", "support useless",
        "cant reach", "not responding"
    ]
}

# ─────────────────────────────────────────
# HISTORY FILE
# ─────────────────────────────────────────

HISTORY_FILE = "data/search_history.json"

def load_history():
    # Folder check logic add kiya taaki error na aaye
    if not os.path.exists("data"):
        os.makedirs("data")
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    # Folder check logic add kiya
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def add_to_history(app_name, app_id, score):
    history = load_history()
    history = [h for h in history if h['app_id'] != app_id]
    history.insert(0, {
        "app_name": app_name,
        "app_id": app_id,
        "score": score,
        "analyzed_at": datetime.now().strftime("%d %b %Y, %H:%M")
    })
    history = history[:10]
    save_history(history)

# ─────────────────────────────────────────
# CORE FUNCTIONS
# ─────────────────────────────────────────

def detect_dark_patterns(review_text):
    found_patterns = []
    text = str(review_text).lower()
    for pattern_name, keywords in dark_pattern_keywords.items():
        for keyword in keywords:
            # Re-escape and boundary added for accuracy
            pattern = rf"\b{re.escape(keyword.lower())}\b"
            if re.search(pattern, text):
                found_patterns.append(pattern_name)
                break
    return found_patterns

def fetch_and_analyze(app_id, app_name, review_count=300):
    """Fetch reviews from Play Store and analyze dark patterns"""
    # Try block add kiya taaki internet/API error handled rahe
    try:
        with st.spinner(f"Fetching reviews for {app_name}..."):
            result, _ = reviews(
                app_id,
                lang='en',
                country='in',
                sort=Sort.NEWEST,
                count=review_count
            )

        if not result:
            st.error("Is app ke liye koi reviews nahi mile.")
            return None, 0

        df = pd.DataFrame(result)[['userName', 'content', 'score', 'at']]
        df.columns = ['user', 'review', 'rating', 'date']
        df['app'] = app_name

        with st.spinner("Cleaning data..."):
            df = df.dropna(subset=['review'])
            # IMPROVEMENT: Noise Filter (skip reviews with only symbols/emojis)
            df = df[df['review'].str.contains(r'[a-zA-Z0-9]', na=False)]
            df = df.drop_duplicates(subset=['review'])
            df = df[df['review'].str.len() > 20]
            df['cleaned_review'] = df['review'].str.lower()

        with st.spinner("Detecting dark patterns..."):
            df['detected_patterns'] = df['cleaned_review'].apply(detect_dark_patterns)
            df['has_dark_pattern'] = df['detected_patterns'].apply(lambda x: len(x) > 0)
            df['detected_patterns_str'] = df['detected_patterns'].apply(
                lambda x: ', '.join(x) if x else 'none'
            )

        # Zero division safety
        total_len = len(df)
        score = round((df['has_dark_pattern'].sum() / total_len) * 100, 1) if total_len > 0 else 0
        return df, score
    
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        return None, 0

def search_app(query):
    """Search for app on Play Store"""
    results = search(query, lang='en', country='in', n_hits=5)
    return results

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────

if 'analyzed_df' not in st.session_state:
    st.session_state.analyzed_df = None
if 'current_app' not in st.session_state:
    st.session_state.current_app = None
if 'current_score' not in st.session_state:
    st.session_state.current_score = None

# ─────────────────────────────────────────
# SIDEBAR — SEARCH + HISTORY
# ─────────────────────────────────────────

with st.sidebar:
    st.title("🔍 DarkScan")
    st.caption("Detect dark patterns in any Indian app")
    st.divider()

    st.subheader("Search Any App")
    search_query = st.text_input(
        "App name",
        placeholder="e.g. Blinkit, Paytm, Ola..."
    )

    if search_query:
        with st.spinner("Searching..."):
            try:
                search_results = search_app(search_query)
                st.write("**Select an app:**")
                for app in search_results[:5]:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{app['title']}**")
                        st.caption(app.get('developer', ''))
                    with col2:
                        if st.button("Analyze", key=app['appId']):
                            st.session_state.selected_app_id = app['appId']
                            st.session_state.selected_app_name = app['title']
                            st.rerun()
            except Exception as e:
                st.error(f"Search failed: {e}")

    st.divider()

    # Review count selector
    st.subheader("Settings")
    review_count = st.slider(
        "Number of reviews to analyze",
        min_value=100,
        max_value=500,
        value=300,
        step=100
    )

    st.divider()

    # Search history
    st.subheader("Recent Searches")
    history = load_history()
    if history:
        for item in history:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{item['app_name']}**")
                st.caption(f"Score: {item['score']}% | {item['analyzed_at']}")
            with col2:
                if st.button("↩", key=f"history_{item['app_id']}"):
                    st.session_state.selected_app_id = item['app_id']
                    st.session_state.selected_app_name = item['app_name']
                    st.rerun()
    else:
        st.caption("No searches yet")

# ─────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────

# Auto analyze if app selected
if 'selected_app_id' in st.session_state and st.session_state.selected_app_id:
    app_id = st.session_state.selected_app_id
    app_name = st.session_state.selected_app_name

    result_data = fetch_and_analyze(app_id, app_name, review_count)
    
    if result_data[0] is not None:
        df, score = result_data
        st.session_state.analyzed_df = df
        st.session_state.current_app = app_name
        st.session_state.current_score = score
        add_to_history(app_name, app_id, score)
    
    st.session_state.selected_app_id = None

# ─────────────────────────────────────────
# DASHBOARD — Show results
# ─────────────────────────────────────────

if st.session_state.analyzed_df is not None:
    df = st.session_state.analyzed_df
    app_name = st.session_state.current_app
    score = st.session_state.current_score

    st.title(f"🔍 {app_name} — Dark Pattern Analysis")
    st.divider()

    # KEY METRICS
    col1, col2, col3, col4 = st.columns(4)

    total_dark = df['has_dark_pattern'].sum()
    all_patterns = []
    for p in df['detected_patterns']:
        all_patterns.extend(p)

    with col1:
        st.metric("Total Reviews", f"{len(df):,}")
    with col2:
        st.metric("Dark Pattern Reviews", f"{total_dark:,}")
    with col3:
        color = "inverse" if score > 15 else "normal"
        st.metric("Manipulation Score", f"{score}%", delta_color=color)
    with col4:
        if all_patterns:
            top = pd.Series(all_patterns).value_counts().index[0].replace('_', ' ').title()
            st.metric("Top Dark Pattern", top)
        else:
            st.metric("Top Dark Pattern", "None found")

    st.divider()

    # SCORE VERDICT
    if score == 0:
        st.success("✅ No dark patterns detected in this app!")
    elif score < 10:
        st.info(f"ℹ️ Low manipulation — only {score}% reviews mention dark patterns.")
    elif score < 20:
        st.warning(f"⚠️ Moderate manipulation — {score}% reviews mention dark patterns.")
    else:
        st.error(f"🚨 High manipulation — {score}% reviews mention dark patterns!")

    st.divider()

    # CHARTS
    col1, col2 = st.columns(2)

    with col1:
        if all_patterns:
            pattern_counts = pd.Series(all_patterns).value_counts().reset_index()
            pattern_counts.columns = ['pattern', 'count']
            pattern_counts['pattern'] = pattern_counts['pattern'].str.replace('_', ' ').str.title()

            fig = px.bar(
                pattern_counts,
                x='pattern',
                y='count',
                title=f'Dark Patterns Found in {app_name}',
                color='count',
                color_continuous_scale='Reds'
            )
            fig.update_layout(plot_bgcolor='white', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No dark patterns found to display.")

    with col2:
        fig2 = px.histogram(
            df,
            x='rating',
            title='Rating Distribution',
            color_discrete_sequence=['#3B8BD4'],
            nbins=5
        )
        fig2.update_layout(plot_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)

    # WORD CLOUD
    if total_dark > 0:
        st.subheader("☁️ Word Cloud — Dark Pattern Reviews")
        dark_text = ' '.join(df[df['has_dark_pattern']]['cleaned_review'].tolist())
        wc = WordCloud(
            width=1200, height=400,
            background_color='white',
            max_words=100,
            colormap='Reds'
        ).generate(dark_text)

        fig_wc, ax = plt.subplots(figsize=(14, 4))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig_wc)

    st.divider()

    # REVIEWS TABLE
    st.subheader("💬 Dark Pattern Reviews")

    pattern_filter = st.selectbox(
        "Filter by pattern:",
        options=["All"] + list(dark_pattern_keywords.keys())
    )

    filtered = df[df['has_dark_pattern']].copy()
    if pattern_filter != "All":
        filtered = filtered[
            filtered['detected_patterns'].apply(lambda x: pattern_filter in x)
        ]

    st.write(f"Showing **{len(filtered)}** reviews")

    for _, row in filtered.head(10).iterrows():
        with st.expander(
            f"⚠️ Rating: {'⭐' * int(row['rating'])} | Pattern: {row['detected_patterns_str']}"
        ):
            st.write(row['review'])

    st.divider()

    # SHARE SECTION
    st.subheader("📤 Share Results")
    share_text = f"""
    🔍 Dark Pattern Analysis: {app_name}
    
    Manipulation Score: {score}%
    Total Reviews Analyzed: {len(df)}
    Dark Pattern Reviews: {total_dark}
    
    Analyzed using DarkScan
    """
    st.code(share_text, language=None)
    st.caption("Copy this text and share on LinkedIn, Twitter, or WhatsApp!")

else:
    # LANDING PAGE — when no app is analyzed yet
    st.title("🔍 DarkScan")
    st.subheader("Detect Dark Patterns in Any Indian App")
    st.write("Search any app from the sidebar and instantly see how manipulative it is!")

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🎯 Any App**\nSearch and analyze any app on Play Store")
    with col2:
        st.warning("**⚡ Real-time**\nFetches latest reviews automatically")
    with col3:
        st.success("**📊 6 Patterns**\nDetects 6 types of dark patterns")

    st.divider()
    st.caption("👈 Search an app from the sidebar to get started!")