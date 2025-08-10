import requests

def fetch_gnews_women_harassment(api_key):
    query = "women harassment OR women abuse OR gender violence OR sexual harassment"
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "lang": "en",
        "max": 10,
        "token": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "articles" not in data:
        print("Error:", data)
        return []

    for article in data["articles"]:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print("-" * 80)

if __name__ == "__main__":
    GNEWS_API_KEY = "dd27943d7515970b6f4db1126300c643"
    fetch_gnews_women_harassment(GNEWS_API_KEY)
