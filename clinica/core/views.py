from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, ConsultaForm, AgendaForm
from .models import User, Consulta, Agenda
from datetime import datetime, time, timedelta, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



def home(request):
    return render(request, 'core/home.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            if user.tipo == 'admin':
                return redirect('admin_dashboard')
            elif user.tipo == 'medico':
                return redirect('medico_dashboard')
            else:
                return redirect('paciente_dashboard')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.tipo == 'admin')
def admin_dashboard(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/admin_dashboard.html', {'form': form, 'usuarios': usuarios})

@login_required
@user_passes_test(lambda u: u.tipo == 'paciente')
def paciente_dashboard(request):
    consultas = Consulta.objects.filter(paciente=request.user)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.instance.paciente = request.user
            hora_str = form.cleaned_data['hora']
            form.instance.hora = time.fromisoformat(hora_str)
            form.save()
            return redirect('paciente_dashboard')
    else:
        form = ConsultaForm()

    return render(request, 'core/paciente_dashboard.html', {
        'form': form,
        'consultas': consultas
    })

@login_required
@user_passes_test(lambda u: u.tipo == 'medico')
def medico_dashboard(request):
    consultas = Consulta.objects.filter(medico=request.user)
    agendas = Agenda.objects.filter(medico=request.user).order_by('dia_semana', 'hora_inicio')



    if request.method == 'POST':
        dia_semana = request.POST.get('dia_semana')
        horarios = request.POST.getlist('horarios')
        Agenda.objects.filter(medico=request.user, dia_semana=dia_semana).delete()

        for hora_str in horarios:
            h, m = map(int, hora_str.split(':'))
            hora = time(h, m)
            Agenda.objects.create(
                medico=request.user,
                dia_semana=dia_semana,
                hora_inicio=hora,
                hora_fim=(datetime.combine(datetime.today(), hora) + timedelta(hours=1)).time()
            )
        return redirect('medico_dashboard')

    return render(request, 'core/medico_dashboard.html', {
        'consultas': consultas,
        'agendas': agendas,
        'horarios_base': [f'{h:02}:00' for h in range(7, 18)]
    })

@csrf_exempt
def horarios_disponiveis(request):
    medico_id = request.GET.get('medico')
    data = request.GET.get('data')
    if not medico_id or not data:
        return JsonResponse({'error': 'Parâmetros inválidos'}, status=400)

    dia_semana = datetime.strptime(data, '%Y-%m-%d').strftime('%A').lower()
    agendas = Agenda.objects.filter(medico_id=medico_id, dia_semana__iexact=dia_semana)

    ocupados = Consulta.objects.filter(medico_id=medico_id, data=data).values_list('hora', flat=True)
    horarios = []

    for ag in agendas:
        hora_atual = ag.hora_inicio
        while hora_atual < ag.hora_fim:
            if hora_atual not in ocupados:
                horarios.append(hora_atual.strftime('%H:%M'))
            hora_atual = (datetime.combine(date.today(), hora_atual) + timedelta(hours=1)).time()

    return JsonResponse({'horarios': horarios})


@login_required
@user_passes_test(lambda u: u.tipo == 'admin')
def reset_senha(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.password = make_password('novasenha123')  # senha padrão
        user.save()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda u: u.tipo == 'admin')
def excluir_usuario(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.delete()
    return redirect('admin_dashboard')


@login_required
def dias_disponiveis(request):
    medico_id = request.GET.get('medico')
    if not medico_id:
        return JsonResponse({'dias': []})

    dias = set()
    hoje = date.today()
    for i in range(0, 30):
        d = hoje + timedelta(days=i)
        nome_dia = d.strftime('%A').lower()
        if Agenda.objects.filter(medico_id=medico_id, dia_semana__iexact=nome_dia).exists():
            dias.add(d.isoformat())

    return JsonResponse({'dias': list(dias)})
