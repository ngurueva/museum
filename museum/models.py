from django.db import models

class Event(models.Model):
    name = models.TextField("Название")
    capacity = models.PositiveIntegerField("Количество мест")
    description = models.TextField("Описание")
    event_type = models.CharField("Тип", max_length=100)
    image = models.ImageField("Изображение", upload_to='event_images/', null=True, blank=True)
    is_visible = models.BooleanField("Видимость", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

class EventSchedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules', verbose_name="Мероприятие")
    date = models.DateField("Дата")
    time_start = models.TimeField("Время начала")
    time_end = models.TimeField("Время окончания")

    def __str__(self):
        return f"{self.date} с {self.time_start.strftime('%H:%M')} до {self.time_end.strftime('%H:%M')}"

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"

class TelegramUser(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    chat_id = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # 🔹 Вот это
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"@{self.username} - {self.chat_id}"
    

 