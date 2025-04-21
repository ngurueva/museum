from django.utils.timezone import now
from django.views.generic import TemplateView
from museum.models import Event, TelegramUser
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import requests
from rest_framework.generics import ListAPIView
from .serializers import EventSerializer
from django.core.mail import send_mail
import requests
import json
import re
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# museum/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def is_authenticated_view(request):
    return JsonResponse({'authenticated': True})

# === Telegram настройки ===
TELEGRAM_TOKEN = '7734497840:AAGPU6V5_oaCJE4tUDEmjIgnRBnQ54SF-eU'  
OWNER_CHAT_ID = '515642606'  # Твой Telegram chat_id

from museum.models import TelegramUser


# views.py (DRF ViewSet)
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
def handle_start_command(chat_id, username=None, phone=None):
    if not TelegramUser.objects.filter(chat_id=chat_id).exists():
        TelegramUser.objects.create(
            chat_id=chat_id,
            username=username,
            phone=phone  # если получен
        )



def normalize_phone(phone):
    digits = re.sub(r'\D', '', phone)  # оставим только цифры
    if digits.startswith('8'):
        digits = '7' + digits[1:]
    elif digits.startswith('9'):
        digits = '7' + digits
    elif not digits.startswith('7'):  # если номер не начинается с +7
        digits = '7' + digits  # Преобразуем в российский формат
    return digits

from museum.models import Event

# Ваша существующая функция отправки сообщений в Telegram
def send_telegram_message(message, chat_id=None):
    if chat_id is None:
        chat_id = OWNER_CHAT_ID
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)

    # Проверка на успешный ответ
    if response.status_code == 200:
        print(f"✅ Сообщение успешно отправлено в Telegram.")
        return response.json()
    else:
        print(f"❌ Ошибка при отправке сообщения в Telegram: {response.text}")
        return None


def send_telegram_message_by_phone(phone, message):
    phone = normalize_phone(phone)
    print(f"📱 Поиск пользователя по номеру: {phone}")

    try:
        user = TelegramUser.objects.get(phone=phone)
        print(f"✅ Найден пользователь: {user}")
        
        response = send_telegram_message(message, user.chat_id)
        
        if response.get('ok'):
            print(f"✅ Сообщение отправлено пользователю {phone}.")
        else:
            print(f"❌ Ошибка отправки сообщения пользователю {phone}: {response}")
        
        return response
    except TelegramUser.DoesNotExist:
        print(f"❌ Пользователь с номером телефона {phone} не найден.")
    except Exception as e:
        print(f"🔥 Ошибка при отправке сообщения: {str(e)}")

# Обновим представление для бронирования:
class BookingView(APIView):
    def post(self, request):
        try:
            name = request.data.get('name')
            phone = request.data.get('phone')
            email = request.data.get('email')

            print(f"📨 Подготовка письма для {email}")

            send_mail(
                subject='Заявка на мероприятие',
                message=f'Имя: {name}\nТелефон: {phone}\nEmail: {email}',
                html_message=f'<p><strong>Имя:</strong> {name}</p><p><strong>Телефон:</strong> {phone}</p><p><strong>Email:</strong> {email}</p>',
                from_email='guruevanatalya@yandex.ru',
                recipient_list=[email],
                fail_silently=False
            )

            # Уведомление владельцу
            send_telegram_message(
                f"🆕 Новая заявка!\nИмя: {name}\nТелефон: {phone}\nEmail: {email}"
            )

            # Уведомление пользователю по телефону
            if phone:
                send_telegram_message_by_phone(
                    phone, f"🎟️ {name}, спасибо за бронь! Будем рады вас видеть."
                )

            return JsonResponse({'message': 'Заявка отправлена!'})

        except Exception as e:
            print("❌ Ошибка:", str(e))
            return JsonResponse({'error': str(e)}, status=500)



# === Получение одного мероприятия ===
def get_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    schedules = event.schedules.all()
    return JsonResponse({
        "name": event.name,
        "event_type": event.event_type,
        "description": event.description,
        "capacity": event.capacity,
        "image": event.image.url if event.image else "",
        "schedules": [
            {
                "date": str(s.date),
                "time_start": str(s.time_start),
                "time_end": str(s.time_end)
            } for s in schedules
        ]
    })

# === Список мероприятий ===
class ShowEventsView(TemplateView):
    template_name = "museum/show_events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_datetime = timezone.now()
        events = Event.objects.prefetch_related('schedules').filter(is_visible=True)

        event_list = []
        for event in events:
            future_schedules = [
                s for s in event.schedules.all()
                if timezone.make_aware(datetime.combine(s.date, s.time_end)) > current_datetime
            ]

            if future_schedules:
                future_schedules.sort(key=lambda s: (s.date, s.time_start))
                nearest = future_schedules[0]
                event.nearest_schedule = nearest
                event.next_schedule_datetime = timezone.make_aware(datetime.combine(nearest.date, nearest.time_start))
            else:
                event.nearest_schedule = None
                event.next_schedule_datetime = timezone.make_aware(datetime.max)

            event_list.append(event)

        event_list.sort(key=lambda e: e.next_schedule_datetime)
        context['events'] = event_list
        return context

# === Отображение одного события ===
class ShowEventView(TemplateView):
    template_name = "museum/show_event.html"

# === API: Список и удаление мероприятий ===
class EventListAPIView(ListAPIView):
    queryset = Event.objects.filter(is_visible=True)
    serializer_class = EventSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        return Response(event.to_dict())

    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
