import os
from dotenv import load_dotenv
from services.reddit_client import RedditClient
from services.twitterapi import TwitterClient

def scan_twitter_by_keyword():
    client = TwitterClient()

    query = os.getenv("TWITTER_SEARCH_QUERY", "harass OR threat OR abuse")
    max_tweets = int(os.getenv("TWITTER_MAX_TWEETS", "50"))

    result = client.scan_recent_tweets(query=query, max_tweets=max_tweets)

    print(f"\n📊 Twitter search results for '{query}':")
    print(f"   Tweets scanned: {result['tweets_scanned']}")
    print(f"   Threats found: {result['threats_found']}")

    for detection in result['detections']:
        print(f"\n   🚨 {detection['type'].upper()} THREAT DETECTED:")
        print(f"      Content: {detection['content']}")
        print(f"      Confidence: {detection['confidence']}")
        print(f"      Created at: {detection.get('created_at', 'N/A')}")

def main():
    load_dotenv()

    print("🚀 Starting Social Threat Monitor")
    print("=" * 40)

    try:
        # Reddit scanning
        reddit_client = RedditClient()

        subreddits = os.getenv("SUBREDDITS", "").split(",")
        subreddits = [s.strip() for s in subreddits if s.strip()]

        print(f"📋 Monitoring Reddit subreddits: {', '.join(subreddits)}")
        print("=" * 40)

        total_threats = 0

        for subreddit_name in subreddits:
            result = reddit_client.scan_subreddit(subreddit_name)

            if "error" in result:
                print(f"⚠️ Skipping r/{subreddit_name} due to error: {result['error']}")
                continue

            print(f"\n📊 r/{result['subreddit']} Results:")
            print(f"   Posts scanned: {result['posts_scanned']}")
            print(f"   Threats found: {result['threats_found']}")

            total_threats += result['threats_found']

            for detection in result['detections']:
                print(f"\n   🚨 {detection['type'].upper()} THREAT DETECTED:")
                if detection['type'] == 'post':
                    print(f"      Title: {detection['title']}")
                    print(f"      URL: {detection['url']}")
                else:
                    print(f"      Post: {detection['post_title']}")
                print(f"      Author: {detection['author']}")
                print(f"      Content: {detection['content']}")
                print(f"      Confidence: {detection['confidence']}")

        print("\n" + "=" * 40)
        print(f"✅ Reddit scan complete! Total threats detected: {total_threats}")

        # Only Twitter keyword search scan (no username)
        scan_twitter_by_keyword()

    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
