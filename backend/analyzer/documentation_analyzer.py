
import google.generativeai as genai
import os
from .readability_analyzer import ReadabilityAnalyzer
from .structure_analyzer import StructureAnalyzer
from .completeness_analyzer import CompletenessAnalyzer
from .style_analyzer import StyleAnalyzer
from utils.logger import get_logger

class DocumentationAnalyzer:
    """Main documentation analyzer that coordinates all analysis components"""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Configure Gemini API
        api_key = "AIzaSyBMcgjfVB2hpHX-cBdBqdpiw5qpf9Rsb3U"
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize analyzers
        self.readability_analyzer = ReadabilityAnalyzer(self.model)
        self.structure_analyzer = StructureAnalyzer(self.model)
        self.completeness_analyzer = CompletenessAnalyzer(self.model)
        self.style_analyzer = StyleAnalyzer(self.model)
    
    def analyze_document(self, scraped_data):
        """Perform comprehensive analysis of scraped documentation"""
        
        self.logger.info("Starting comprehensive document analysis...")
        
        try:
            # Extract basic information
            url = scraped_data.get('url', '')
            title = scraped_data.get('title', '')
            content = scraped_data.get('content', '')
            
            self.logger.info(f"Analyzing document: {title}")
            self.logger.info(f"Content length: {len(content)} characters")
            
            # Perform individual analyses
            self.logger.info("Analyzing readability...")
            readability_result = self.readability_analyzer.analyze(scraped_data)
            
            self.logger.info("Analyzing structure...")
            structure_result = self.structure_analyzer.analyze(scraped_data)
            
            self.logger.info("Analyzing completeness...")
            completeness_result = self.completeness_analyzer.analyze(scraped_data)
            
            self.logger.info("Analyzing style...")
            style_result = self.style_analyzer.analyze(scraped_data)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(
                readability_result, structure_result, 
                completeness_result, style_result
            )
            
            # Compile final analysis result
            analysis_result = {
                'document_info': {
                    'url': url,
                    'title': title,
                    'word_count': len(content.split()),
                    'character_count': len(content),
                    'analyzed_at': scraped_data.get('scraped_at')
                },
                'readability': readability_result,
                'structure': structure_result,
                'completeness': completeness_result,
                'style': style_result,
                'overall_score': overall_score,
                'summary': self._generate_summary(
                    readability_result, structure_result, 
                    completeness_result, style_result
                )
            }
            
            self.logger.info(f"✅ Analysis complete. Overall score: {overall_score}")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            return {
                'error': str(e),
                'document_info': {
                    'url': scraped_data.get('url', ''),
                    'title': scraped_data.get('title', ''),
                }
            }
    
    def _calculate_overall_score(self, readability, structure, completeness, style):
        """Calculate weighted overall score from individual analysis scores"""
        
        try:
            scores = []
            weights = []
            
            # Readability (25% weight)
            if 'score' in readability:
                scores.append(readability['score'])
                weights.append(0.25)
            
            # Structure (25% weight)
            if 'score' in structure:
                scores.append(structure['score'])
                weights.append(0.25)
            
            # Completeness (25% weight)
            if 'score' in completeness:
                scores.append(completeness['score'])
                weights.append(0.25)
            
            # Style (25% weight)
            if 'score' in style:
                scores.append(style['score'])
                weights.append(0.25)
            
            if scores:
                weighted_score = sum(score * weight for score, weight in zip(scores, weights))
                return round(weighted_score / sum(weights), 1)
            else:
                return 0.0
                
        except Exception:
            return 0.0
    
    def _generate_summary(self, readability, structure, completeness, style):
        """Generate executive summary of the analysis"""
        
        summary = {
            'strengths': [],
            'weaknesses': [],
            'priority_improvements': [],
            'recommendation': ''
        }
        
        try:
            # Identify strengths
            if readability.get('score', 0) >= 7:
                summary['strengths'].append("Good readability for target audience")
            
            if structure.get('score', 0) >= 7:
                summary['strengths'].append("Well-organized document structure")
            
            if completeness.get('score', 0) >= 7:
                summary['strengths'].append("Comprehensive information coverage")
            
            if style.get('score', 0) >= 7:
                summary['strengths'].append("Adherence to style guidelines")
            
            # Identify weaknesses and priority improvements
            analysis_areas = [
                ('readability', readability, "Improve readability for marketers"),
                ('structure', structure, "Enhance document structure and flow"),
                ('completeness', completeness, "Add missing information and examples"),
                ('style', style, "Improve writing style and tone")
            ]
            
            for area_name, area_result, improvement in analysis_areas:
                score = area_result.get('score', 0)
                if score < 6:
                    summary['weaknesses'].append(f"Poor {area_name} (score: {score})")
                    summary['priority_improvements'].append(improvement)
                elif score < 7:
                    summary['priority_improvements'].append(improvement)
            
            # Generate overall recommendation
            overall_score = self._calculate_overall_score(readability, structure, completeness, style)
            
            if overall_score >= 8:
                summary['recommendation'] = "Excellent documentation with minor improvements needed"
            elif overall_score >= 7:
                summary['recommendation'] = "Good documentation with some areas for improvement"
            elif overall_score >= 6:
                summary['recommendation'] = "Adequate documentation requiring moderate improvements"
            else:
                summary['recommendation'] = "Documentation needs significant improvements across multiple areas"
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            summary['recommendation'] = "Unable to generate summary due to analysis errors"
        
        return summary
