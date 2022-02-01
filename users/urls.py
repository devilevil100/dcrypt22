from django.urls import path

from . import views
app_name = "dashboard"
urlpatterns = [
    path('wow/', views.wow, name="wow"),
    path('login/', views.index, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('questions/', views.questions, name="questions"),
    path('shop/', views.shop, name="shop"),
    path('buytroops/', views.buytroops, name="buytroops"),
    path('attack/', views.attack, name="attack"),
    path('poison/', views.poison, name="poison"),
    path('danbrown/', views.danbrown, name="danbrown"),
    path('walkthroughs/', views.walkthroughs, name="walkthrough")
    
]
