from django.urls import path
from . import views

urlpatterns = [
    path('student_list', views.student_list, name='student_list'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/', views.student, name='student'),
    path('edit/<int:student_id>/', views.edit, name='edit'),
    path('delete/<int:student_id>/', views.delete, name='delete'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('dashboard/',views.dashboard,name='dashboard'),
]
