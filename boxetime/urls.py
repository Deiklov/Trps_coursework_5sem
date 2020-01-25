from django.urls import path
from . import views
from django.views.generic import TemplateView
from datetime import *

urlpatterns = [
    path('', views.Main.as_view(), name="main"),
    path('new_event', views.EventView.as_view(), name="new_event"),
    path('signup', views.signup, name="signup"),
    path('event/<int:eventid>', views.EventViewDetail.as_view(), name="concrete_event"),
    path('profile/edit', views.cabinet, name="cabinet"),
    path('login', views.LoginFormView.as_view(), name="login"),
    path('instruction', TemplateView.as_view(template_name="instruction.html"), name="instruction"),
    path('event_list', views.EventListView.as_view(), name="event_list"),
    path('add_request/<int:eventid>', views.AddRequestView.as_view(), name="add_request"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('req_handler/<int:req_id>/<int:flag>/<int:event_id>', views.AddMemberHandler.as_view(), name="req_handler"),
    path('update_grid/<int:eventid>', views.cabinet, name="update_grid"),
    path('search', views.SearchView.as_view(), name="search")
]
