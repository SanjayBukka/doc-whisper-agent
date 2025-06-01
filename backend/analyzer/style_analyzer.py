
import re
from textstat import flesch_reading_ease
from utils.logger import get_logger

class StyleAnalyzer:
    """Analyzes writing style and adherence to style guidelines"""
    
    def __init__(self, gemini_model):
        self.logger = get_logger(__name__)
        self.model = gemini_model
    
    def analyze(self, scraped_data):
        """Comprehensive style analysis"""
        
        try:
            content = scraped_data.get('content', '')
            
            # Voice and tone analysis
            voice_analysis = self._analyze_voice_tone(content)
            
            # Clarity and conciseness analysis
            clarity_analysis = self._analyze_clarity(content)
            
            # Action-oriented language analysis
            action_analysis = self._analyze_action_language(content)
            
            # Consistency analysis
            consistency_analysis = self._analyze_consistency(content)
            
            # LLM-based style analysis
            llm_analysis = self._analyze_style_with_llm(content)
            
            # Generate suggestions
            suggestions = self._generate_style_suggestions(
                voice_analysis, clarity_analysis, action_analysis, consistency_analysis
            )
            
            # Calculate style score
            score = self._calculate_style_score(
                voice_analysis, clarity_analysis, action_analysis, consistency_analysis
            )
            
            return {
                'score': score,
                'voice_analysis': voice_analysis,
                'clarity_analysis': clarity_analysis,
                'action_analysis': action_analysis,
                'consistency_analysis': consistency_analysis,
                'llm_analysis': llm_analysis,
                'suggestions': suggestions,
                'summary': self._generate_style_summary(score, suggestions)
            }
            
        except Exception as e:
            self.logger.error(f"Error in style analysis: {str(e)}")
            return {
                'score': 0,
                'error': str(e),
                'suggestions': ["Unable to analyze style due to processing error"]
            }
    
    def _analyze_voice_tone(self, content):
        """Analyze voice and tone characteristics"""
        
        sentences = self._split_into_sentences(content)
        
        # Analyze passive vs active voice
        passive_count = self._count_passive_voice(sentences)
        passive_ratio = passive_count / len(sentences) if sentences else 0
        
        # Analyze sentence types
        sentence_analysis = self._analyze_sentence_types(sentences)
        
        # Analyze tone indicators
        tone_analysis = self._analyze_tone_indicators(content)
        
        # Analyze formality level
        formality_analysis = self._analyze_formality(content)
        
        return {
            'total_sentences': len(sentences),
            'passive_voice_count': passive_count,
            'passive_voice_ratio': round(passive_ratio, 3),
            'sentence_types': sentence_analysis,
            'tone_indicators': tone_analysis,
            'formality_level': formality_analysis,
            'voice_quality': self._determine_voice_quality(passive_ratio, tone_analysis)
        }
    
    def _analyze_clarity(self, content):
        """Analyze clarity and conciseness"""
        
        sentences = self._split_into_sentences(content)
        words = content.split()
        
        # Calculate basic metrics
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        # Analyze complex words
        complex_words = self._count_complex_words(words)
        complex_word_ratio = complex_words / len(words) if words else 0
        
        # Analyze filler words
        filler_analysis = self._analyze_filler_words(content)
        
        # Analyze sentence complexity
        complexity_analysis = self._analyze_sentence_complexity(sentences)
        
        # Calculate readability
        readability_score = flesch_reading_ease(content) if content else 0
        
        return {
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_word_length': round(avg_word_length, 1),
            'complex_words': complex_words,
            'complex_word_ratio': round(complex_word_ratio, 3),
            'filler_words': filler_analysis,
            'sentence_complexity': complexity_analysis,
            'readability_score': round(readability_score, 1),
            'clarity_grade': self._grade_clarity(avg_sentence_length, complex_word_ratio, readability_score)
        }
    
    def _analyze_action_language(self, content):
        """Analyze action-oriented and imperative language"""
        
        sentences = self._split_into_sentences(content)
        
        # Action verbs
        action_verbs = [
            'click', 'select', 'choose', 'enter', 'type', 'navigate', 'go',
            'open', 'close', 'save', 'create', 'add', 'remove', 'delete',
            'configure', 'set', 'enable', 'disable', 'start', 'stop',
            'install', 'download', 'upload', 'copy', 'paste', 'edit'
        ]
        
        content_lower = content.lower()
        action_verb_count = sum(content_lower.count(verb) for verb in action_verbs)
        
        # Imperative sentences (commands)
        imperative_count = self._count_imperative_sentences(sentences)
        imperative_ratio = imperative_count / len(sentences) if sentences else 0
        
        # User-focused language
        user_focus_analysis = self._analyze_user_focus(content)
        
        return {
            'action_verb_count': action_verb_count,
            'imperative_sentences': imperative_count,
            'imperative_ratio': round(imperative_ratio, 3),
            'user_focus': user_focus_analysis,
            'action_orientation': self._grade_action_orientation(action_verb_count, imperative_ratio, len(content.split()))
        }
    
    def _analyze_consistency(self, content):
        """Analyze style consistency"""
        
        # Analyze capitalization consistency
        capitalization_analysis = self._analyze_capitalization(content)
        
        # Analyze punctuation consistency
        punctuation_analysis = self._analyze_punctuation(content)
        
        # Analyze terminology consistency
        terminology_analysis = self._analyze_terminology(content)
        
        # Analyze formatting consistency
        formatting_analysis = self._analyze_formatting_consistency(content)
        
        return {
            'capitalization': capitalization_analysis,
            'punctuation': punctuation_analysis,
            'terminology': terminology_analysis,
            'formatting': formatting_analysis,
            'overall_consistency': self._calculate_consistency_score(
                capitalization_analysis, punctuation_analysis, terminology_analysis
            )
        }
    
    def _analyze_style_with_llm(self, content):
        """Use LLM to analyze writing style against guidelines"""
        
        prompt = f"""
        Analyze this documentation for writing style and adherence to professional style guidelines:

        Content: {content[:2000]}...

        Please evaluate based on Microsoft Style Guide principles:
        1. Voice and Tone: Is it customer-focused, clear, and professional?
        2. Clarity: Are sentences concise and easy to understand?
        3. Action-oriented: Does it guide users effectively with clear instructions?
        4. Consistency: Is the tone and style consistent throughout?
        5. Inclusivity: Is the language inclusive and accessible?

        Identify specific areas where the writing could be improved and provide concrete suggestions.
        Keep your response concise and actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Error in LLM style analysis: {str(e)}")
            return "Unable to perform LLM-based style analysis due to API error"
    
    def _split_into_sentences(self, content):
        """Split content into sentences"""
        
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
        return sentences
    
    def _count_passive_voice(self, sentences):
        """Count passive voice constructions"""
        
        passive_patterns = [
            r'\b(is|are|was|were|been|being)\s+\w*ed\b',
            r'\b(is|are|was|were|been|being)\s+\w*en\b',
            r'\b(get|gets|got|getting)\s+\w*ed\b'
        ]
        
        passive_count = 0
        for sentence in sentences:
            for pattern in passive_patterns:
                if re.search(pattern, sentence.lower()):
                    passive_count += 1
                    break  # Count each sentence only once
        
        return passive_count
    
    def _analyze_sentence_types(self, sentences):
        """Analyze distribution of sentence types"""
        
        declarative = 0
        interrogative = 0
        imperative = 0
        exclamatory = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence.endswith('?'):
                interrogative += 1
            elif sentence.endswith('!'):
                exclamatory += 1
            elif self._is_imperative(sentence):
                imperative += 1
            else:
                declarative += 1
        
        total = len(sentences)
        return {
            'declarative': declarative,
            'interrogative': interrogative,
            'imperative': imperative,
            'exclamatory': exclamatory,
            'declarative_ratio': declarative / total if total > 0 else 0,
            'interrogative_ratio': interrogative / total if total > 0 else 0,
            'imperative_ratio': imperative / total if total > 0 else 0,
            'exclamatory_ratio': exclamatory / total if total > 0 else 0
        }
    
    def _analyze_tone_indicators(self, content):
        """Analyze tone indicators in the content"""
        
        # Positive tone indicators
        positive_words = [
            'easy', 'simple', 'quick', 'efficient', 'helpful', 'useful',
            'convenient', 'smooth', 'seamless', 'intuitive', 'powerful'
        ]
        
        # Negative tone indicators
        negative_words = [
            'difficult', 'complex', 'complicated', 'hard', 'challenging',
            'confusing', 'problem', 'issue', 'error', 'fail', 'wrong'
        ]
        
        # Confident tone indicators
        confident_words = [
            'will', 'must', 'should', 'ensure', 'guarantee', 'definitely',
            'certainly', 'always', 'never', 'exactly'
        ]
        
        content_lower = content.lower()
        
        positive_count = sum(content_lower.count(word) for word in positive_words)
        negative_count = sum(content_lower.count(word) for word in negative_words)
        confident_count = sum(content_lower.count(word) for word in confident_words)
        
        return {
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'confident_indicators': confident_count,
            'tone_balance': positive_count - negative_count,
            'confidence_level': confident_count
        }
    
    def _analyze_formality(self, content):
        """Analyze formality level of the content"""
        
        # Formal indicators
        formal_words = [
            'utilize', 'commence', 'terminate', 'subsequently', 'furthermore',
            'nevertheless', 'therefore', 'consequently', 'accordingly'
        ]
        
        # Informal indicators
        informal_words = [
            'use', 'start', 'end', 'then', 'also', 'but', 'so', 'okay',
            'ok', 'yeah', 'yep', 'nope', 'gonna', 'wanna'
        ]
        
        # Contractions
        contractions = [
            "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't",
            "haven't", "hasn't", "hadn't", "couldn't", "wouldn't", "shouldn't"
        ]
        
        content_lower = content.lower()
        
        formal_count = sum(content_lower.count(word) for word in formal_words)
        informal_count = sum(content_lower.count(word) for word in informal_words)
        contraction_count = sum(content_lower.count(contraction) for contraction in contractions)
        
        formality_score = formal_count - informal_count - contraction_count
        
        if formality_score > 5:
            level = "Very Formal"
        elif formality_score > 0:
            level = "Formal"
        elif formality_score > -5:
            level = "Neutral"
        else:
            level = "Informal"
        
        return {
            'formal_words': formal_count,
            'informal_words': informal_count,
            'contractions': contraction_count,
            'formality_score': formality_score,
            'formality_level': level
        }
    
    def _count_complex_words(self, words):
        """Count complex words (3+ syllables)"""
        
        complex_count = 0
        for word in words:
            # Simple syllable counting
            syllables = self._count_syllables(word)
            if syllables >= 3:
                complex_count += 1
        
        return complex_count
    
    def _count_syllables(self, word):
        """Simple syllable counter"""
        
        word = word.lower().strip('.,!?;:"()[]{}')
        if not word:
            return 0
        
        vowels = "aeiouy"
        syllables = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllables += 1
            prev_was_vowel = is_vowel
        
        # Handle silent e
        if word.endswith('e') and syllables > 1:
            syllables -= 1
        
        return max(1, syllables)
    
    def _analyze_filler_words(self, content):
        """Analyze use of filler words"""
        
        filler_words = [
            'very', 'really', 'quite', 'rather', 'somewhat', 'fairly',
            'pretty', 'just', 'only', 'simply', 'actually', 'basically',
            'literally', 'obviously', 'clearly', 'certainly', 'definitely'
        ]
        
        content_lower = content.lower()
        filler_count = sum(content_lower.count(word) for word in filler_words)
        
        return {
            'total_fillers': filler_count,
            'filler_density': filler_count / len(content.split()) if content.split() else 0
        }
    
    def _analyze_sentence_complexity(self, sentences):
        """Analyze sentence complexity"""
        
        if not sentences:
            return {'avg_clauses': 0, 'complex_sentences': 0}
        
        complex_count = 0
        total_clauses = 0
        
        for sentence in sentences:
            # Count clauses by looking for conjunctions and relative pronouns
            clause_indicators = [
                'and', 'but', 'or', 'because', 'since', 'when', 'where',
                'while', 'although', 'though', 'if', 'unless', 'that', 'which', 'who'
            ]
            
            clause_count = 1  # Every sentence has at least one clause
            sentence_lower = sentence.lower()
            
            for indicator in clause_indicators:
                clause_count += sentence_lower.count(f' {indicator} ')
            
            total_clauses += clause_count
            
            if clause_count > 2:
                complex_count += 1
        
        return {
            'avg_clauses': round(total_clauses / len(sentences), 1),
            'complex_sentences': complex_count,
            'complexity_ratio': complex_count / len(sentences)
        }
    
    def _count_imperative_sentences(self, sentences):
        """Count imperative sentences"""
        
        imperative_count = 0
        
        for sentence in sentences:
            if self._is_imperative(sentence):
                imperative_count += 1
        
        return imperative_count
    
    def _is_imperative(self, sentence):
        """Check if a sentence is imperative"""
        
        imperative_starters = [
            'click', 'select', 'choose', 'enter', 'type', 'navigate', 'go',
            'open', 'close', 'save', 'create', 'add', 'remove', 'delete',
            'configure', 'set', 'enable', 'disable', 'make', 'ensure',
            'check', 'verify', 'confirm', 'install', 'download'
        ]
        
        words = sentence.lower().split()
        if words and words[0] in imperative_starters:
            return True
        
        return False
    
    def _analyze_user_focus(self, content):
        """Analyze user-focused language"""
        
        # User-focused pronouns
        user_pronouns = ['you', 'your', 'yours']
        # System-focused language
        system_pronouns = ['we', 'our', 'us', 'the system', 'the application']
        
        content_lower = content.lower()
        
        user_count = sum(content_lower.count(pronoun) for pronoun in user_pronouns)
        system_count = sum(content_lower.count(pronoun) for pronoun in system_pronouns)
        
        return {
            'user_pronouns': user_count,
            'system_pronouns': system_count,
            'user_focus_ratio': user_count / (user_count + system_count) if (user_count + system_count) > 0 else 0
        }
    
    def _analyze_capitalization(self, content):
        """Analyze capitalization consistency"""
        
        # This is a simplified analysis
        sentences = self._split_into_sentences(content)
        
        proper_caps = 0
        total_sentences = len(sentences)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence[0].isupper():
                proper_caps += 1
        
        return {
            'proper_sentence_caps': proper_caps,
            'total_sentences': total_sentences,
            'capitalization_rate': proper_caps / total_sentences if total_sentences > 0 else 0
        }
    
    def _analyze_punctuation(self, content):
        """Analyze punctuation consistency"""
        
        # Count different punctuation marks
        periods = content.count('.')
        commas = content.count(',')
        semicolons = content.count(';')
        colons = content.count(':')
        
        # Check for consistent list punctuation
        # This is a simplified check
        
        return {
            'periods': periods,
            'commas': commas,
            'semicolons': semicolons,
            'colons': colons,
            'punctuation_variety': len([x for x in [periods, commas, semicolons, colons] if x > 0])
        }
    
    def _analyze_terminology(self, content):
        """Analyze terminology consistency"""
        
        # Look for potential inconsistencies in common terms
        # This is a simplified analysis that could be expanded
        
        variations = [
            (['email', 'e-mail'], 'email_consistency'),
            (['website', 'web site'], 'website_consistency'),
            (['login', 'log in', 'log-in'], 'login_consistency'),
            (['setup', 'set up', 'set-up'], 'setup_consistency')
        ]
        
        consistency_issues = []
        content_lower = content.lower()
        
        for variation_list, issue_type in variations:
            found_variations = [var for var in variation_list if var in content_lower]
            if len(found_variations) > 1:
                consistency_issues.append({
                    'type': issue_type,
                    'variations_found': found_variations
                })
        
        return {
            'consistency_issues': consistency_issues,
            'issues_count': len(consistency_issues)
        }
    
    def _analyze_formatting_consistency(self, content):
        """Analyze formatting consistency"""
        
        # Look for consistent formatting patterns
        # This is a basic analysis
        
        # Check for consistent use of quotes
        single_quotes = content.count("'")
        double_quotes = content.count('"')
        
        # Check for consistent emphasis (simplified)
        bold_markers = content.count('**')
        italic_markers = content.count('*')
        
        return {
            'single_quotes': single_quotes,
            'double_quotes': double_quotes,
            'bold_markers': bold_markers,
            'italic_markers': italic_markers
        }
    
    def _determine_voice_quality(self, passive_ratio, tone_analysis):
        """Determine overall voice quality"""
        
        if passive_ratio < 0.1 and tone_analysis['tone_balance'] > 0:
            return "Excellent"
        elif passive_ratio < 0.2 and tone_analysis['tone_balance'] >= 0:
            return "Good"
        elif passive_ratio < 0.3:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _grade_clarity(self, avg_sentence_length, complex_word_ratio, readability_score):
        """Grade overall clarity"""
        
        clarity_score = 0
        
        # Sentence length scoring
        if avg_sentence_length <= 20:
            clarity_score += 3
        elif avg_sentence_length <= 25:
            clarity_score += 2
        elif avg_sentence_length <= 30:
            clarity_score += 1
        
        # Complex word ratio scoring
        if complex_word_ratio <= 0.1:
            clarity_score += 3
        elif complex_word_ratio <= 0.15:
            clarity_score += 2
        elif complex_word_ratio <= 0.2:
            clarity_score += 1
        
        # Readability score scoring
        if readability_score >= 70:
            clarity_score += 4
        elif readability_score >= 60:
            clarity_score += 3
        elif readability_score >= 50:
            clarity_score += 2
        elif readability_score >= 40:
            clarity_score += 1
        
        return min(10, clarity_score)
    
    def _grade_action_orientation(self, action_verb_count, imperative_ratio, word_count):
        """Grade action orientation"""
        
        if word_count == 0:
            return 0
        
        action_density = action_verb_count / word_count
        
        score = 0
        
        # Action verb density
        if action_density >= 0.02:
            score += 4
        elif action_density >= 0.015:
            score += 3
        elif action_density >= 0.01:
            score += 2
        elif action_density >= 0.005:
            score += 1
        
        # Imperative ratio
        if imperative_ratio >= 0.2:
            score += 4
        elif imperative_ratio >= 0.15:
            score += 3
        elif imperative_ratio >= 0.1:
            score += 2
        elif imperative_ratio >= 0.05:
            score += 1
        
        return min(10, score)
    
    def _calculate_consistency_score(self, capitalization, punctuation, terminology):
        """Calculate overall consistency score"""
        
        score = 7  # Start with good score
        
        # Capitalization consistency
        cap_rate = capitalization.get('capitalization_rate', 0)
        if cap_rate >= 0.9:
            score += 1
        elif cap_rate < 0.7:
            score -= 1
        
        # Terminology consistency
        issues_count = terminology.get('issues_count', 0)
        score -= issues_count * 0.5
        
        return max(0, min(10, score))
    
    def _generate_style_suggestions(self, voice_analysis, clarity_analysis, 
                                  action_analysis, consistency_analysis):
        """Generate specific style improvement suggestions"""
        
        suggestions = []
        
        # Voice and tone suggestions
        passive_ratio = voice_analysis.get('passive_voice_ratio', 0)
        if passive_ratio > 0.2:
            suggestions.append(f"Reduce passive voice usage ({passive_ratio:.1%}). Use active voice for clearer instructions.")
        
        tone_balance = voice_analysis['tone_indicators'].get('tone_balance', 0)
        if tone_balance < 0:
            suggestions.append("Use more positive language to create a helpful, encouraging tone.")
        
        # Clarity suggestions
        avg_sentence_length = clarity_analysis.get('avg_sentence_length', 0)
        if avg_sentence_length > 25:
            suggestions.append(f"Shorten sentences (current average: {avg_sentence_length} words). Aim for 15-20 words per sentence.")
        
        complex_ratio = clarity_analysis.get('complex_word_ratio', 0)
        if complex_ratio > 0.15:
            suggestions.append("Simplify complex words to improve readability for broader audience.")
        
        filler_density = clarity_analysis['filler_words'].get('filler_density', 0)
        if filler_density > 0.03:
            suggestions.append("Remove unnecessary filler words to make writing more concise.")
        
        # Action orientation suggestions
        imperative_ratio = action_analysis.get('imperative_ratio', 0)
        if imperative_ratio < 0.1:
            suggestions.append("Add more action-oriented language with clear imperatives (e.g., 'Click here', 'Enter your data').")
        
        user_focus_ratio = action_analysis['user_focus'].get('user_focus_ratio', 0)
        if user_focus_ratio < 0.5:
            suggestions.append("Use more user-focused language ('you', 'your') instead of system-focused language.")
        
        # Consistency suggestions
        issues_count = consistency_analysis['terminology'].get('issues_count', 0)
        if issues_count > 0:
            suggestions.append("Maintain consistent terminology throughout the document.")
        
        return suggestions
    
    def _calculate_style_score(self, voice_analysis, clarity_analysis, 
                             action_analysis, consistency_analysis):
        """Calculate overall style score"""
        
        try:
            # Voice score (25% weight)
            voice_quality = voice_analysis.get('voice_quality', 'Fair')
            voice_score = {'Excellent': 10, 'Good': 8, 'Fair': 6, 'Needs Improvement': 4}.get(voice_quality, 5)
            
            # Clarity score (30% weight)
            clarity_score = clarity_analysis.get('clarity_grade', 5)
            
            # Action orientation score (25% weight)
            action_score = action_analysis.get('action_orientation', 5)
            
            # Consistency score (20% weight)
            consistency_score = consistency_analysis.get('overall_consistency', 5)
            
            # Calculate weighted average
            total_score = (voice_score * 0.25 + clarity_score * 0.30 + 
                          action_score * 0.25 + consistency_score * 0.20)
            
            return round(total_score, 1)
            
        except Exception:
            return 5.0  # Default middle score
    
    def _generate_style_summary(self, score, suggestions):
        """Generate style analysis summary"""
        
        if score >= 8:
            return f"Excellent writing style (score: {score}). Professional and clear communication."
        elif score >= 6:
            return f"Good writing style (score: {score}) with room for improvement."
        elif score >= 4:
            return f"Adequate style (score: {score}) but needs significant improvements."
        else:
            return f"Poor writing style (score: {score}). Major revisions needed."
