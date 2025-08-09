import os
from dotenv import load_dotenv
from services.reddit_client import RedditClient

def main():
    # Load environment variables
    load_dotenv()

    print("🚀 Starting Social Threat Monitor")
    print("=" * 40)

    try:
        # Initialize Reddit client
        client = RedditClient()

        # Get subreddits to monitor
        subreddits = os.getenv("SUBREDDITS", "").split(",")
        subreddits = [s.strip() for s in subreddits if s.strip()]

        print(f"📋 Monitoring: {', '.join(subreddits)}")
        print("=" * 40)

        total_threats = 0

        # Scan each subreddit
        for subreddit_name in subreddits:
            result = client.scan_subreddit(subreddit_name)

            if "error" in result:
                continue

            print(f"\n📊 r/{result['subreddit']} Results:")
            print(f"   Posts scanned: {result['posts_scanned']}")
            print(f"   Threats found: {result['threats_found']}")

            total_threats += result['threats_found']

            # Show detections
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
        print(f"✅ Scan complete! Total threats detected: {total_threats}")

    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
