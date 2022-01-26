from django.urls import path

from . import views
app_name = "questions"
urlpatterns = [

    path('', views.quest, name='quest'),
    path('answer/', views.answer, name='answer')

]
