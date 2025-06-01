
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.moengage_scraper import MoEngageScraper
from analyzer.documentation_analyzer import DocumentationAnalyzer
from utils.logger import setup_logger

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
scraper = MoEngageScraper()
analyzer = DocumentationAnalyzer()
logger = setup_logger()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "MoEngage Documentation Analyzer API is running"})

@app.route('/test-urls', methods=['GET'])
def get_test_urls():
    """Get test URLs that should work for scraping"""
    test_urls = [
        {
            "url": "https://httpbin.org/html",
            "description": "Simple HTML test page"
        },
        {
            "url": "https://example.com",
            "description": "Basic example page"
        },
        {
            "url": "https://en.wikipedia.org/wiki/Web_scraping",
            "description": "Wikipedia article on web scraping"
        },
        {
            "url": "https://jsonplaceholder.typicode.com/posts/1",
            "description": "JSON API endpoint (will return JSON data)"
        }
    ]
    return jsonify({"test_urls": test_urls})

@app.route('/analyze', methods=['POST'])
def analyze_documentation():
    """Analyze a documentation URL"""
    try:
        # Get URL from request
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required in request body"}), 400
        
        url = data['url']
        logger.info(f"Analyzing URL: {url}")
        
        # Step 1: Scrape the documentation
        logger.info("Scraping content...")
        scraped_data = scraper.scrape_url(url)
        
        if not scraped_data or 'error' in scraped_data:
            error_msg = scraped_data.get('error', 'Unknown scraping error')
            logger.error(f"Scraping failed: {error_msg}")
            
            # Provide better error messages for common issues
            if "403" in error_msg or "Forbidden" in error_msg:
                return jsonify({
                    "error": "Access denied to the URL. The website may be blocking automated requests. Please try a different URL or check if the URL is publicly accessible.",
                    "suggestion": "Try using one of the test URLs from /test-urls endpoint"
                }), 400
            elif "Failed to fetch" in error_msg:
                return jsonify({
                    "error": "Unable to access the URL. Please check if the URL is correct and accessible.",
                    "suggestion": "Try using one of the test URLs from /test-urls endpoint"
                }), 400
            else:
                return jsonify({
                    "error": f"Failed to scrape URL: {error_msg}",
                    "suggestion": "Try using one of the test URLs from /test-urls endpoint"
                }), 400
        
        # Step 2: Analyze the content
        logger.info("Analyzing content...")
        analysis_result = analyzer.analyze_document(scraped_data)
        
        if 'error' in analysis_result:
            error_msg = analysis_result.get('error', 'Unknown analysis error')
            logger.error(f"Analysis failed: {error_msg}")
            return jsonify({"error": f"Analysis failed: {error_msg}"}), 500
        
        logger.info("✅ Analysis completed successfully")
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/analyze/batch', methods=['POST'])
def analyze_batch():
    """Analyze multiple URLs in batch"""
    try:
        data = request.get_json()
        if not data or 'urls' not in data:
            return jsonify({"error": "URLs array is required in request body"}), 400
        
        urls = data['urls']
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({"error": "URLs must be a non-empty array"}), 400
        
        results = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing URL {i}/{len(urls)}: {url}")
            
            try:
                # Scrape and analyze
                scraped_data = scraper.scrape_url(url)
                if 'error' in scraped_data:
                    results.append({"url": url, "error": scraped_data['error']})
                    continue
                
                analysis_result = analyzer.analyze_document(scraped_data)
                results.append(analysis_result)
                
            except Exception as e:
                logger.error(f"Error processing {url}: {str(e)}")
                results.append({"url": url, "error": str(e)})
        
        return jsonify({"results": results, "total_processed": len(urls)})
        
    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}")
        return jsonify({"error": f"Batch analysis failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting MoEngage Documentation Analyzer API...")
    print("📖 API Documentation:")
    print("  POST /analyze - Analyze single URL")
    print("  POST /analyze/batch - Analyze multiple URLs")
    print("  GET /health - Health check")
    print("  GET /test-urls - Get working test URLs")
    print()
    print("🧪 Test URLs available at: http://localhost:5000/test-urls")
    print("🔗 API running on: http://localhost:5000")
    print()
    print("💡 If MoEngage URLs are blocked, try the test URLs first!")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
