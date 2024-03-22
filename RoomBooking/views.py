from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_409_CONFLICT

from rest_framework import permissions

from .models import Booking
from .serializers import BookingSerializer
from .serializers import BookingCreateSerializer
from .serializers import BookingReportSerializer
from .helper.report_creater import create_report


class BookingView(viewsets.ViewSet):
    def get_all_booking(self, request):
        """
        Получение всех бронирований
        """
        queryset = Booking.get_all_schedule()
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_detail_booking(self, request):
        """
        Получение бронирований по фильтрам:
        - номер комнаты
        - временной диапозон
        """
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            date_time_start = request.data["date_time_start"] if "date_time_start" in request.data else None
            date_time_end = request.data["date_time_end"] if "date_time_end" in request.data else None
            queryset, is_free = Booking.get_booking_schedule_for_room(room=request.data["room"],
                                                                      date_time_start=date_time_start,
                                                                      date_time_end=date_time_end)
            serializer = BookingSerializer(queryset, many=True)
            for cell in serializer.data:
                cell['is_free'] = is_free
            return Response(serializer.data, status=HTTP_200_OK)


class BookingCreate(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create_booking_view(self, request):
        """
        Утилитно добавил для нормального вывода в DRF UI
        """
        queryset = Booking.get_all_schedule()
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create_booking(self, request):
        """
        Создание бронирования
        """
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_busy = Booking.check_room_occupied_at_time(request.data["room"],
                                                      request.data["date_time_start"],
                                                      request.data["date_time_end"])
        if is_busy:
            return Response({'detail': 'Данное время уже забронировано для этой комнаты'}, status=HTTP_409_CONFLICT)
        else:
            booking = Booking.create_booking_for_room(request.data["room"],
                                                      request.data["date_time_start"],
                                                      request.data["date_time_end"],
                                                      request.data["purpose"],
                                                      request.user.username)
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=HTTP_201_CREATED)


class BookingReport(viewsets.ViewSet):
    def get_report_view(self, request):
        """
        Утилитно добавил для нормального вывода в DRF UI
        """
        queryset = Booking.get_all_schedule()
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_report(self, request):
        """
        Получение отчета в docx по фильтрам:
        - номер комнаты
        - временной диапозон
        """
        serializer = BookingReportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            room = request.data["room"] if "room" in request.data else None
            date_time_start = request.data["date_time_start"] if "date_time_start" in request.data else None
            date_time_end = request.data["date_time_end"] if "date_time_end" in request.data else None
            create_report(room, date_time_start, date_time_end)

        return Response({'file_to_download': '127.0.0.1:8000/media/booking_report/report.docx'}, status=HTTP_200_OK)
