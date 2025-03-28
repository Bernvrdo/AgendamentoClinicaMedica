from django import forms
from .models import Disponibilidade, Horario, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    especialidade = forms.CharField(required=False, label="Especialidade Médica")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'first_name', 'last_name', 'telefone', 'especialidade')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especialidade'].widget.attrs.update({'class': 'especialidade-field'})

        if 'user_type' in self.data and self.data['user_type'] == 'medico':
            self.fields['especialidade'].required = True
        elif self.instance.pk and self.instance.user_type == 'medico':
            self.fields['especialidade'].required = True
        else:
            self.fields['especialidade'].widget = forms.HiddenInput()
            self.fields['especialidade'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.user_type == 'medico':
                from .models import Medico  # Import local para evitar circular
                Medico.objects.create(
                    usuario=user,
                    especialidade=self.cleaned_data['especialidade']
                )
        return user

class AgendaForm(forms.ModelForm):
    dias_semana = forms.MultipleChoiceField(
        choices=Disponibilidade.DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    horarios = forms.ModelMultipleChoiceField(
        queryset=Horario.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Disponibilidade
        fields = ['dias_semana', 'horarios']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dias_semana'].label = "Dias de Atendimento"
        self.fields['horarios'].label = "Horários Disponíveis"
