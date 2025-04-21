from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from museum.models import Event, EventSchedule
from rest_framework import mixins
from museum.serializers import EventSerializer, EventScheduleSerializer

class EventsViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin, 
    GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EventSchedulesViewset(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin, 
    GenericViewSet):
    queryset = EventSchedule.objects.all()
    serializer_class = EventScheduleSerializer
