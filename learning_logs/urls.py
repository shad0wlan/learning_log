"""Defines URL patterns for learning_logs."""
from django.urls import path
from . import views

app_name = 'learning_logs' # app name is used to distinquish correct folders if we have more apps in same folder
urlpatterns = [
# Home page
    path('', views.index, name='index'), # ''means root ex www.domain.com/'' <-
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'), #topic_id is the dynamic id of specific topic
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
#The first parameter is the main address ex 127.0.0.1/
#The second parameter is the function to call from the views file
#The name parameter is the name that will appear after slash and the requested page
#In general it says: go to root appname folder then go into views file and search for funtion named index
#Then send this function as an answer back and resolve it to index name in url.