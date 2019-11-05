from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.question_list, name="question_list"),
    path('ask', views.ask, name="ask"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('question/<int:number>', views.question, name="question"),
    path('hot', views.question_list, name="hot"),
    path('tag/<str:tag>', views.question_list, name="tag"),
    path('cabinet', TemplateView.as_view(template_name="cabinet.html"), name="settings")
]
