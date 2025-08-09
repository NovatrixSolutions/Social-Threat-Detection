import os
import praw
from .detection import ThreatDetector

class RedditClient:
    def __init__(self):
        self.reddit = self._connect()
        self.detector = ThreatDetector()
        print("✅ Connected to Reddit")

    def _connect(self):
        """Connect to Reddit API"""
        return praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent=os.getenv("USER_AGENT", "SocialThreatMonitor/1.0")
        )

    def scan_subreddit(self, subreddit_name):
        """Scan a subreddit for threats"""
        results = {
            "subreddit": subreddit_name,
            "posts_scanned": 0,
            "threats_found": 0,
            "detections": []
        }

        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            limit = int(os.getenv("POST_LIMIT", "3"))

            print(f"🔍 Scanning r/{subreddit_name}...")

            for post in subreddit.new(limit=limit):
                results["posts_scanned"] += 1

                # Check post content
                content = f"{post.title} {post.selftext or ''}"
                analysis = self.detector.analyze(content)

                if analysis["is_threat"]:
                    results["threats_found"] += 1
                    results["detections"].append({
                        "type": "post",
                        "title": post.title,
                        "author": str(post.author),
                        "content": analysis["text_preview"],
                        "url": post.url,
                        "confidence": analysis["confidence"]
                    })

                # Check top comments
                post.comments.replace_more(limit=0)
                for comment in post.comments.list()[:5]:
                    if hasattr(comment, 'body') and comment.body:
                        analysis = self.detector.analyze(comment.body)
                        if analysis["is_threat"]:
                            results["threats_found"] += 1
                            results["detections"].append({
                                "type": "comment",
                                "post_title": post.title,
                                "author": str(comment.author),
                                "content": analysis["text_preview"],
                                "confidence": analysis["confidence"]
                            })

        except Exception as e:
            print(f"❌ Error scanning r/{subreddit_name}: {e}")
            results["error"] = str(e)

        return results
