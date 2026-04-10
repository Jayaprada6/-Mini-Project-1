import requests
import time
import json
import os
from datetime import datetime

print("Program started...")

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category
def get_category(title):
    title = title.lower()
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title:
                return category
    return None


def main():
    try:
        print("Fetching top stories...")
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        story_ids = response.json()[:500]
        print("Total IDs fetched:", len(story_ids))
    except Exception as e:
        print("Error fetching top stories:", e)
        return

    results = []
    category_count = {key: 0 for key in CATEGORIES}

    for story_id in story_ids:
        try:
            print("Fetching story:", story_id)

            url = ITEM_URL.format(story_id)
            res = requests.get(url, headers=HEADERS)
            story = res.json()

            if not story or "title" not in story:
                continue

            category = get_category(story["title"])

            if not category:
                continue

            if category_count[category] >= 25:
                continue

            data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            results.append(data)
            category_count[category] += 1

            # Stop when ~125 collected
            if sum(category_count.values()) >= 125:
                break

        except Exception as e:
            print(f"Error fetching story {story_id}:", e)
            continue

    # Small delay (as per instruction)
    time.sleep(2)

    print("Creating data folder...")
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    print("Saving file...")
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Collected {len(results)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()
