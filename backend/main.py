
import os
import json
import argparse
from datetime import datetime
from scraper.moengage_scraper import MoEngageScraper
from analyzer.documentation_analyzer import DocumentationAnalyzer
from utils.file_manager import FileManager
from utils.logger import setup_logger

def main():
    """Main entry point for the MoEngage Documentation Analyzer"""
    
    # Setup logging
    logger = setup_logger()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analyze MoEngage Documentation')
    parser.add_argument('--url', type=str, help='URL to analyze')
    parser.add_argument('--urls-file', type=str, help='File containing URLs to analyze')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize components
    scraper = MoEngageScraper()
    analyzer = DocumentationAnalyzer()
    file_manager = FileManager(args.output_dir)
    
    # Determine URLs to process
    urls = []
    if args.url:
        urls = [args.url]
    elif args.urls_file:
        with open(args.urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        # Default URLs for testing
        urls = [
            "https://partners.moengage.com/hc/en-us/articles/9643917325460-Create-content-creatives",
            "https://help.moengage.com/hc/en-us/articles/28194279371668-How-to-Analyze-OTT-Content-Performance"
        ]
    
    logger.info(f"Processing {len(urls)} URLs...")
    
    results = []
    
    for i, url in enumerate(urls, 1):
        logger.info(f"Processing URL {i}/{len(urls)}: {url}")
        
        try:
            # Step 1: Scrape the documentation
            logger.info("Scraping content...")
            scraped_data = scraper.scrape_url(url)
            
            if not scraped_data or 'error' in scraped_data:
                logger.error(f"Failed to scrape {url}: {scraped_data.get('error', 'Unknown error')}")
                continue
            
            # Step 2: Analyze the content
            logger.info("Analyzing content...")
            analysis_result = analyzer.analyze_document(scraped_data)
            
            # Step 3: Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{i}_{timestamp}"
            
            # Save individual analysis
            file_manager.save_analysis_result(analysis_result, filename)
            file_manager.save_scraped_content(scraped_data, filename)
            
            results.append(analysis_result)
            
            logger.info(f"✅ Successfully processed {url}")
            
        except Exception as e:
            logger.error(f"❌ Error processing {url}: {str(e)}")
            continue
    
    # Save summary report
    if results:
        summary = {
            "total_documents": len(results),
            "processed_at": datetime.now().isoformat(),
            "results": results
        }
        file_manager.save_summary_report(summary)
        logger.info(f"✅ Analysis complete! Results saved to {args.output_dir}/")
    else:
        logger.warning("No documents were successfully processed.")

if __name__ == "__main__":
    main()
