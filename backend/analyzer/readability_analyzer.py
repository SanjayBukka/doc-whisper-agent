
import textstat
import re
from utils.logger import get_logger

class ReadabilityAnalyzer:
    """Analyzes document readability specifically for non-technical marketers"""
    
    def __init__(self, gemini_model):
        self.logger = get_logger(__name__)
        self.model = gemini_model
    
    def analyze(self, scraped_data):
        """Comprehensive readability analysis"""
        
        content = scraped_data.get('content', '')
        
        try:
            # Basic metrics
            basic_metrics = self._calculate_basic_metrics(content)
            
            # Advanced readability scores
            readability_scores = self._calculate_readability_scores(content)
            
            # Technical complexity analysis
            complexity_analysis = self._analyze_technical_complexity(content)
            
            # LLM-based marketer perspective analysis
            marketer_analysis = self._analyze_for_marketers(content)
            
            # Generate actionable suggestions
            suggestions = self._generate_readability_suggestions(
                basic_metrics, readability_scores, complexity_analysis
            )
            
            # Calculate overall readability score
            score = self._calculate_readability_score(readability_scores, complexity_analysis)
            
            return {
                'score': score,
                'basic_metrics': basic_metrics,
                'readability_scores': readability_scores,
                'complexity_analysis': complexity_analysis,
                'marketer_analysis': marketer_analysis,
                'suggestions': suggestions,
                'summary': self._generate_readability_summary(score, suggestions)
            }
            
        except Exception as e:
            self.logger.error(f"Error in readability analysis: {str(e)}")
            return {
                'score': 0,
                'error': str(e),
                'suggestions': ["Unable to analyze readability due to processing error"]
            }
    
    def _calculate_basic_metrics(self, content):
        """Calculate basic text metrics"""
        
        sentences = textstat.sentence_count(content)
        words = textstat.lexicon_count(content)
        syllables = textstat.syllable_count(content)
        
        return {
            'word_count': words,
            'sentence_count': sentences,
            'syllable_count': syllables,
            'avg_sentence_length': round(words / sentences, 1) if sentences > 0 else 0,
            'avg_syllables_per_word': round(syllables / words, 2) if words > 0 else 0,
            'character_count': len(content),
            'paragraph_count': len([p for p in content.split('\n\n') if p.strip()])
        }
    
    def _calculate_readability_scores(self, content):
        """Calculate various readability scores"""
        
        try:
            return {
                'flesch_reading_ease': round(textstat.flesch_reading_ease(content), 1),
                'flesch_kincaid_grade': round(textstat.flesch_kincaid_grade(content), 1),
                'gunning_fog': round(textstat.gunning_fog(content), 1),
                'coleman_liau': round(textstat.coleman_liau_index(content), 1),
                'automated_readability': round(textstat.automated_readability_index(content), 1),
                'smog_index': round(textstat.smog_index(content), 1)
            }
        except Exception as e:
            self.logger.warning(f"Error calculating readability scores: {str(e)}")
            return {
                'flesch_reading_ease': 0,
                'flesch_kincaid_grade': 0,
                'gunning_fog': 0,
                'coleman_liau': 0,
                'automated_readability': 0,
                'smog_index': 0
            }
    
    def _analyze_technical_complexity(self, content):
        """Analyze technical complexity for marketing audience"""
        
        # Technical terms commonly found in documentation
        technical_terms = [
            'api', 'sdk', 'json', 'xml', 'html', 'css', 'javascript', 'integration',
            'endpoint', 'authentication', 'authorization', 'webhook', 'callback',
            'parameter', 'payload', 'request', 'response', 'configuration',
            'implementation', 'deployment', 'initialization', 'instantiation'
        ]
        
        content_lower = content.lower()
        
        # Count technical terms
        tech_term_count = sum(content_lower.count(term) for term in technical_terms)
        tech_term_density = tech_term_count / len(content.split()) if content.split() else 0
        
        # Analyze jargon and complex phrases
        jargon_patterns = [
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+\.\w+\(\)',  # Method calls
            r'\b\w+\/\w+',      # Path-like patterns
            r'\{[^}]+\}',       # Code-like brackets
        ]
        
        jargon_count = sum(len(re.findall(pattern, content)) for pattern in jargon_patterns)
        
        return {
            'technical_term_count': tech_term_count,
            'technical_term_density': round(tech_term_density * 100, 2),
            'jargon_count': jargon_count,
            'complexity_level': self._determine_complexity_level(tech_term_density, jargon_count)
        }
    
    def _analyze_for_marketers(self, content):
        """Use LLM to analyze content from marketer perspective"""
        
        prompt = f"""
        Analyze this documentation content from a non-technical marketer's perspective:

        Content: {content[:2000]}...

        Please evaluate:
        1. How understandable is this for someone without technical background?
        2. Are technical concepts explained in business terms?
        3. What specific technical jargon might confuse marketers?
        4. Are there clear business benefits and use cases explained?
        5. Is the tone appropriate for a marketing audience?

        Provide specific examples and suggestions for improvement.
        Keep your response concise and actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {str(e)}")
            return "Unable to perform marketer-specific analysis due to API error"
    
    def _generate_readability_suggestions(self, basic_metrics, readability_scores, complexity_analysis):
        """Generate specific, actionable readability suggestions"""
        
        suggestions = []
        
        # Sentence length suggestions
        avg_sentence_length = basic_metrics.get('avg_sentence_length', 0)
        if avg_sentence_length > 25:
            suggestions.append(f"Average sentence length is {avg_sentence_length} words. Break long sentences into shorter ones (aim for 15-20 words).")
        elif avg_sentence_length > 20:
            suggestions.append(f"Some sentences are long ({avg_sentence_length} words average). Consider splitting complex sentences.")
        
        # Readability score suggestions
        flesch_score = readability_scores.get('flesch_reading_ease', 0)
        if flesch_score < 30:
            suggestions.append("Text is very difficult to read. Use simpler words and shorter sentences.")
        elif flesch_score < 50:
            suggestions.append("Text is fairly difficult. Simplify vocabulary and sentence structure.")
        elif flesch_score < 60:
            suggestions.append("Text readability is standard but could be improved for broader accessibility.")
        
        # Grade level suggestions
        grade_level = readability_scores.get('flesch_kincaid_grade', 0)
        if grade_level > 12:
            suggestions.append(f"Content requires college-level reading (grade {grade_level}). Simplify for broader audience.")
        elif grade_level > 10:
            suggestions.append(f"Content is at grade {grade_level} level. Consider simplifying for marketing audience.")
        
        # Technical complexity suggestions
        tech_density = complexity_analysis.get('technical_term_density', 0)
        if tech_density > 5:
            suggestions.append(f"High technical term density ({tech_density}%). Add definitions or explanations for technical concepts.")
        elif tech_density > 3:
            suggestions.append("Consider adding a glossary or inline explanations for technical terms.")
        
        # Specific improvement suggestions
        if complexity_analysis.get('jargon_count', 0) > 10:
            suggestions.append("Reduce technical jargon or provide clear explanations for marketing audience.")
        
        if basic_metrics.get('avg_syllables_per_word', 0) > 1.7:
            suggestions.append("Use shorter, simpler words when possible to improve readability.")
        
        return suggestions
    
    def _calculate_readability_score(self, readability_scores, complexity_analysis):
        """Calculate overall readability score (0-10)"""
        
        try:
            flesch_score = readability_scores.get('flesch_reading_ease', 0)
            grade_level = readability_scores.get('flesch_kincaid_grade', 20)
            tech_density = complexity_analysis.get('technical_term_density', 10)
            
            # Convert Flesch score to 0-10 scale
            flesch_normalized = max(0, min(10, flesch_score / 10))
            
            # Penalize high grade level
            grade_penalty = max(0, (grade_level - 8) * 0.5)
            
            # Penalize high technical density
            tech_penalty = tech_density * 0.3
            
            score = flesch_normalized - grade_penalty - tech_penalty
            return max(0, min(10, round(score, 1)))
            
        except Exception:
            return 5.0  # Default middle score
    
    def _determine_complexity_level(self, tech_density, jargon_count):
        """Determine overall complexity level"""
        
        if tech_density > 5 or jargon_count > 20:
            return "Very High"
        elif tech_density > 3 or jargon_count > 10:
            return "High"
        elif tech_density > 1 or jargon_count > 5:
            return "Moderate"
        else:
            return "Low"
    
    def _generate_readability_summary(self, score, suggestions):
        """Generate a summary of readability analysis"""
        
        if score >= 8:
            return f"Excellent readability (score: {score}). Content is well-suited for marketing audience."
        elif score >= 6:
            return f"Good readability (score: {score}) with room for improvement."
        elif score >= 4:
            return f"Moderate readability (score: {score}). Significant improvements needed."
        else:
            return f"Poor readability (score: {score}). Major revision required for marketing audience."
