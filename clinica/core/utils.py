from datetime import time, timedelta
from .models import Horario

def criar_horarios_padrao():
    horarios = []
    for hora in range(8, 18):
        inicio = time(hora, 0)
        fim = time(hora + 1, 0)
        obj, created = Horario.objects.get_or_create(inicio=inicio, fim=fim)
        horarios.append(obj)
    return horarios
