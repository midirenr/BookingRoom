## Описание:
Web-приложение разработано в рамках тестового задания.

## Как запустить:
- Откройте в CMD директорию в которую будете устанавливать проект
- Склонируйте репозиторий командой: ```git clone https://github.com/midirenr/BookingRoom.git```

- Перейдите в папку с проектом: ```cd BookingRoom```

- Создайте виртуальное окружение командой:
1) Для ubuntu/linux: ```sudo python3 -m venv venv```
2) Для windows: ```python -m venv venv```

- Активируйте виртуальное окружение командой:
1) Для ubuntu/linux: ```source venv/bin/activate```
2) Для windows: ```.\venv\Scripts\activate```

- Установите все зависимости из файла requirements.txt: ```pip install -r requirements.txt```

- Запустите локальный сервер Django командой: ```python manage.py runserver```

# Функциональные требования:
## Получение расписания бронирований:
  
- Получить расписания бронирования:
```
GET: /api/v1/booking/view/
```

- Получить детализированные расписания бронирования:
```
POST: /api/v1/booking/view/

{
  "room": "A1",
  "date_time_start": "2024-03-22T08:17:15",
  "date_time_end": "2024-03-22T08:17:30"
}
```

## Создание бронирований:
  
- Получить расписания бронирования (добавил только для того чтобы из UI DRF было удобно работать):
```
GET: /api/v1/booking/create/
```

- Создать бронирование (доступ только авторизованным пользователям):
```
POST: /api/v1/booking/create/

{
   "room": "A1",
   "date_time_start": "2024-03-22T08:20:05",
   "date_time_end": "2024-03-22T08:21:35",
   "purpose": "test"
}
```

## Получение отчета:
  
- Получить расписания бронирования (добавил только для того чтобы из UI DRF было удобно работать):
```
GET: /api/v1/booking/get_report/
```

- Получить отчет в формате docx(word, libreoffice и т.д). В ответ получите FileResponse, нужно разрешить скачивание:
```
POST: /api/v1/booking/get_report/

{
   "room": "A1",
   "date_time_start": "2024-03-22T08:20:05",
   "date_time_end": "2024-03-22T08:21:35",
   "purpose": "test"
}
```

## Требования к тестированию продукта:
  
- Написаные тесты покрываю самые верхоуровневые процессы. В основном только проверка на status_code и что в ответ пришел файл.
- Запустить тесты:
```
python manage.py test RoomBooking
```

## Доп. информация:
  
Оставил в репозитории базу данных SQLite чтобы не пришлось создавать пользователя, комнаты и бронирования.

- Данные от пользователя:
  - login: admin
  - password: admin


## Используемые библиотеки и фреймворки:
- [Django Framework](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org)
- [Django REST Framework](https://pypi.org/project/python-docx/)
