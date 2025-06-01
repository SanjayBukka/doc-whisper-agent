
import os
import json
from datetime import datetime
from pathlib import Path
from utils.logger import get_logger

class FileManager:
    """Handles file operations for saving analysis results"""
    
    def __init__(self, output_dir="output"):
        self.logger = get_logger(__name__)
        self.output_dir = Path(output_dir)
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Create output directory structure"""
        
        directories = [
            self.output_dir,
            self.output_dir / "analysis_results",
            self.output_dir / "scraped_content",
            self.output_dir / "reports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Ensured directory exists: {directory}")
    
    def save_analysis_result(self, analysis_result, filename):
        """Save analysis result as JSON"""
        
        try:
            filepath = self.output_dir / "analysis_results" / f"{filename}.json"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved analysis result: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error saving analysis result: {str(e)}")
            return None
    
    def save_scraped_content(self, scraped_data, filename):
        """Save scraped content as JSON"""
        
        try:
            filepath = self.output_dir / "scraped_content" / f"{filename}_content.json"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(scraped_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved scraped content: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error saving scraped content: {str(e)}")
            return None
    
    def save_summary_report(self, summary_data):
        """Save summary report"""
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.output_dir / "reports" / f"summary_report_{timestamp}.json"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved summary report: {filepath}")
            
            # Also create a readable markdown report
            self._create_markdown_report(summary_data, timestamp)
            
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Error saving summary report: {str(e)}")
            return None
    
    def _create_markdown_report(self, summary_data, timestamp):
        """Create a human-readable markdown report"""
        
        try:
            filepath = self.output_dir / "reports" / f"summary_report_{timestamp}.md"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# MoEngage Documentation Analysis Report\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total Documents Analyzed:** {summary_data.get('total_documents', 0)}\n\n")
                
                for i, result in enumerate(summary_data.get('results', []), 1):
                    f.write(f"## Document {i}: {result.get('document_info', {}).get('title', 'Unknown')}\n\n")
                    f.write(f"**URL:** {result.get('document_info', {}).get('url', 'N/A')}\n")
                    f.write(f"**Word Count:** {result.get('document_info', {}).get('word_count', 'N/A')}\n")
                    f.write(f"**Overall Score:** {result.get('overall_score', 'N/A')}/10\n\n")
                    
                    # Summary
                    summary = result.get('summary', {})
                    f.write("### Summary\n")
                    f.write(f"**Recommendation:** {summary.get('recommendation', 'N/A')}\n\n")
                    
                    if summary.get('strengths'):
                        f.write("**Strengths:**\n")
                        for strength in summary['strengths']:
                            f.write(f"- {strength}\n")
                        f.write("\n")
                    
                    if summary.get('priority_improvements'):
                        f.write("**Priority Improvements:**\n")
                        for improvement in summary['priority_improvements']:
                            f.write(f"- {improvement}\n")
                        f.write("\n")
                    
                    # Detailed scores
                    f.write("### Detailed Scores\n")
                    f.write(f"- **Readability:** {result.get('readability', {}).get('score', 'N/A')}/10\n")
                    f.write(f"- **Structure:** {result.get('structure', {}).get('score', 'N/A')}/10\n")
                    f.write(f"- **Completeness:** {result.get('completeness', {}).get('score', 'N/A')}/10\n")
                    f.write(f"- **Style:** {result.get('style', {}).get('score', 'N/A')}/10\n\n")
                    
                    f.write("---\n\n")
            
            self.logger.info(f"Created markdown report: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error creating markdown report: {str(e)}")
    
    def load_analysis_result(self, filename):
        """Load previously saved analysis result"""
        
        try:
            filepath = self.output_dir / "analysis_results" / f"{filename}.json"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                result = json.load(f)
            
            self.logger.info(f"Loaded analysis result: {filepath}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error loading analysis result: {str(e)}")
            return None
    
    def list_saved_analyses(self):
        """List all saved analysis files"""
        
        try:
            analysis_dir = self.output_dir / "analysis_results"
            files = list(analysis_dir.glob("*.json"))
            return [f.stem for f in files]
            
        except Exception as e:
            self.logger.error(f"Error listing saved analyses: {str(e)}")
            return []
    
    def get_output_summary(self):
        """Get summary of all output files"""
        
        try:
            summary = {
                'analysis_results': len(list((self.output_dir / "analysis_results").glob("*.json"))),
                'scraped_content': len(list((self.output_dir / "scraped_content").glob("*.json"))),
                'reports': len(list((self.output_dir / "reports").glob("*.*"))),
                'output_directory': str(self.output_dir.absolute())
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting output summary: {str(e)}")
            return {}
