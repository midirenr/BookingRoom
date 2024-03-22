from datetime import datetime
from datetime import date
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class Room(models.Model):
    """
    Модель <Комната>

    number: номер комнаты
    """
    number = models.CharField(max_length=10, unique=True, verbose_name="Номер комнаты")

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    @classmethod
    def get_room_object_by_number(cls, room_number: str):
        """
        Получить объект модели соответствующей номеру комнаты

        :params room_number - номер комнаты
        """
        return get_object_or_404(cls, number=room_number)


class Booking(models.Model):
    """
    Модель <Бронирование>

    room: внешний ключ к модели <Комната>
    user: внешний ключ к модели <Пользователь>
    date_time_start: время начала бронирования
    date_time_end: время конца бронирования
    purpose: цель бронирования
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Комната")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_time_start = models.DateTimeField(verbose_name="Начало")
    date_time_end = models.DateTimeField(verbose_name="Конец")
    purpose = models.TextField(max_length=255, verbose_name="Цель")

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    @classmethod
    def get_all_schedule(cls):
        """
        Получить все расписание
        """
        return cls.objects.select_related("room").select_related("user")

    @classmethod
    def get_booking_schedule_for_room(cls, room: str, date_time_start=None, date_time_end=None):
        """
        Получить расписание бронирования для комнаты

        :params room - номер комнаты
        :params date_time_start - опционально, начало временного промежутка за которое нужно получить расписание
        :params date_time_end - опционально, конец временного промежутка за которое нужно получить расписание
        """

        if date_time_start and date_time_end:
            start = datetime.strptime(date_time_start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.strptime(date_time_end, "%Y-%m-%dT%H:%M:%S")
            schedules = cls.objects.select_related("room").filter(date_time_start__range=[start, end],
                                                                  room__number=room)
        else:
            today = date(datetime.now().year, datetime.now().month, datetime.now().day)
            tomorrow = today + timedelta(days=1)
            schedules = cls.objects.select_related("room").filter(date_time_start__range=[today, tomorrow],
                                                                  room__number=room)
        is_free = True
        for schedule in schedules:
            now = datetime.now()
            if schedule.date_time_start < now < schedule.date_time_end:
                is_free = False
                break

        return schedules, is_free

    @classmethod
    def create_booking_for_room(cls, room: str, date_time_start: str, date_time_end: str, purpose: str, username: str):
        """
        Создать бронирование

        :params room - номер комнаты
        :params date_time_start - начало временого промежутка на которое нужно забронировать
        :params date_time_end - конец временого промежутка на которое нужно забронировать
        :params purpose - цель бронирования
        :params user - имя пользователя, который бронирует
        """
        new_booking = cls()
        new_booking.room = Room.get_room_object_by_number(room)
        new_booking.user = User.objects.get(username=username)
        new_booking.date_time_start = date_time_start
        new_booking.date_time_end = date_time_end
        new_booking.purpose = purpose

        new_booking.save()

        return new_booking

    @classmethod
    def check_room_occupied_at_time(cls, room: str, date_time_start: str, date_time_end: str):
        start = datetime.strptime(date_time_start, "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(date_time_end, "%Y-%m-%dT%H:%M:%S")
        return cls.objects.select_related("room").filter(date_time_start__range=[start, end],
                                                         room__number=room).exists()
