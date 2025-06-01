
import re
from utils.logger import get_logger

class StructureAnalyzer:
    """Analyzes document structure and information flow"""
    
    def __init__(self, gemini_model):
        self.logger = get_logger(__name__)
        self.model = gemini_model
    
    def analyze(self, scraped_data):
        """Comprehensive structure analysis"""
        
        try:
            content = scraped_data.get('content', '')
            headings = scraped_data.get('headings', [])
            paragraphs = scraped_data.get('paragraphs', [])
            lists = scraped_data.get('lists', [])
            
            # Analyze heading structure
            heading_analysis = self._analyze_headings(headings)
            
            # Analyze paragraph structure
            paragraph_analysis = self._analyze_paragraphs(paragraphs, content)
            
            # Analyze information flow
            flow_analysis = self._analyze_information_flow(content, headings)
            
            # Analyze document organization
            organization_analysis = self._analyze_organization(headings, lists, paragraphs)
            
            # LLM-based structure analysis
            llm_analysis = self._analyze_structure_with_llm(content, headings)
            
            # Generate suggestions
            suggestions = self._generate_structure_suggestions(
                heading_analysis, paragraph_analysis, organization_analysis
            )
            
            # Calculate structure score
            score = self._calculate_structure_score(
                heading_analysis, paragraph_analysis, organization_analysis
            )
            
            return {
                'score': score,
                'heading_analysis': heading_analysis,
                'paragraph_analysis': paragraph_analysis,
                'flow_analysis': flow_analysis,
                'organization_analysis': organization_analysis,
                'llm_analysis': llm_analysis,
                'suggestions': suggestions,
                'summary': self._generate_structure_summary(score, suggestions)
            }
            
        except Exception as e:
            self.logger.error(f"Error in structure analysis: {str(e)}")
            return {
                'score': 0,
                'error': str(e),
                'suggestions': ["Unable to analyze structure due to processing error"]
            }
    
    def _analyze_headings(self, headings):
        """Analyze heading hierarchy and structure"""
        
        if not headings:
            return {
                'total_headings': 0,
                'levels_used': [],
                'hierarchy_score': 0,
                'has_gaps': True,
                'max_gap': 0,
                'distribution': {}
            }
        
        levels = [h['level'] for h in headings]
        unique_levels = sorted(set(levels))
        
        # Check for gaps in hierarchy (e.g., H1 -> H3 without H2)
        gaps = []
        max_gap = 0
        for i in range(len(unique_levels) - 1):
            gap = unique_levels[i + 1] - unique_levels[i]
            if gap > 1:
                gaps.append((unique_levels[i], unique_levels[i + 1]))
                max_gap = max(max_gap, gap)
        
        # Analyze heading distribution
        distribution = {}
        for level in range(1, 7):
            count = sum(1 for h in headings if h['level'] == level)
            if count > 0:
                distribution[f'h{level}'] = count
        
        # Calculate hierarchy score
        hierarchy_score = self._calculate_hierarchy_score(levels, gaps)
        
        return {
            'total_headings': len(headings),
            'levels_used': unique_levels,
            'hierarchy_score': hierarchy_score,
            'has_gaps': len(gaps) > 0,
            'max_gap': max_gap,
            'gaps': gaps,
            'distribution': distribution,
            'headings_per_1000_words': len(headings) / (len(' '.join([h['text'] for h in headings]).split()) / 1000) if headings else 0
        }
    
    def _analyze_paragraphs(self, paragraphs, content):
        """Analyze paragraph structure and length"""
        
        if not paragraphs:
            # Fallback: split content by double newlines
            para_texts = [p.strip() for p in content.split('\n\n') if p.strip()]
            paragraphs = [{'text': p, 'word_count': len(p.split())} for p in para_texts]
        
        if not paragraphs:
            return {
                'total_paragraphs': 0,
                'avg_length': 0,
                'length_distribution': {},
                'long_paragraphs': 0,
                'short_paragraphs': 0
            }
        
        word_counts = [p.get('word_count', len(p.get('text', '').split())) for p in paragraphs]
        avg_length = sum(word_counts) / len(word_counts) if word_counts else 0
        
        # Categorize paragraphs by length
        short_paragraphs = sum(1 for count in word_counts if count < 20)
        medium_paragraphs = sum(1 for count in word_counts if 20 <= count <= 100)
        long_paragraphs = sum(1 for count in word_counts if count > 100)
        very_long_paragraphs = sum(1 for count in word_counts if count > 200)
        
        return {
            'total_paragraphs': len(paragraphs),
            'avg_length': round(avg_length, 1),
            'length_distribution': {
                'short': short_paragraphs,
                'medium': medium_paragraphs,
                'long': long_paragraphs,
                'very_long': very_long_paragraphs
            },
            'long_paragraphs': long_paragraphs,
            'short_paragraphs': short_paragraphs,
            'word_counts': word_counts
        }
    
    def _analyze_information_flow(self, content, headings):
        """Analyze logical flow of information"""
        
        # Look for flow indicators
        transition_words = [
            'first', 'second', 'third', 'next', 'then', 'finally', 'lastly',
            'however', 'therefore', 'furthermore', 'moreover', 'additionally',
            'in contrast', 'on the other hand', 'as a result', 'consequently'
        ]
        
        content_lower = content.lower()
        transition_count = sum(content_lower.count(word) for word in transition_words)
        
        # Look for logical progression indicators
        step_indicators = ['step 1', 'step 2', '1.', '2.', '3.', 'first step', 'next step']
        has_steps = any(indicator in content_lower for indicator in step_indicators)
        
        # Analyze heading progression
        heading_flow_score = self._analyze_heading_flow(headings)
        
        return {
            'transition_word_count': transition_count,
            'has_clear_steps': has_steps,
            'heading_flow_score': heading_flow_score,
            'flow_quality': self._determine_flow_quality(transition_count, has_steps, heading_flow_score)
        }
    
    def _analyze_organization(self, headings, lists, paragraphs):
        """Analyze overall document organization"""
        
        # Calculate content density
        total_content_blocks = len(headings) + len(lists) + len(paragraphs)
        
        # Check for introduction and conclusion
        has_intro = self._has_introduction(headings)
        has_conclusion = self._has_conclusion(headings)
        
        # Analyze list usage
        list_analysis = {
            'total_lists': len(lists),
            'unordered_lists': sum(1 for l in lists if l.get('type') == 'unordered'),
            'ordered_lists': sum(1 for l in lists if l.get('type') == 'ordered'),
            'avg_items_per_list': sum(l.get('item_count', 0) for l in lists) / len(lists) if lists else 0
        }
        
        return {
            'total_content_blocks': total_content_blocks,
            'has_introduction': has_intro,
            'has_conclusion': has_conclusion,
            'list_analysis': list_analysis,
            'organization_score': self._calculate_organization_score(
                has_intro, has_conclusion, len(lists), len(headings)
            )
        }
    
    def _analyze_structure_with_llm(self, content, headings):
        """Use LLM to analyze document structure and flow"""
        
        # Prepare heading structure for analysis
        heading_structure = ""
        for heading in headings[:10]:  # Limit to first 10 headings
            indent = "  " * (heading['level'] - 1)
            heading_structure += f"{indent}H{heading['level']}: {heading['text']}\n"
        
        prompt = f"""
        Analyze the structure and flow of this documentation:

        Heading Structure:
        {heading_structure}

        Content Preview: {content[:1500]}...

        Please evaluate:
        1. Is the document well-organized with clear sections?
        2. Does information flow logically from general to specific?
        3. Are headings descriptive and helpful for navigation?
        4. Is the content scannable and easy to find information?
        5. Are there clear transitions between sections?

        Provide specific suggestions for structural improvements.
        Keep your response concise and actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error in LLM structure analysis: {str(e)}")
            return "Unable to perform LLM-based structure analysis due to API error"
    
    def _generate_structure_suggestions(self, heading_analysis, paragraph_analysis, organization_analysis):
        """Generate specific structure improvement suggestions"""
        
        suggestions = []
        
        # Heading suggestions
        if heading_analysis['total_headings'] < 3:
            suggestions.append("Add more headings to break up content and improve scannability.")
        
        if heading_analysis['has_gaps']:
            suggestions.append("Fix heading hierarchy gaps (e.g., don't skip from H1 to H3 without H2).")
        
        if heading_analysis['max_gap'] > 2:
            suggestions.append("Maintain consistent heading hierarchy - avoid skipping multiple heading levels.")
        
        # Paragraph suggestions
        avg_para_length = paragraph_analysis.get('avg_length', 0)
        if avg_para_length > 120:
            suggestions.append(f"Average paragraph length is {avg_para_length} words. Break into shorter paragraphs (aim for 50-100 words).")
        
        long_paras = paragraph_analysis.get('long_paragraphs', 0)
        total_paras = paragraph_analysis.get('total_paragraphs', 1)
        if long_paras / total_paras > 0.3:
            suggestions.append("Many paragraphs are too long. Break them into focused, shorter paragraphs.")
        
        # Organization suggestions
        if not organization_analysis.get('has_introduction'):
            suggestions.append("Add a clear introduction section to orient readers.")
        
        if not organization_analysis.get('has_conclusion'):
            suggestions.append("Consider adding a summary or conclusion section.")
        
        list_count = organization_analysis['list_analysis']['total_lists']
        if list_count == 0:
            suggestions.append("Use bullet points or numbered lists to break up text and improve readability.")
        
        return suggestions
    
    def _calculate_hierarchy_score(self, levels, gaps):
        """Calculate heading hierarchy quality score"""
        
        if not levels:
            return 0
        
        # Base score for having headings
        score = 5
        
        # Bonus for starting with H1
        if min(levels) == 1:
            score += 2
        
        # Penalty for gaps
        score -= len(gaps) * 1.5
        
        # Bonus for good distribution
        unique_levels = len(set(levels))
        if 2 <= unique_levels <= 4:
            score += 2
        elif unique_levels > 4:
            score -= 1
        
        return max(0, min(10, round(score, 1)))
    
    def _analyze_heading_flow(self, headings):
        """Analyze the logical flow of headings"""
        
        if len(headings) < 2:
            return 5  # Neutral score for insufficient data
        
        # Look for logical progression
        flow_score = 7  # Start with good score
        
        # Check for consistent level usage
        levels = [h['level'] for h in headings]
        if len(set(levels)) > 4:
            flow_score -= 1  # Too many heading levels
        
        # Check for abrupt level changes
        for i in range(len(levels) - 1):
            level_jump = abs(levels[i + 1] - levels[i])
            if level_jump > 2:
                flow_score -= 0.5
        
        return max(0, min(10, flow_score))
    
    def _determine_flow_quality(self, transition_count, has_steps, heading_flow_score):
        """Determine overall information flow quality"""
        
        score = heading_flow_score
        
        # Bonus for transition words
        if transition_count > 5:
            score += 1
        
        # Bonus for clear steps
        if has_steps:
            score += 1
        
        score = max(0, min(10, score))
        
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        elif score >= 4:
            return "Fair"
        else:
            return "Poor"
    
    def _has_introduction(self, headings):
        """Check if document has an introduction section"""
        
        intro_terms = ['introduction', 'overview', 'getting started', 'about']
        for heading in headings[:3]:  # Check first 3 headings
            heading_text = heading['text'].lower()
            if any(term in heading_text for term in intro_terms):
                return True
        return False
    
    def _has_conclusion(self, headings):
        """Check if document has a conclusion section"""
        
        conclusion_terms = ['conclusion', 'summary', 'next steps', 'what\'s next']
        for heading in headings[-3:]:  # Check last 3 headings
            heading_text = heading['text'].lower()
            if any(term in heading_text for term in conclusion_terms):
                return True
        return False
    
    def _calculate_organization_score(self, has_intro, has_conclusion, list_count, heading_count):
        """Calculate overall organization score"""
        
        score = 5  # Base score
        
        if has_intro:
            score += 1.5
        if has_conclusion:
            score += 1.5
        if list_count > 0:
            score += 1
        if heading_count >= 3:
            score += 1
        if heading_count >= 5:
            score += 0.5
        
        return max(0, min(10, round(score, 1)))
    
    def _calculate_structure_score(self, heading_analysis, paragraph_analysis, organization_analysis):
        """Calculate overall structure score"""
        
        try:
            # Weight different components
            hierarchy_score = heading_analysis.get('hierarchy_score', 0) * 0.3
            organization_score = organization_analysis.get('organization_score', 0) * 0.3
            
            # Paragraph score based on length distribution
            para_score = 7  # Start with good score
            avg_length = paragraph_analysis.get('avg_length', 0)
            if avg_length > 150:
                para_score -= 2
            elif avg_length > 100:
                para_score -= 1
            para_score *= 0.4
            
            total_score = hierarchy_score + organization_score + para_score
            return max(0, min(10, round(total_score, 1)))
            
        except Exception:
            return 5.0  # Default middle score
    
    def _generate_structure_summary(self, score, suggestions):
        """Generate structure analysis summary"""
        
        if score >= 8:
            return f"Excellent document structure (score: {score}). Well-organized and easy to navigate."
        elif score >= 6:
            return f"Good structure (score: {score}) with some areas for improvement."
        elif score >= 4:
            return f"Adequate structure (score: {score}) but needs significant improvements."
        else:
            return f"Poor structure (score: {score}). Major reorganization needed."
