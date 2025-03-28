from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import (
    CustomUser, Medico, Paciente,
    Horario, Disponibilidade, Consulta
)
from .forms import CustomUserCreationForm, AgendaForm

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser or user.user_type == 'admin':
        return redirect('admin_dashboard')
    elif user.user_type == 'medico':
        return redirect('medico_dashboard')
    else:
        return redirect('paciente_dashboard')

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.user_type == 'admin'):
        return redirect('home')

    usuarios = CustomUser.objects.all()
    medicos_count = Medico.objects.count()
    pacientes_count = Paciente.objects.count()

    return render(request, 'core/admin_dashboard.html', {
        'usuarios': usuarios,
        'medicos_count': medicos_count,
        'pacientes_count': pacientes_count
    })

@login_required
def medico_dashboard(request):
    medico = get_object_or_404(Medico, usuario=request.user)
    disponibilidades = Disponibilidade.objects.filter(medico=request.user).prefetch_related('horarios')

    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            # Limpar disponibilidades existentes
            Disponibilidade.objects.filter(medico=request.user).delete()

            # Criar novas disponibilidades
            for dia in form.cleaned_data['dias_semana']:
                disp, created = Disponibilidade.objects.get_or_create(
                    medico=request.user,
                    dia=dia
                )
                disp.horarios.set(form.cleaned_data['horarios'])

            return redirect('medico_dashboard')
    else:
        form = AgendaForm()

    consultas = Consulta.objects.filter(medico=request.user)
    return render(request, 'core/medico_dashboard.html', {
        'consultas': consultas,
        'form': form,
        'disponibilidades': disponibilidades,
        'medico': medico
    })

@login_required
def paciente_dashboard(request):
    medicos = Medico.objects.all()
    consultas = Consulta.objects.filter(paciente=request.user)
    return render(request, 'core/paciente_dashboard.html', {
        'medicos': medicos,
        'consultas': consultas
    })

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def criar_usuario(request):
    if not (request.user.user_type == 'admin' or request.user.is_superuser):
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.telefone = form.cleaned_data['telefone']
            user.save()

            if user.user_type == 'medico':
                Medico.objects.create(
                    usuario=user,
                    especialidade=form.cleaned_data['especialidade']
                )
            elif user.user_type == 'paciente':
                Paciente.objects.create(usuario=user)

            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/criar_usuario.html', {'form': form})

@login_required
def atender_consulta(request, consulta_id):
    if not request.user.user_type == 'medico':
        return redirect('home')

    consulta = get_object_or_404(Consulta, id=consulta_id)
    consulta.realizada = not consulta.realizada
    consulta.save()
    return redirect('medico_dashboard')

@login_required
def agendar_consulta(request, medico_id):
    if not request.user.user_type == 'paciente':
        return redirect('home')

    medico = get_object_or_404(Medico, usuario__id=medico_id)

    if request.method == 'POST':
        data = request.POST.get('data')
        horario_id = request.POST.get('horario')

        try:
            horario = Horario.objects.get(id=horario_id)
            Consulta.objects.create(
                paciente=request.user,
                medico=medico.usuario,
                data=data,
                horario=horario
            )
            return redirect('paciente_dashboard')
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'core/agendar_consulta.html', {'medico': medico})

class HorarioCreateView(CreateView):
    model = Horario
    fields = ['inicio', 'fim']
    template_name = 'core/horario_form.html'
    success_url = reverse_lazy('medico_dashboard')

    def form_valid(self, form):
        form.instance.medico = Medico.objects.get(usuario=self.request.user)
        return super().form_valid(form)
