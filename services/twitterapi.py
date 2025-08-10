import os
import tweepy
from .detection import ThreatDetector

class TwitterClient:
    def __init__(self):
        self.client = self._connect()
        self.detector = ThreatDetector()
        print("✅ Connected to Twitter")

    def _connect(self):
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        if not bearer_token:
            raise ValueError("TWITTER_BEARER_TOKEN not set in environment")
        return tweepy.Client(bearer_token=bearer_token)

    def scan_recent_tweets(self, query, max_tweets=50):
        results = {
            "query": query,
            "tweets_scanned": 0,
            "threats_found": 0,
            "detections": []
        }

        try:
            # Twitter API max_results per request can be 10-100
            max_per_request = 100
            tweets_to_fetch = min(max_tweets, 500)  # max 500 for example
            next_token = None

            print(f"🔍 Searching recent tweets for query: '{query}'")

            while results["tweets_scanned"] < tweets_to_fetch:
                remaining = tweets_to_fetch - results["tweets_scanned"]
                fetch_count = min(max_per_request, remaining)

                response = self.client.search_recent_tweets(
                    query=query,
                    max_results=fetch_count,
                    tweet_fields=["text", "author_id", "created_at"],
                    next_token=next_token
                )

                tweets = response.data or []
                meta = response.meta

                for tweet in tweets:
                    results["tweets_scanned"] += 1

                    analysis = self.detector.analyze(tweet.text)
                    if analysis.get("is_threat"):
                        results["threats_found"] += 1
                        results["detections"].append({
                            "type": "tweet",
                            "content": analysis.get("text_preview", tweet.text[:50]),
                            "tweet_id": tweet.id,
                            "author_id": tweet.author_id,
                            "created_at": str(tweet.created_at),
                            "confidence": analysis.get("confidence", 0.0)
                        })

                next_token = meta.get("next_token")
                if not next_token:
                    break  # no more tweets

        except Exception as e:
            print(f"❌ Error searching tweets for query '{query}': {e}")
            results["error"] = str(e)

        return results
