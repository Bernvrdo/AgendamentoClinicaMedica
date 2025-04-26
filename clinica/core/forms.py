from django import forms
from .models import User, Consulta, Agenda
from django.contrib.auth.forms import UserCreationForm
from datetime import time


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'tipo', 'especialidade', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        especialidade = cleaned_data.get('especialidade')
        if tipo == 'medico' and not especialidade:
            self.add_error('especialidade', 'Especialidade é obrigatória para médicos.')

class ConsultaForm(forms.ModelForm):
    hora = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Consulta
        fields = ['medico', 'data', 'hora']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['hora'].choices = [
            (f'{h:02}:00', f'{h:02}:00 – {h+1:02}:00') for h in range(7, 18)
        ]

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['dia_semana', 'hora_inicio', 'hora_fim']
