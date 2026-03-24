from google_play_scraper import reviews, Sort
import pandas as pd
import time

print("Data collection shuru ho rahi hai...")
print("=" * 50)

apps = {
    "Zomato": "com.application.zomato",
    "Swiggy": "in.swiggy.android",
    "MakeMyTrip": "com.makemytrip"
}

def collect_reviews(app_name, app_id, count=500):
    print(f"\n{app_name} ke reviews download ho rahe hain...")
    
    result, _ = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=count
    )
    
    df = pd.DataFrame(result)
    
    df = df[['userName', 'content', 'score', 'at']]
    df.columns = ['user', 'review', 'rating', 'date']
    df['app'] = app_name
    
    filename = f"data/{app_name.lower()}_reviews.csv"
    df.to_csv(filename, index=False)
    
    print(f"Total reviews mila: {len(df)}")
    print(f"File save hui: {filename}")
    print(f"Sample review: {df['review'].iloc[0][:80]}...")
    
    return df

all_data = []

for app_name, app_id in apps.items():
    df = collect_reviews(app_name, app_id, count=500)
    all_data.append(df)
    time.sleep(2)

combined_df = pd.concat(all_data, ignore_index=True)
combined_df.to_csv("data/all_reviews.csv", index=False)

print("\n" + "=" * 50)
print("Data collection complete!")
print(f"Total reviews collected: {len(combined_df)}")
print("\nApp-wise breakdown:")
print(combined_df['app'].value_counts())
print("\nRating distribution:")
print(combined_df['rating'].value_counts().sort_index())