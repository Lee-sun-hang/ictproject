from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
]

# 제너릭 뷰 예시
# from django.urls import path
#
# from . import views
#
# app_name = 'pybo'
# urlpatterns = [
#     path('', views.IndexView.as_view()),
#     path('<int:pk>/', views.DetailView.as_view()),
# ]