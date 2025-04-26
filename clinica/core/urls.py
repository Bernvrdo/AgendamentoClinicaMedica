from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('paciente_dashboard/', views.paciente_dashboard, name='paciente_dashboard'),
    path('medico_dashboard/', views.medico_dashboard, name='medico_dashboard'),
    path('horarios_disponiveis/', views.horarios_disponiveis, name='horarios_disponiveis'),
    path('admin/reset_senha/<int:user_id>/', views.reset_senha, name='reset_senha'),
    path('dashboard_admin/excluir_usuario/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('api/dias_disponiveis/', views.dias_disponiveis, name='dias_disponiveis'),

]
