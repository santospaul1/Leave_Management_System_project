from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from employee.models import Employee
from notification.models import Notification
from .forms import FeedbackForm
from .models import Feedback
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)
    if score['compound'] >= 0.05:
        return 'Positive'
    elif score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
    
@login_required
def provide_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()
    employee = Employee.objects.get(user=request.user)
    user_notifications = Notification.objects.filter(recipient=request.user, is_read = False).order_by('-timestamp')
    return render(request, 'feedback/provide_feedback.html', {'form': form, 'employee':employee, 'notifications':user_notifications})

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def thank_you(request):
    return render(request, 'feedback/thank_you.html')
