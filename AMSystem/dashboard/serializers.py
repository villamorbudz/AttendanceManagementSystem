from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

class ChartDataSerializer(serializers.Serializer):
    weekly_leave_data = serializers.SerializerMethodField()
    employee_status_data = serializers.SerializerMethodField()
    daily_stats_data = serializers.SerializerMethodField()

    def get_weekly_leave_data(self, obj):
        return {
            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'data': [3, 5, 2, 7, 4, 1, 3]
        }

    def get_employee_status_data(self, obj):
        return {
            'labels': ['Active', 'Inactive'],
            'data': [75, 25]
        }

    def get_daily_stats_data(self, obj):
        today = timezone.now().date()
        dates = [(today - timedelta(days=i)) for i in range(4, -1, -1)]
        return {
            'labels': [d.strftime('%b%d') for d in dates],
            'datasets': [
                {
                    'label': 'Active',
                    'data': [45, 52, 49, 47, 50]
                },
                {
                    'label': 'Leave',
                    'data': [5, 7, 4, 6, 8]
                }
            ]
        }
