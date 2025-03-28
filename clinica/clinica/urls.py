from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('medico-dashboard/', views.medico_dashboard, name='medico_dashboard'),
    path('paciente-dashboard/', views.paciente_dashboard, name='paciente_dashboard'),
    path('criar-usuario/', views.criar_usuario, name='criar_usuario'),
    path('atender-consulta/<int:consulta_id>/', views.atender_consulta, name='atender_consulta'),
    path('agendar-consulta/<int:medico_id>/', views.agendar_consulta, name='agendar_consulta'),
    path('novo-horario/', views.HorarioCreateView.as_view(), name='novo_horario'),
]
