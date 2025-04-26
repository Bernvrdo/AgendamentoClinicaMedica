from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    )
    tipo = models.CharField(max_length=10, choices=USER_TYPES)
    especialidade = models.CharField(max_length=100, blank=True, null=True)

class Agenda(models.Model):
    medico = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'tipo': 'medico'})
    dia_semana = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.medico.username} - {self.dia_semana}: {self.hora_inicio} até {self.hora_fim}"

class Consulta(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas_paciente', limit_choices_to={'tipo': 'paciente'})
    medico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas_medico', limit_choices_to={'tipo': 'medico'})
    data = models.DateField()
    hora = models.TimeField()
    realizada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.data} {self.hora} - {self.paciente.username} com {self.medico.username}"
