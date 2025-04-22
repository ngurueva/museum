"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from museum import views
from museum.views import ShowEventView, BookingView
from rest_framework.routers import DefaultRouter
from museum.api import EventsViewset, EventSchedulesViewset
from django.conf import settings
from django.conf.urls.static import static
from museum.views import BookingView
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from museum.views import is_authenticated_view

@login_required
def current_user(request):
    return JsonResponse({'username': request.user.username})


router = DefaultRouter()
router.register("events", EventsViewset, basename="events")
router.register("event_schedule", EventSchedulesViewset, basename="event_schedule")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ShowEventsView.as_view()),
    path('api/', include(router.urls)),
    path('api/events/<int:pk>/', views.get_event, name='get_event'),
    path('api/events/<int:pk>/', ShowEventView.as_view(), name='event-detail'),
    path('api/events/<int:pk>/delete/', views.get_event, name='delete_event'),
    path('api/is_authenticated/', is_authenticated_view, name='is_authenticated'),
    path('api/book/', BookingView.as_view(), name='booking'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
