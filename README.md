# 🔍 DarkScan: Dark Pattern Detector for Indian Apps

**DarkScan** ek AI-powered analytics tool hai jo Google Play Store ke user reviews ko real-time mein analyze karke mobile applications mein maujood manipulative UX patterns (**Dark Patterns**) ko detect karta hai. Yeh project users ko deceptive design practices ke baare mein aware karne aur apps ki integrity check karne ke liye banaya gaya hai.

---

## 🚀 Overview
DarkScan specifically Indian consumer apps jaise **Zomato, Swiggy, aur MakeMyTrip** par focus karta hai. Yeh system Play Store se automatically reviews fetch karta hai aur advanced text processing ka use karke batata hai ki kaunsa app kitna manipulative hai.

## ✨ Key Features

* **Real-time Analysis:** Sidebar search se kisi bhi app ko select karke uske latest reviews fetch aur analyze karein.
* **Advanced Detection Algorithm:** Keyword-based matching ke saath **Regular Expressions (Regex)** ka use taaki accuracy 100% rahe.
* **Noise Filtering:** Machine learning ready cleaning logic jo emojis aur useless short reviews ko remove karta hai.
* **Interactive Dashboard:** * **Key Metrics:** Total reviews vs flagged reviews ka count.
    * **Manipulation Score:** Percentage base score jo app ki "deceptiveness" batata hai.
    * **Pattern Breakdown:** Pie charts aur Bar graphs ke zariye patterns ki distribution.
    * **Word Cloud:** Dark pattern reviews mein sabse zyada use hone wale words ka visualization.
* **Search History:** Recent searches ko save karta hai taaki aap pichle results ko fast load kar sakein.

## 🛠️ Detection Categories
System niche diye gaye 6 major dark patterns ko identify karta hai:
1.  **Fake Urgency:** Artificial pressure (e.g., "Hurry! Offer ends in 2 mins").
2.  **Hidden Costs:** Checkout ke waqt extra delivery ya platform fees.
3.  **Roach Motel:** Subscription ya account delete karne ko bahut mushkil banana.
4.  **Forced Subscription:** Bina clear consent ke paise deduct karna.
5.  **Trick Questions:** Confusing language se unwanted options select karwana.
6.  **Fake Scarcity:** Jhoothi stock shortage dikhana (e.g., "Only 1 left").

## 📊 Technical Stack
* **Frontend:** Streamlit
* **Data Source:** Google Play Scraper (API-less fetching)
* **Data Handling:** Pandas & JSON
* **Visualization:** Plotly Express, Matplotlib, WordCloud
* **Logic:** Python Regular Expressions (re)

## 📂 Project Structure
```text
dark-patterns-project/
├── app.py                # Main Dashboard Code
├── data/
│   ├── search_history.json # Saved recent searches
│   ├── app_scores.csv      # Benchmarking data
│   └── detected_reviews.csv # Final analyzed output
├── notebooks/
│   ├── 01_data_collection.py # Scraper logic
│   ├── 02_data_cleaning.py   # Text preprocessing
│   └── 03_pattern_detection.py # Regex matching logic
└── README.md             # Documentation

## 🚀 How to Run the Project

Project ko apne local system par run karne ke liye niche diye gaye steps follow karein:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/dark-patterns-project.git](https://github.com/yourusername/dark-patterns-project.git)
    cd dark-patterns-project
    ```

2.  **Create a Virtual Environment (Optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows ke liye: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas plotly matplotlib wordcloud google-play-scraper
    ```

4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

## 🛠️ Implementation Logic (Key Changes)

Is project ko accurate banane ke liye humne do main logic updates kiye hain:

* **Regex-Based Detection:** Humne simple keyword matching ki jagah `re.search(rf"\b{keyword}\b", text)` ka use kiya hai. Isse yeh fayda hota hai ki "One" keyword sirf tabhi match hoga jab woh akela word ho, na ki kisi aur word (jaise "PhonePe") ke beech mein.
* **Noise Filtering:** Reviews fetch karne ke baad hum sirf wahi data rakhte hain jisme alphanumeric characters (a-z, 0-9) ho. Isse sirf emojis ya stars wale useless reviews calculation ko kharab nahi karte.

## 📈 Future Roadmap

* **Sentiment Analysis:** Reviews ke emotional tone ko samajhne ke liye NLP models add karna.
* **App Comparison:** Do apps ke manipulation scores ko side-by-side compare karne ka feature.
* **Browser Extension:** Ek extension banana jo user ko Play Store browse karte waqt hi alert kare.

---
**Author:** Akshat Verma  
**Project Link:** [https://github.com/yourusername/dark-patterns-project](https://github.com/yourusername/dark-patterns-project)