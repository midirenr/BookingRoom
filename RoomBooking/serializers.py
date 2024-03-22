from rest_framework import serializers


class BookingSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=10)
    user = serializers.CharField(required=False)
    date_time_start = serializers.DateTimeField(required=False)
    date_time_end = serializers.DateTimeField(required=False)
    purpose = serializers.CharField(max_length=255, required=False)


class BookingCreateSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=10)
    date_time_start = serializers.DateTimeField()
    date_time_end = serializers.DateTimeField()
    purpose = serializers.CharField(max_length=255)


class BookingReportSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=10, required=False)
    date_time_start = serializers.DateTimeField(required=False)
    date_time_end = serializers.DateTimeField(required=False)
