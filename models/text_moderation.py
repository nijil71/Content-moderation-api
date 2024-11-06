# models/text_moderation.py
from transformers import pipeline
import torch

class TextModerator:
    def __init__(self):
        # Initialize toxic content detection
        self.toxic_classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Initialize sentiment analysis
        self.sentiment_classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )
    
    def _check_spam_indicators(self, text):
        """
        Basic rule-based spam detection
        """
        text = text.lower()
        spam_indicators = {
            'spam_score': 0,
            'reasons': []
        }
        
        # Check for common spam indicators
        spam_phrases = [
            'click here', 'act now', 'limited time', 'buy now', 'free offer',
            'guaranteed', 'no obligation', 'winner', 'congratulations you won',
            'money back', 'order now', 'while supplies last'
        ]
        
        # Check for excessive capitalization
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        if caps_ratio > 0.5:
            spam_indicators['spam_score'] += 0.5
            spam_indicators['reasons'].append('Excessive capitalization')
        
        # Check for spam phrases
        for phrase in spam_phrases:
            if phrase in text:
                spam_indicators['spam_score'] += 0.3
                spam_indicators['reasons'].append(f'Contains spam phrase: {phrase}')
        
        # Check for repeated punctuation
        if '!!!' in text or '???' in text:
            spam_indicators['spam_score'] += 0.2
            spam_indicators['reasons'].append('Repeated punctuation')
        
        # Normalize score to be between 0 and 1
        spam_indicators['spam_score'] = min(1.0, spam_indicators['spam_score'])
        
        return spam_indicators
    
    def analyze(self, text):
        # Get toxic content prediction
        toxic_result = self.toxic_classifier(text)[0]
        
        # Get sentiment prediction
        sentiment_result = self.sentiment_classifier(text)[0]
        
        # Get spam indicators
        spam_result = self._check_spam_indicators(text)
        
        # Determine if content is toxic based on score threshold
        is_toxic = toxic_result['label'] == 'toxic' and toxic_result['score'] > 0.7
        
        return {
            'toxic': {
                'label': 'toxic' if is_toxic else 'non-toxic',
                'score': round(toxic_result['score'], 4)
            },
            'sentiment': {
                'label': sentiment_result['label'],
                'score': round(sentiment_result['score'], 4)
            },
            'spam': {
                'score': round(spam_result['spam_score'], 4),
                'is_spam': spam_result['spam_score'] > 0.5,
                'reasons': spam_result['reasons']
            },
            'moderation_result': {
                'is_flagged': (
                    is_toxic or 
                    spam_result['spam_score'] > 0.5
                ),
                'reason': 'Content contains inappropriate material' if is_toxic
                         else 'Content appears to be spam' if spam_result['spam_score'] > 0.5
                         else 'Content appears to be safe'
            },
            'text': text
        }

    def _get_detailed_toxicity(self, text):
        """
        Get detailed toxicity analysis for debugging purposes
        """
        result = self.toxic_classifier(text)[0]
        return {
            'raw_label': result['label'],
            'raw_score': result['score'],
            'analysis': {
                'high_confidence': result['score'] > 0.7,
                'medium_confidence': 0.3 < result['score'] <= 0.7,
                'low_confidence': result['score'] <= 0.3
            }
        }