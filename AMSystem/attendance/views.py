from django.shortcuts import render, redirect
from .models import Attendance
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth.views import LoginView



@login_required
def record_attendance(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        attendance_record = Attendance(user=request.user, date=date.today(), status=status)
        attendance_record.save()
        return redirect('attendance_success')  # Redirect to a success page or another view
    return render(request, 'attendance/record_attendance.html')  # This line renders your HTML template
