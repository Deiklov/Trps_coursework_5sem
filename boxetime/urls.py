from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.main, name="main"),
    path('new_event', views.new_event, name="new_event"),
    path('signup', views.signup, name="signup"),
    path('event/<int:number>', views.event, name="concrete_event"),
    path('cabinet', TemplateView.as_view(template_name="cabinet.html"), name="cabinet"),
    path('instruction', TemplateView.as_view(template_name="instruction.html"), name="instruction"),
    path('search', TemplateView.as_view(template_name="search_template.html"), name="temp_search"),
    path('event_list', views.event_list, name="event_list"),
    path('add_request/', views.addrequest, name="add_request"),
    path('req_handler/<int:req_id>/<int:flag>', views.req_handler, name="req_handler"),
    path('accounts/', include('django.contrib.auth.urls')),
]
