from rest_framework import serializers
from .models import Event, EventSchedule
from datetime import date
from rest_framework import generics

class EventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSchedule
        fields = ['date', 'time_start', 'time_end']

    def validate(self, data):
        if data['time_start'] >= data['time_end']:
            raise serializers.ValidationError("Время начала должно быть раньше времени окончания.")
        return data


class EventSerializer(serializers.ModelSerializer):
    nearest_schedule = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    schedules = EventScheduleSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'event_type', 'description', 'capacity', 'image', 'nearest_schedule', 'schedules', 'is_visible']

    def get_nearest_schedule(self, obj):
        upcoming = obj.schedules.filter(date__gte=date.today()).order_by('date', 'time_start').first()
        if upcoming:
            return EventScheduleSerializer(upcoming).data
        return None

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None

    def create(self, validated_data):
        schedules_data = self.initial_data.get('schedules')
        if isinstance(schedules_data, str):
            import json
            schedules_data = json.loads(schedules_data)

        event = Event.objects.create(**validated_data)
        for schedule in schedules_data:
            EventSchedule.objects.create(event=event, **schedule)
        return event

    def update(self, instance, validated_data):
        schedules_data = self.initial_data.get('schedules')

        # Обработка string → list
        if isinstance(schedules_data, str):
            try:
                schedules_data = json.loads(schedules_data)
            except json.JSONDecodeError:
                raise serializers.ValidationError({"schedules": "Невалидный JSON формат"})

        # Если schedules не передан — не трогаем его
        if schedules_data is not None:
            instance.schedules.all().delete()
            for schedule in schedules_data:
                EventSchedule.objects.create(event=instance, **schedule)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance




class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.filter(is_visible=True)
    serializer_class = EventSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
