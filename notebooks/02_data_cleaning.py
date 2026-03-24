import pandas as pd
import re

print("Data cleaning shuru ho rahi hai...")
print("=" * 50)

# Load the combined data
df = pd.read_csv("data/all_reviews.csv")

print(f"Raw data mein total reviews: {len(df)}")
print(f"\nPehle 3 rows dekhte hain:")
print(df.head(3))

# ─────────────────────────────────────────
# STEP 2A: Basic cleaning
# ─────────────────────────────────────────

print("\n--- Step 2A: Basic Cleaning ---")

# Remove rows where review text is empty
df = df.dropna(subset=['review'])
print(f"Empty reviews hatane ke baad: {len(df)}")

# Remove duplicate reviews
df = df.drop_duplicates(subset=['review'])
print(f"Duplicate reviews hatane ke baad: {len(df)}")

# Remove reviews shorter than 20 characters (not useful)
df = df[df['review'].str.len() > 20]
print(f"Choti reviews hatane ke baad: {len(df)}")

# ─────────────────────────────────────────
# STEP 2B: Text cleaning
# ─────────────────────────────────────────

print("\n--- Step 2B: Text Cleaning ---")

def clean_text(text):
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Apply cleaning to review column
df['cleaned_review'] = df['review'].apply(clean_text)

print("Text cleaning complete!")
print(f"\nOriginal review example:")
print(df['review'].iloc[0])
print(f"\nCleaned review example:")
print(df['cleaned_review'].iloc[0])

# ─────────────────────────────────────────
# STEP 2C: Add useful columns
# ─────────────────────────────────────────

print("\n--- Step 2C: Extra Columns Add kar rahe hain ---")

# Review length (useful for analysis)
df['review_length'] = df['review'].str.len()

# Convert date column properly
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

print("Extra columns add ho gayi!")

# ─────────────────────────────────────────
# STEP 2D: Final summary
# ─────────────────────────────────────────

print("\n--- Step 2D: Final Summary ---")
print(f"\nFinal clean data mein total reviews: {len(df)}")
print(f"\nApp-wise breakdown:")
print(df['app'].value_counts())
print(f"\nAverage rating per app:")
print(df.groupby('app')['rating'].mean().round(2))
print(f"\nAverage review length:")
print(df.groupby('app')['review_length'].mean().round(0))

# Save cleaned data
df.to_csv("data/cleaned_reviews.csv", index=False)
print("\nCleaned data save ho gaya: data/cleaned_reviews.csv")
print("=" * 50)
print("Data cleaning complete!")