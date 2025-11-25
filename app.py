#!/usr/bin/env python3
"""
Social Threat Monitor - Flask API
Individual endpoints for each service with fresh data fetching
TWITTER DISABLED - Python 3.13 imghdr compatibility issue
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import traceback
import sys
from datetime import datetime
from typing import Dict, Any

from services.reddit_service import RedditService
# from services.twitter_service import TwitterService  # 🚫 DISABLED Python 3.13
from services.youtube_service import YouTubeService
from services.gnews_service import GNewsService
from services.newsapi_service import NewsAPIService
from utils.logger import setup_logger
import os

app = Flask(__name__)
CORS(app)

logger = setup_logger("flask_app")

service_instances = {}

def get_service_instance(service_name: str):
    """Get or create service instance with error handling"""
    if service_name not in service_instances:
        try:
            if service_name == "reddit":
                service_instances[service_name] = RedditService()
            elif service_name == "twitter":
                logger.warning("🚫 Twitter DISABLED - Python 3.13 imghdr issue")
                service_instances[service_name] = None
                return None
            elif service_name == "youtube":
                service_instances[service_name] = YouTubeService()
            elif service_name == "gnews":
                service_instances[service_name] = GNewsService()
            elif service_name == "newsapi":
                service_instances[service_name] = NewsAPIService()
            else:
                raise ValueError(f"Unknown service: {service_name}")

            logger.info(f"✅ {service_name.capitalize()} service initialized")

        except Exception as e:
            logger.error(f"❌ Failed to initialize {service_name}: {e}")
            service_instances[service_name] = None
            return None

    return service_instances[service_name]

@app.route('/api/reddit/scan', methods=['GET'])
def scan_reddit():
    try:
        subreddit = request.args.get('subreddit', 'TwoXChromosomes')
        limit = request.args.get('limit', 10, type=int)

        service = get_service_instance('reddit')
        if not service:
            return jsonify({
                "success": False,
                "error": "Reddit service unavailable",
                "service": "reddit",
                "timestamp": datetime.utcnow().isoformat()
            }), 503

        logger.info(f"🔍 Reddit scan requested: r/{subreddit}, limit={limit}")
        result = service.fetch_data(subreddit_name=subreddit, limit=limit)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ Reddit scan error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "reddit",
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/twitter/scan', methods=['GET'])
def scan_twitter():
    return jsonify({
        "success": False,
        "error": "Twitter temporarily disabled (Python 3.13 imghdr issue)",
        "service": "twitter",
        "status": "Available: reddit, youtube, gnews, newsapi",
        "timestamp": datetime.utcnow().isoformat()
    }), 503

@app.route('/api/youtube/scan', methods=['GET'])
def scan_youtube():
    try:
        query = request.args.get('query', 'women harassment')
        limit = request.args.get('limit', 20, type=int)

        service = get_service_instance('youtube')
        if not service:
            return jsonify({
                "success": False,
                "error": "YouTube service unavailable",
                "service": "youtube",
                "timestamp": datetime.utcnow().isoformat()
            }), 503

        logger.info(f"🔍 YouTube scan requested: query='{query}', limit={limit}")
        result = service.fetch_data(query=query, max_results=limit)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ YouTube scan error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "youtube",
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/gnews/scan', methods=['GET'])
def scan_gnews():
    try:
        query = request.args.get('query', 'women harassment OR gender violence OR sexual harassment')
        limit = request.args.get('limit', 20, type=int)

        service = get_service_instance('gnews')
        if not service:
            return jsonify({
                "success": False,
                "error": "GNews service unavailable",
                "service": "gnews",
                "timestamp": datetime.utcnow().isoformat()
            }), 503

        logger.info(f"🔍 GNews scan requested: query='{query}', limit={limit}")
        result = service.fetch_data(query=query, max_articles=limit)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ GNews scan error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "gnews",
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/newsapi/scan', methods=['GET'])
def scan_newsapi():
    try:
        query = request.args.get('query', 'women harassment OR women abuse OR sexual harassment')
        limit = request.args.get('limit', 20, type=int)

        service = get_service_instance('newsapi')
        if not service:
            return jsonify({
                "success": False,
                "error": "NewsAPI service unavailable",
                "service": "newsapi",
                "timestamp": datetime.utcnow().isoformat()
            }), 503

        logger.info(f"🔍 NewsAPI scan requested: query='{query}', limit={limit}")
        result = service.fetch_data(query=query, max_articles=limit)
        return jsonify(result)

    except Exception as e:
        logger.error(f"❌ NewsAPI scan error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "service": "newsapi",
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/scan/all', methods=['GET'])
def scan_all_services():
    try:
        query = request.args.get('query', 'harassment OR abuse')
        subreddit = request.args.get('subreddit', 'TwoXChromosomes')
        limit = request.args.get('limit', 20, type=int)

        results = {
            "scan_timestamp": datetime.utcnow().isoformat(),
            "total_threats_found": 0,
            "services_scanned": 0,
            "services": {}
        }

        service_configs = [
            ("reddit", {"subreddit_name": subreddit, "limit": limit}),
            ("twitter", {"query": query, "max_tweets": limit}),
            ("youtube", {"query": query, "max_results": limit}),
            ("gnews", {"query": query, "max_articles": limit}),
            ("newsapi", {"query": query, "max_articles": limit})
        ]

        for service_name, config in service_configs:
            try:
                service = get_service_instance(service_name)
                if service:
                    logger.info(f"🔍 Scanning {service_name}")
                    result = service.fetch_data(**config)
                    results["services"][service_name] = result

                    if result.get("success"):
                        threats_found = result.get("data", {}).get("threats_found", 0)
                        results["total_threats_found"] += threats_found
                        results["services_scanned"] += 1
                else:
                    results["services"][service_name] = {
                        "success": False,
                        "error": f"{service_name} service unavailable",
                        "timestamp": datetime.utcnow().isoformat()
                    }

            except Exception as e:
                logger.error(f"❌ Error scanning {service_name}: {e}")
                results["services"][service_name] = {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }

        results["scan_completed"] = datetime.utcnow().isoformat()
        logger.info(f"✅ All services scan completed: {results['total_threats_found']} total threats found")

        return jsonify(results)

    except Exception as e:
        logger.error(f"❌ All services scan error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        services_status = {}
        # Twitter always shows unavailable
        for service_name in ["reddit", "twitter", "youtube", "gnews", "newsapi"]:
            try:
                service = get_service_instance(service_name)
                if service_name == "twitter":
                    services_status[service_name] = "unavailable"
                else:
                    services_status[service_name] = "available" if service else "unavailable"
            except Exception:
                services_status[service_name] = "error"

        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": services_status,
            "endpoints": [
                "/api/reddit/scan",
                "/api/twitter/scan",
                "/api/youtube/scan",
                "/api/gnews/scan",
                "/api/newsapi/scan",
                "/api/scan/all",
                "/api/health"
            ]
        })

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "GET /api/reddit/scan?subreddit=<name>&limit=<num>",
            "GET /api/twitter/scan?query=<text>&limit=<num>",
            "GET /api/youtube/scan?query=<text>&limit=<num>",
            "GET /api/gnews/scan?query=<text>&limit=<num>",
            "GET /api/newsapi/scan?query=<text>&limit=<num>",
            "GET /api/scan/all",
            "GET /api/health"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "timestamp": datetime.utcnow().isoformat()
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info("🚀 Starting Social Threat Monitor API Server")
    logger.info("📋 Available endpoints:")
    logger.info("   GET /api/reddit/scan?subreddit=<name>&limit=<num>")
    logger.info("   GET /api/twitter/scan?query=<text>&limit=<num>")
    logger.info("   GET /api/youtube/scan?query=<text>&limit=<num>")
    logger.info("   GET /api/gnews/scan?query=<text>&limit=<num>")
    logger.info("   GET /api/newsapi/scan?query=<text>&limit=<num>")
    logger.info("   GET /api/scan/all?query=<text>&subreddit=<name>&limit=<num>")
    logger.info("   GET /api/health")
    app.run(debug=False, host='0.0.0.0', port=port)
























    # #!/usr/bin/env python3
# """
# Social Threat Monitor - Flask API
# Individual endpoints for each service with fresh data fetching
# """
#
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import json
# import traceback
# import sys
# from datetime import datetime
# from typing import Dict, Any
#
# from services.reddit_service import RedditService
# from services.twitter_service import TwitterService
# from services.youtube_service import YouTubeService
# from services.gnews_service import GNewsService
# from services.newsapi_service import NewsAPIService
# from utils.logger import setup_logger
# import os
#
#
# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend integration
#
# logger = setup_logger("flask_app")
#
# # Service instances cache
# service_instances = {}
#
# def get_service_instance(service_name: str):
#     """Get or create service instance with error handling"""
#     if service_name not in service_instances:
#         try:
#             if service_name == "reddit":
#                 service_instances[service_name] = RedditService()
#             elif service_name == "twitter":
#                 service_instances[service_name] = TwitterService()
#             elif service_name == "youtube":
#                 service_instances[service_name] = YouTubeService()
#             elif service_name == "gnews":
#                 service_instances[service_name] = GNewsService()
#             elif service_name == "newsapi":
#                 service_instances[service_name] = NewsAPIService()
#             else:
#                 raise ValueError(f"Unknown service: {service_name}")
#
#             logger.info(f"✅ {service_name.capitalize()} service initialized")
#
#         except Exception as e:
#             logger.error(f"❌ Failed to initialize {service_name}: {e}")
#             return None
#
#     return service_instances[service_name]
#
# @app.route('/api/reddit/scan', methods=['GET'])
# def scan_reddit():
#     """
#     Scan Reddit for threats
#     Query parameters:
#     - subreddit: subreddit name (default: TwoXChromosomes)
#     - limit: number of posts to scan (default: 10)
#     """
#     try:
#         subreddit = request.args.get('subreddit', 'TwoXChromosomes')
#         limit = request.args.get('limit', 10, type=int)
#
#         service = get_service_instance('reddit')
#         if not service:
#             return jsonify({
#                 "success": False,
#                 "error": "Reddit service unavailable",
#                 "service": "reddit",
#                 "timestamp": datetime.utcnow().isoformat()
#             }), 503
#
#         logger.info(f"🔍 Reddit scan requested: r/{subreddit}, limit={limit}")
#         result = service.fetch_data(subreddit_name=subreddit, limit=limit)
#
#         return jsonify(result)
#
#     except Exception as e:
#         logger.error(f"❌ Reddit scan error: {e}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "service": "reddit",
#             "timestamp": datetime.utcnow().isoformat()
#         }), 500
#
# @app.route('/api/twitter/scan', methods=['GET'])
# def scan_twitter():
#     """
#     Scan Twitter for threats
#     Query parameters:
#     - query: search query (default: harassment OR abuse)
#     - limit: max tweets to scan (default: 50)
#     """
#     try:
#         query = request.args.get('query', 'harassment OR abuse OR threat')
#         limit = request.args.get('limit', 50, type=int)
#
#         service = get_service_instance('twitter')
#         if not service:
#             return jsonify({
#                 "success": False,
#                 "error": "Twitter service unavailable",
#                 "service": "twitter",
#                 "timestamp": datetime.utcnow().isoformat()
#             }), 503
#
#         logger.info(f"🔍 Twitter scan requested: query='{query}', limit={limit}")
#         result = service.fetch_data(query=query, max_tweets=limit)
#
#         return jsonify(result)
#
#     except Exception as e:
#         logger.error(f"❌ Twitter scan error: {e}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "service": "twitter",
#             "timestamp": datetime.utcnow().isoformat()
#         }), 500
#
# @app.route('/api/youtube/scan', methods=['GET'])
# def scan_youtube():
#     """
#     Scan YouTube for threats
#     Query parameters:
#     - query: search query (default: women harassment)
#     - limit: max videos to scan (default: 20)
#     """
#     try:
#         query = request.args.get('query', 'women harassment')
#         limit = request.args.get('limit', 20, type=int)
#
#         service = get_service_instance('youtube')
#         if not service:
#             return jsonify({
#                 "success": False,
#                 "error": "YouTube service unavailable",
#                 "service": "youtube",
#                 "timestamp": datetime.utcnow().isoformat()
#             }), 503
#
#         logger.info(f"🔍 YouTube scan requested: query='{query}', limit={limit}")
#         result = service.fetch_data(query=query, max_results=limit)
#
#         return jsonify(result)
#
#     except Exception as e:
#         logger.error(f"❌ YouTube scan error: {e}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "service": "youtube",
#             "timestamp": datetime.utcnow().isoformat()
#         }), 500
#
# @app.route('/api/gnews/scan', methods=['GET'])
# def scan_gnews():
#     """
#     Scan GNews for threats
#     Query parameters:
#     - query: search query (default: women harassment OR gender violence)
#     - limit: max articles to scan (default: 20)
#     """
#     try:
#         query = request.args.get('query', 'women harassment OR gender violence OR sexual harassment')
#         limit = request.args.get('limit', 20, type=int)
#
#         service = get_service_instance('gnews')
#         if not service:
#             return jsonify({
#                 "success": False,
#                 "error": "GNews service unavailable",
#                 "service": "gnews",
#                 "timestamp": datetime.utcnow().isoformat()
#             }), 503
#
#         logger.info(f"🔍 GNews scan requested: query='{query}', limit={limit}")
#         result = service.fetch_data(query=query, max_articles=limit)
#
#         return jsonify(result)
#
#     except Exception as e:
#         logger.error(f"❌ GNews scan error: {e}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "service": "gnews",
#             "timestamp": datetime.utcnow().isoformat()
#         }), 500
#
# @app.route('/api/newsapi/scan', methods=['GET'])
# def scan_newsapi():
#     """
#     Scan NewsAPI for threats
#     Query parameters:
#     - query: search query (default: women harassment OR abuse)
#     - limit: max articles to scan (default: 20)
#     """
#     try:
#         query = request.args.get('query', 'women harassment OR women abuse OR sexual harassment')
#         limit = request.args.get('limit', 20, type=int)
#
#         service = get_service_instance('newsapi')
#         if not service:
#             return jsonify({
#                 "success": False,
#                 "error": "NewsAPI service unavailable",
#                 "service": "newsapi",
#                 "timestamp": datetime.utcnow().isoformat()
#             }), 503
#
#         logger.info(f"🔍 NewsAPI scan requested: query='{query}', limit={limit}")
#         result = service.fetch_data(query=query, max_articles=limit)
#
#         return jsonify(result)
#
#     except Exception as e:
#         logger.error(f"❌ NewsAPI scan error: {e}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "service": "newsapi",
#             "timestamp": datetime.utcnow().isoformat()
#         }), 500
#
# @app.route('/api/scan/all', methods=['GET'])
# def scan_all_services():
#     """
#     Scan all available services
#     Query parameters:
#     - query: search query for Twitter, YouTube, and news services
#     - subreddit: Reddit subreddit to scan
#     - limit: limit for each service
#     """
#     try:
#         query = request.args.get('query', 'harassment OR abuse')
#         subreddit = request.args.get('subreddit', 'TwoXChromosomes')
#         limit = request.args.get('limit', 20, type=int)
#
#         results = {
#             "scan_timestamp": datetime.utcnow().isoformat(),
#             "total_threats_found": 0,
#             "services_scanned": 0,
#             "services": {}
#         }
#
#         # Define service configurations
#         service_configs = [
#             ("reddit", {"subreddit_name": subreddit, "limit": limit}),
#             ("twitter", {"query": query, "max_tweets": limit}),
#             ("youtube", {"query": query, "max_results": limit}),
#             ("gnews", {"query": query, "max_articles": limit}),
#             ("newsapi", {"query": query, "max_articles": limit})
#         ]
#
#         for service_name, config in service_configs:
#             try:
#                 service = get_service_instance(service_name)
#                 if service:
#                     logger.info(f"🔍 Scanning {service_name}")
#                     result = service.fetch_data(**config)
#                     results["services"][service_name] = result
#
#                     if result.get("success"):
#                         threats_found = result.get("data", {}).get("threats_found", 0)
#                         results["total_threats_found"] += threats_found
#                         results["services_scanned"] += 1
#                 else:
#                     results["services"][service_name] = {
#                         "success": False,
#                         "error": f"{service_name} service unavailable",
#                         "timestamp": datetime.utcnow().isoformat()
#                     }
#
#             except Exception as e:
#                 logger.error(f"❌ Error scanning {service_name}: {e}")
#                 results["services"][service_name] = {
#                     "success": False,
#                     "error": str(e),
#                     "timestamp": datetime.utcnow().isoformat()
#                 }
#
#         results["scan_completed"] = datetime.utcnow().isoformat()
#         logger.info(f"✅ All services scan completed: {results['total_threats_found']} total threats found")
#
#         return jsonify(results)
#
#     except Exception as e:
#         logger.error(f"❌ All services scan error: {e}")
#         logger.error(traceback.format_exc())
#         return jsonify({
#             "success": False,
#             "error": str(e),
#             "timestamp": datetime.utcnow().isoformat()
#         }), 500
#
# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     try:
#         services_status = {}
#
#         for service_name in ["reddit", "twitter", "youtube", "gnews", "newsapi"]:
#             try:
#                 service = get_service_instance(service_name)
#                 services_status[service_name] = "available" if service else "unavailable"
#             except Exception:
#                 services_status[service_name] = "error"
#
#         return jsonify({
#             "status": "healthy",
#             "timestamp": datetime.utcnow().isoformat(),
#             "services": services_status,
#             "endpoints": [
#                 "/api/reddit/scan",
#                 "/api/twitter/scan",
#                 "/api/youtube/scan",
#                 "/api/gnews/scan",
#                 "/api/newsapi/scan",
#                 "/api/scan/all",
#                 "/api/health"
#             ]
#         })
#
#     except Exception as e:
#         return jsonify({
#             "status": "unhealthy",
#             "error": str(e),
#             "timestamp": datetime.utcnow().isoformat()
#         }), 500
#
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({
#         "error": "Endpoint not found",
#         "available_endpoints": [
#             "GET /api/reddit/scan?subreddit=<name>&limit=<num>",
#             "GET /api/twitter/scan?query=<text>&limit=<num>",
#             "GET /api/youtube/scan?query=<text>&limit=<num>",
#             "GET /api/gnews/scan?query=<text>&limit=<num>",
#             "GET /api/newsapi/scan?query=<text>&limit=<num>",
#             "GET /api/scan/all",
#             "GET /api/health"
#         ]
#     }), 404
#
# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({
#         "error": "Internal server error",
#         "timestamp": datetime.utcnow().isoformat()
#     }), 500
#
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     logger.info("🚀 Starting Social Threat Monitor API Server")
#     logger.info("🚀 Starting Social Threat Monitor API Server")
#     logger.info("📋 Available endpoints:")
#     logger.info("   GET /api/reddit/scan?subreddit=<name>&limit=<num>")
#     logger.info("   GET /api/twitter/scan?query=<text>&limit=<num>")
#     logger.info("   GET /api/youtube/scan?query=<text>&limit=<num>")
#     logger.info("   GET /api/gnews/scan?query=<text>&limit=<num>")
#     logger.info("   GET /api/newsapi/scan?query=<text>&limit=<num>")
#     logger.info("   GET /api/scan/all?query=<text>&subreddit=<name>&limit=<num>")
#     logger.info("   GET /api/health")
#     app.run(debug=False, host='0.0.0.0', port=port)  # Fixed for Render
#
#
