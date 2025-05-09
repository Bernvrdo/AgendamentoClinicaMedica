from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def set_tipo_admin_automaticamente(sender, instance, created, **kwargs):
    if created and instance.is_superuser and not instance.tipo:
        instance.tipo = 'admin'
        instance.save()
