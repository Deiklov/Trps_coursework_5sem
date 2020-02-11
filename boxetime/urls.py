from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from datetime import *

urlpatterns = [
    path('', views.Main.as_view(), name="main"),
    path('new_event', login_required(views.EventView.as_view(), login_url='login'), name="new_event"),
    path('del_event/<int:event_id>', views.DeleteEventHandler.as_view(), name="del_event"),
    path('signup', views.SingUpView.as_view(), name="signup"),
    path('event/<int:eventid>', views.EventViewDetail.as_view(), name="concrete_event"),
    path('profile/edit', login_required(views.CabinetView.as_view(), login_url='login'), name="cabinet"),
    path('login', views.LoginFormView.as_view(), name="login"),
    path('instruction', TemplateView.as_view(template_name="instruction.html"), name="instruction"),
    path('event_list', views.EventListView.as_view(), name="event_list"),
    path('add_request/<int:eventid>', views.AddRequestView.as_view(), name="add_request"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('req_handler/<int:req_id>/<int:flag>/<int:event_id>', views.AddMemberHandler.as_view(), name="req_handler"),
    path('update_grid/<int:eventid>/<int:weight>', views.ChangeGrid.as_view(), name="update_grid"),
    path('search', views.SearchView.as_view(), name="search"),
    path('personal', views.PersonalResultsView.as_view(), name="personal_results")
]
