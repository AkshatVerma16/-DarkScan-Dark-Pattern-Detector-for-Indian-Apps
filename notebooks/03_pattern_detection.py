import pandas as pd

print("Dark Pattern Detection started...")
print("=" * 50)

# Load cleaned data
df = pd.read_csv("data/cleaned_reviews.csv")
print(f"Total reviews loaded: {len(df)}")

# ─────────────────────────────────────────
# STEP 3A: Dark Pattern Keywords Dictionary
# ─────────────────────────────────────────

print("\n--- Step 3A: Building Keywords Dictionary ---")

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

print(f"Total dark pattern categories: {len(dark_pattern_keywords)}")
for pattern, keywords in dark_pattern_keywords.items():
    print(f"  {pattern}: {len(keywords)} keywords")

# ─────────────────────────────────────────
# STEP 3B: Detection Functions
# ─────────────────────────────────────────

print("\n--- Step 3B: Setting Up Detection Functions ---")

def detect_dark_patterns(review_text):
    """
    Takes a review text and returns list of
    dark patterns found in it
    """
    found_patterns = []

    for pattern_name, keywords in dark_pattern_keywords.items():
        for keyword in keywords:
            if keyword in str(review_text).lower():
                found_patterns.append(pattern_name)
                break

    return found_patterns

def has_dark_pattern(review_text):
    """Returns True if any dark pattern is found"""
    return len(detect_dark_patterns(review_text)) > 0

def count_dark_patterns(review_text):
    """Returns count of dark patterns found"""
    return len(detect_dark_patterns(review_text))

# Test the function
test_review = "the app added insurance automatically without my permission and hidden charges appeared at checkout"
print(f"\nTest review: '{test_review}'")
print(f"Detected patterns: {detect_dark_patterns(test_review)}")

# ─────────────────────────────────────────
# STEP 3C: Apply Detection on All Reviews
# ─────────────────────────────────────────

print("\n--- Step 3C: Running Detection on All Reviews ---")

df['detected_patterns'] = df['cleaned_review'].apply(detect_dark_patterns)
df['has_dark_pattern'] = df['cleaned_review'].apply(has_dark_pattern)
df['pattern_count'] = df['cleaned_review'].apply(count_dark_patterns)

df['detected_patterns_str'] = df['detected_patterns'].apply(
    lambda x: ', '.join(x) if x else 'none'
)

print(f"Detection complete!")
print(f"Reviews with dark patterns: {df['has_dark_pattern'].sum()}")
print(f"Reviews without dark patterns: {(~df['has_dark_pattern']).sum()}")

# ─────────────────────────────────────────
# STEP 3D: App-wise Analysis
# ─────────────────────────────────────────

print("\n--- Step 3D: App-wise Analysis ---")

app_analysis = df.groupby('app').agg(
    total_reviews=('review', 'count'),
    dark_pattern_reviews=('has_dark_pattern', 'sum'),
).reset_index()

app_analysis['manipulation_score'] = (
    (app_analysis['dark_pattern_reviews'] / app_analysis['total_reviews']) * 100
).round(1)

print("\nApp-wise Manipulation Score:")
print(app_analysis.sort_values('manipulation_score', ascending=False))

# ─────────────────────────────────────────
# STEP 3E: Pattern-wise Breakdown
# ─────────────────────────────────────────

print("\n--- Step 3E: Pattern-wise Breakdown ---")

all_patterns = []
for patterns in df['detected_patterns']:
    all_patterns.extend(patterns)

pattern_series = pd.Series(all_patterns)
print("\nMost common dark patterns:")
print(pattern_series.value_counts())

# ─────────────────────────────────────────
# STEP 3F: Save Results
# ─────────────────────────────────────────

df.to_csv("data/detected_reviews.csv", index=False)
app_analysis.to_csv("data/app_scores.csv", index=False)

print("\n" + "=" * 50)
print("Files saved:")
print("  data/detected_reviews.csv")
print("  data/app_scores.csv")
print("\nDark Pattern Detection Complete!")