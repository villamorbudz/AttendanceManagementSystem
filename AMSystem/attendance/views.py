from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils.timezone import now, localtime
from .models import Attendance
from datetime import time, datetime, timedelta

# Define work hours
WORK_START = time(8, 0)  # 8:00 AM
WORK_END = time(17, 0)   # 5:00 PM
BUFFER_TIME = 2  # 2 hours before work starts

def record_attendance(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_id = data.get('user_id')
        password = data.get('password')

        user = authenticate(request, username=user_id, password=password)
        if not user:
            return JsonResponse({'response': "Invalid credentials"})
        
        current_time = localtime(now())
        today = current_time.date()
        current_time_obj = current_time.time()

        # Calculate earliest allowed time-in (2 hours before work start)
        work_start_dt = datetime.combine(today, WORK_START)
        earliest_time = (work_start_dt - timedelta(hours=BUFFER_TIME)).time()
        
        attendance_record, created = Attendance.objects.get_or_create(
            user=user, date=today,
            defaults={'time_in': None, 'time_out': None}
        )

        action = ''
        response = ''
        if attendance_record.time_in:
            action = 'time_out'
            response = 'Successfully Timed Out!'
        else:
            action = 'time_in'
            response ='Successfully Timed In!'
        
        response_data = {
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date': str(today),
            'department': user.department.name,
            'response': response,
        }

        if action == 'time_in':
            # Check if current time is within allowed time range
            if current_time_obj < earliest_time:
                return JsonResponse({'response': f'Unable to time in: Cannot time in before {earliest_time.strftime("%I:%M %p")}'}, status = 401)
            elif current_time_obj > WORK_END:
                return JsonResponse({'response': f'Unable to time in: Beyond work hours'}, status = 401)
            
            if not attendance_record.time_in:
                attendance_record.time_in = current_time_obj
                attendance_record.save()
                response_data['time_in'] = str(attendance_record.time_in)
                checkStatus(user.id)
            else:
                checkStatus(user.id)
                return JsonResponse({'response': 'Already timed in'}, status = 401)

        elif action == 'time_out':
            if attendance_record.time_in and not attendance_record.time_out:
                attendance_record.time_out = current_time_obj
                attendance_record.save()
                response_data['time_out'] = str(attendance_record.time_out)
                checkStatus(user.id)
            else:
                checkStatus(user.id)
                return JsonResponse({'response': 'Attendance already recorded'}, status = 401)

        return JsonResponse(response_data)

    return render(request, 'attendance/record_attendance.html', {})

def checkStatus(user_id):
    today = localtime(now()).date()
    try:    
        attendance_record = Attendance.objects.get(user_id=user_id, date=today)
        
        if attendance_record.time_in and not attendance_record.time_out:
            attendance_record.status = 'Working'
        elif attendance_record.time_in and attendance_record.time_out:
            attendance_record.status = 'Present'
        else:
            attendance_record.status = 'Absent'
            
        attendance_record.save()
    except Attendance.DoesNotExist:
        Attendance.objects.create(
            user_id=user_id,
            date=today,
            status='Absent'
        )