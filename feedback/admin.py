from django.contrib import admin

from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at', 'sentiment_polarity', 'sentiment_subjectivity')
    search_fields = ('user__username', 'comment')

admin.site.register(Feedback, FeedbackAdmin)