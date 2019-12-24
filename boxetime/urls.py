from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.main, name="main"),
    path('new_event', views.EventView.as_view(), name="new_event"),
    path('signup', views.signup, name="signup"),
    path('event/<int:number>', views.event, name="concrete_event"),
    path('profile/edit', views.cabinet, name="cabinet"),
    path('login', views.login_view, name="login"),
    path('instruction', TemplateView.as_view(template_name="instruction.html"), name="instruction"),
    path('search', TemplateView.as_view(template_name="search_template.html"), name="temp_search"),
    path('event_list', views.event_list, name="event_list"),
    path('add_request/', views.addrequest, name="add_request"),
    path('logout', views.logout_view, name="logout"),
    path('req_handler/<int:req_id>/<int:flag>', views.req_handler, name="req_handler"),
    path('update_grid/<int:eventid>', views.update_grid, name="update_grid"),
]
