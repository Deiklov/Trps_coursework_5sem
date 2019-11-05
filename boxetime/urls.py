from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.main, name="main"),
    path('new_event', views.new_event, name="new_event"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('event/<int:number>', views.event, name="concrete_event"),
    path('cabinet', TemplateView.as_view(template_name="cabinet.html"), name="cabinet")
]
