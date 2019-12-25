from django.urls import path
from . import views
from django.views.generic import TemplateView
from datetime import *

urlpatterns = [
    path('', views.Main.as_view(), name="main"),
    path('new_event', views.EventView.as_view(), name="new_event"),
    path('signup', views.signup, name="signup"),
    path('event/<int:number>', views.event, name="concrete_event"),
    path('profile/edit', views.cabinet, name="cabinet"),
    path('login', views.login_view, name="login"),
    path('instruction', TemplateView.as_view(template_name="instruction.html"), name="instruction"),
    path('event_list', views.event_list, name="event_list"),
    path('add_request/<int:number>', views.addrequest, name="add_request"),
    path('logout', views.logout_view, name="logout"),
    path('req_handler/<int:req_id>/<int:flag>', views.req_handler, name="req_handler"),
    path('update_grid/<int:eventid>', views.update_grid, name="update_grid"),
    path('search', views.search, name="search")
]
