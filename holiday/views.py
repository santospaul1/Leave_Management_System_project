# in views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Holiday
from .forms import HolidayForm

@login_required
def add_holiday(request):
    holidays = Holiday.objects.all()
    if request.method == "POST":
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')
    else:
        form = HolidayForm()
    return render(request, 'holidays/add_holiday.html', {'holidays': holidays, 'form': form})



@login_required
def holiday_list(request):
    holidays = Holiday.objects.all()
    
    return render(request, 'holidays/holiday_list.html', {'holidays':holidays})

@login_required
def edit_holiday(request, holiday_id):
    holiday = get_object_or_404(Holiday, id=holiday_id)
    
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')  # Redirect to the list of holidays or another appropriate page
    else:
        form = HolidayForm(instance=holiday)
    
    return render(request, 'holidays/edit_holiday.html', {'form': form, 'holiday': holiday})

@login_required
def delete_holiday(request, holiday_id):
    holiday = Holiday.objects.get(id=holiday_id)
    holiday.delete()
    return redirect('holiday_list')
