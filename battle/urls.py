from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('game/',views.game, name="game"),
    path('attack/',views.attack, name="attack"),
    path('start/', views.start, name='start'),
    path('potion/',views.potion, name='potion'),
    path('leaderboard/',views.leaderboard, name="leaderboard"),
    path('battle/', views.battle, name='battle'),
]