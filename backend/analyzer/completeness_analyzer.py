
import re
from utils.logger import get_logger

class CompletenessAnalyzer:
    """Analyzes content completeness and coverage"""
    
    def __init__(self, gemini_model):
        self.logger = get_logger(__name__)
        self.model = gemini_model
    
    def analyze(self, scraped_data):
        """Comprehensive completeness analysis"""
        
        try:
            content = scraped_data.get('content', '')
            code_blocks = scraped_data.get('code_blocks', [])
            images = scraped_data.get('images', [])
            links = scraped_data.get('links', [])
            lists = scraped_data.get('lists', [])
            
            # Analyze examples and illustrations
            example_analysis = self._analyze_examples(content, code_blocks, images)
            
            # Analyze instructional completeness
            instruction_analysis = self._analyze_instructions(content, lists)
            
            # Analyze information depth
            depth_analysis = self._analyze_information_depth(content)
            
            # Analyze supporting materials
            support_analysis = self._analyze_supporting_materials(code_blocks, images, links)
            
            # LLM-based completeness analysis
            llm_analysis = self._analyze_completeness_with_llm(content)
            
            # Generate suggestions
            suggestions = self._generate_completeness_suggestions(
                example_analysis, instruction_analysis, depth_analysis, support_analysis
            )
            
            # Calculate completeness score
            score = self._calculate_completeness_score(
                example_analysis, instruction_analysis, depth_analysis, support_analysis
            )
            
            return {
                'score': score,
                'example_analysis': example_analysis,
                'instruction_analysis': instruction_analysis,
                'depth_analysis': depth_analysis,
                'support_analysis': support_analysis,
                'llm_analysis': llm_analysis,
                'suggestions': suggestions,
                'summary': self._generate_completeness_summary(score, suggestions)
            }
            
        except Exception as e:
            self.logger.error(f"Error in completeness analysis: {str(e)}")
            return {
                'score': 0,
                'error': str(e),
                'suggestions': ["Unable to analyze completeness due to processing error"]
            }
    
    def _analyze_examples(self, content, code_blocks, images):
        """Analyze presence and quality of examples"""
        
        # Look for example indicators in text
        example_keywords = [
            'example', 'for example', 'for instance', 'such as', 'like this',
            'sample', 'demonstration', 'illustration', 'case study'
        ]
        
        content_lower = content.lower()
        example_mentions = sum(content_lower.count(keyword) for keyword in example_keywords)
        
        # Analyze code examples
        code_example_analysis = {
            'total_code_blocks': len(code_blocks),
            'inline_code': sum(1 for cb in code_blocks if cb.get('type') == 'inline'),
            'block_code': sum(1 for cb in code_blocks if cb.get('type') == 'block'),
            'has_code_examples': len(code_blocks) > 0
        }
        
        # Analyze visual examples
        visual_example_analysis = {
            'total_images': len(images),
            'images_with_alt': sum(1 for img in images if img.get('alt')),
            'has_visual_examples': len(images) > 0
        }
        
        # Determine example quality
        example_quality = self._determine_example_quality(
            example_mentions, code_blocks, images, content
        )
        
        return {
            'example_mentions': example_mentions,
            'code_examples': code_example_analysis,
            'visual_examples': visual_example_analysis,
            'example_quality': example_quality,
            'has_practical_examples': example_mentions > 0 or len(code_blocks) > 0
        }
    
    def _analyze_instructions(self, content, lists):
        """Analyze clarity and completeness of instructions"""
        
        # Look for instructional language
        instruction_keywords = [
            'step', 'click', 'select', 'choose', 'enter', 'type', 'navigate',
            'open', 'close', 'save', 'create', 'delete', 'configure', 'set up'
        ]
        
        content_lower = content.lower()
        instruction_count = sum(content_lower.count(keyword) for keyword in instruction_keywords)
        
        # Analyze step-by-step instructions
        step_patterns = [
            r'step \d+', r'\d+\.', r'first[,\s]', r'second[,\s]', r'third[,\s]',
            r'then[,\s]', r'next[,\s]', r'finally[,\s]', r'lastly[,\s]'
        ]
        
        step_indicators = sum(len(re.findall(pattern, content_lower)) for pattern in step_patterns)
        has_clear_steps = step_indicators > 2
        
        # Analyze procedural lists
        procedural_lists = 0
        for list_item in lists:
            if list_item.get('type') == 'ordered':
                procedural_lists += 1
        
        return {
            'instruction_word_count': instruction_count,
            'step_indicators': step_indicators,
            'has_clear_steps': has_clear_steps,
            'procedural_lists': procedural_lists,
            'instruction_density': instruction_count / len(content.split()) if content.split() else 0
        }
    
    def _analyze_information_depth(self, content):
        """Analyze depth and comprehensiveness of information"""
        
        # Look for depth indicators
        depth_keywords = [
            'why', 'how', 'what', 'when', 'where', 'because', 'reason',
            'purpose', 'benefit', 'advantage', 'important', 'note', 'warning',
            'tip', 'remember', 'consider', 'alternatively', 'option'
        ]
        
        content_lower = content.lower()
        depth_indicators = sum(content_lower.count(keyword) for keyword in depth_keywords)
        
        # Analyze explanatory content
        explanation_patterns = [
            r'this is because', r'the reason', r'in order to', r'so that',
            r'this means', r'in other words', r'specifically', r'particularly'
        ]
        
        explanations = sum(len(re.findall(pattern, content_lower)) for pattern in explanation_patterns)
        
        # Look for prerequisite information
        prereq_keywords = ['prerequisite', 'requirement', 'before', 'first', 'ensure', 'make sure']
        prerequisites = sum(content_lower.count(keyword) for keyword in prereq_keywords)
        
        # Look for troubleshooting information
        troubleshoot_keywords = [
            'troubleshoot', 'problem', 'issue', 'error', 'fail', 'not working',
            'common issues', 'frequently asked', 'faq'
        ]
        troubleshooting = sum(content_lower.count(keyword) for keyword in troubleshoot_keywords)
        
        return {
            'depth_indicators': depth_indicators,
            'explanations': explanations,
            'has_prerequisites': prerequisites > 0,
            'has_troubleshooting': troubleshooting > 0,
            'information_richness': self._calculate_information_richness(
                depth_indicators, explanations, prerequisites, troubleshooting, content
            )
        }
    
    def _analyze_supporting_materials(self, code_blocks, images, links):
        """Analyze supporting materials and resources"""
        
        # Analyze code support
        code_support = {
            'has_code_examples': len(code_blocks) > 0,
            'code_variety': len(set(cb.get('language', 'unknown') for cb in code_blocks)),
            'well_commented_code': self._check_code_comments(code_blocks)
        }
        
        # Analyze visual support
        visual_support = {
            'has_images': len(images) > 0,
            'images_per_1000_words': len(images) / 1000,  # Approximate
            'descriptive_images': sum(1 for img in images if len(img.get('alt', '')) > 10)
        }
        
        # Analyze reference materials
        reference_support = {
            'total_links': len(links),
            'external_links': sum(1 for link in links if link.get('is_external')),
            'internal_links': sum(1 for link in links if not link.get('is_external')),
            'has_references': len(links) > 0
        }
        
        return {
            'code_support': code_support,
            'visual_support': visual_support,
            'reference_support': reference_support,
            'overall_support_quality': self._calculate_support_quality(
                code_support, visual_support, reference_support
            )
        }
    
    def _analyze_completeness_with_llm(self, content):
        """Use LLM to analyze content completeness"""
        
        prompt = f"""
        Analyze this documentation for completeness and comprehensiveness:

        Content: {content[:2000]}...

        Please evaluate:
        1. Does it provide enough detail for users to successfully implement/use the feature?
        2. Are there sufficient examples for different use cases?
        3. Are edge cases or potential issues addressed?
        4. Is there clear guidance on what to do next?
        5. Are prerequisites and dependencies clearly stated?
        6. What important information might be missing?

        Identify specific gaps and suggest what additional content should be included.
        Keep your response concise and actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error in LLM completeness analysis: {str(e)}")
            return "Unable to perform LLM-based completeness analysis due to API error"
    
    def _generate_completeness_suggestions(self, example_analysis, instruction_analysis, 
                                         depth_analysis, support_analysis):
        """Generate specific completeness improvement suggestions"""
        
        suggestions = []
        
        # Example suggestions
        if not example_analysis['has_practical_examples']:
            suggestions.append("Add practical examples to illustrate concepts and usage.")
        elif example_analysis['example_mentions'] < 2:
            suggestions.append("Include more diverse examples to cover different use cases.")
        
        if not example_analysis['code_examples']['has_code_examples']:
            if self._seems_technical_content(instruction_analysis):
                suggestions.append("Add code examples to support technical instructions.")
        
        # Instruction suggestions
        if not instruction_analysis['has_clear_steps']:
            suggestions.append("Provide clear step-by-step instructions for better guidance.")
        
        if instruction_analysis['instruction_density'] < 0.02:
            suggestions.append("Add more actionable instructions and clear next steps.")
        
        # Depth suggestions
        if not depth_analysis['has_prerequisites']:
            suggestions.append("Clearly state prerequisites and requirements before starting.")
        
        if not depth_analysis['has_troubleshooting']:
            suggestions.append("Add troubleshooting section for common issues and problems.")
        
        if depth_analysis['information_richness'] < 5:
            suggestions.append("Provide more detailed explanations and context for better understanding.")
        
        # Support material suggestions
        code_support = support_analysis['code_support']
        if not code_support['has_code_examples'] and self._seems_technical_content(instruction_analysis):
            suggestions.append("Include code examples for technical implementation.")
        
        visual_support = support_analysis['visual_support']
        if not visual_support['has_images']:
            suggestions.append("Add screenshots or diagrams to support explanations.")
        
        reference_support = support_analysis['reference_support']
        if not reference_support['has_references']:
            suggestions.append("Include links to related documentation and resources.")
        
        return suggestions
    
    def _determine_example_quality(self, example_mentions, code_blocks, images, content):
        """Determine overall quality of examples"""
        
        score = 0
        
        # Text examples
        if example_mentions > 0:
            score += 2
        if example_mentions > 2:
            score += 1
        
        # Code examples
        if len(code_blocks) > 0:
            score += 3
        if len(code_blocks) > 2:
            score += 1
        
        # Visual examples
        if len(images) > 0:
            score += 2
        
        # Variety bonus
        has_text_examples = example_mentions > 0
        has_code_examples = len(code_blocks) > 0
        has_visual_examples = len(images) > 0
        
        variety_count = sum([has_text_examples, has_code_examples, has_visual_examples])
        if variety_count >= 2:
            score += 1
        if variety_count == 3:
            score += 1
        
        return min(10, score)
    
    def _check_code_comments(self, code_blocks):
        """Check if code blocks have helpful comments"""
        
        if not code_blocks:
            return False
        
        comment_patterns = [r'//.*', r'/\*.*\*/', r'#.*', r'<!--.*-->']
        
        for code_block in code_blocks:
            code_text = code_block.get('text', '')
            for pattern in comment_patterns:
                if re.search(pattern, code_text):
                    return True
        
        return False
    
    def _calculate_information_richness(self, depth_indicators, explanations, 
                                      prerequisites, troubleshooting, content):
        """Calculate information richness score"""
        
        word_count = len(content.split())
        if word_count == 0:
            return 0
        
        # Normalize indicators by content length
        normalized_depth = (depth_indicators / word_count) * 1000
        normalized_explanations = (explanations / word_count) * 1000
        
        score = 0
        score += min(3, normalized_depth)  # Max 3 points for depth indicators
        score += min(2, normalized_explanations)  # Max 2 points for explanations
        score += 2 if prerequisites > 0 else 0  # 2 points for prerequisites
        score += 2 if troubleshooting > 0 else 0  # 2 points for troubleshooting
        score += 1 if word_count > 500 else 0  # 1 point for sufficient length
        
        return min(10, score)
    
    def _calculate_support_quality(self, code_support, visual_support, reference_support):
        """Calculate overall support material quality"""
        
        score = 5  # Base score
        
        # Code support
        if code_support['has_code_examples']:
            score += 1.5
        if code_support['well_commented_code']:
            score += 0.5
        
        # Visual support
        if visual_support['has_images']:
            score += 1.5
        if visual_support['descriptive_images'] > 0:
            score += 0.5
        
        # Reference support
        if reference_support['has_references']:
            score += 1
        if reference_support['external_links'] > 0:
            score += 0.5
        
        return min(10, score)
    
    def _seems_technical_content(self, instruction_analysis):
        """Determine if content seems technical based on instruction analysis"""
        
        return instruction_analysis['instruction_density'] > 0.01
    
    def _calculate_completeness_score(self, example_analysis, instruction_analysis, 
                                    depth_analysis, support_analysis):
        """Calculate overall completeness score"""
        
        try:
            # Weight different components
            example_score = example_analysis.get('example_quality', 0) * 0.25
            
            instruction_score = 7  # Start with good score
            if not instruction_analysis.get('has_clear_steps'):
                instruction_score -= 2
            if instruction_analysis.get('instruction_density', 0) < 0.02:
                instruction_score -= 1
            instruction_score *= 0.25
            
            depth_score = depth_analysis.get('information_richness', 0) * 0.25
            
            support_score = support_analysis.get('overall_support_quality', 0) * 0.25
            
            total_score = example_score + instruction_score + depth_score + support_score
            return max(0, min(10, round(total_score, 1)))
            
        except Exception:
            return 5.0  # Default middle score
    
    def _generate_completeness_summary(self, score, suggestions):
        """Generate completeness analysis summary"""
        
        if score >= 8:
            return f"Comprehensive documentation (score: {score}). Contains sufficient detail and examples."
        elif score >= 6:
            return f"Good completeness (score: {score}) with some gaps to address."
        elif score >= 4:
            return f"Moderate completeness (score: {score}). Significant improvements needed."
        else:
            return f"Incomplete documentation (score: {score}). Major additions required."
