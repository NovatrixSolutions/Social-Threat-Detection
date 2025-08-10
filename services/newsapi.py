import requests

def fetch_newsapi_women_harassment(api_key):
    query = "women harassment OR women abuse OR gender violence OR sexual harassment"
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevance",
        "pageSize": 10,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print("Error:", data.get("message"))
        return []

    for article in data.get("articles", []):
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print("-" * 80)

if __name__ == "__main__":
    NEWSAPI_KEY = "6d56700244b04c6484a798a48118a455"
    fetch_newsapi_women_harassment(NEWSAPI_KEY)
