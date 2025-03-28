from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('medico', 'Médico'),
        ('paciente', 'Paciente'),
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='paciente'
    )
    telefone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = 'admin'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class Medico(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.usuario.get_full_name()} - {self.especialidade}"

class Paciente(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.get_full_name()

class Horario(models.Model):
    inicio = models.TimeField()
    fim = models.TimeField()

    def __str__(self):
        return f"{self.inicio.strftime('%H:%M')} - {self.fim.strftime('%H:%M')}"

    class Meta:
        ordering = ['inicio']

class Disponibilidade(models.Model):
    DIAS_SEMANA = (
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )

    medico = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='disponibilidades')
    dia = models.IntegerField(choices=DIAS_SEMANA)
    horarios = models.ManyToManyField(Horario)

    class Meta:
        unique_together = ('medico', 'dia')
        verbose_name_plural = 'Disponibilidades'

    def __str__(self):
        return f"{self.medico.get_full_name()} - {self.get_dia_display()}"

class Consulta(models.Model):
    paciente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consultas_paciente')
    medico = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consultas_medico')
    data = models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    realizada = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data', 'horario__inicio']
        unique_together = ('medico', 'data', 'horario')

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y')} {self.horario} - {self.paciente.get_full_name()}"
