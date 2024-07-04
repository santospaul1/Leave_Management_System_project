
from django.db import models
from django.contrib.auth.models import User
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Ensure the VADER lexicon is downloaded
nltk.download('vader_lexicon')

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment_polarity = models.FloatField(null=True, blank=True)
    sentiment_subjectivity = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(self.comment)
        self.sentiment_polarity = sentiment['compound']
        
        # Use TextBlob for subjectivity
        analysis = TextBlob(self.comment)
        self.sentiment_subjectivity = analysis.sentiment.subjectivity
        
        super().save(*args, **kwargs)

    def get_sentiment_category(self):
        if self.sentiment_polarity is None:
            return "Unknown"
        if self.sentiment_polarity > 0.05:
            return "Positive"
        elif self.sentiment_polarity < -0.05:
            return "Negative"
        else:
            return "Neutral"

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.created_at}"
