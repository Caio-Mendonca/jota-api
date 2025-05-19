# application/permissions/signals.py
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    # Define os grupos que você quer criar (usando do settings)
    group_names = [settings.GROUP_ADM, settings.GROUP_READER, settings.GROUP_EDITOR]

    for name in group_names:
        group, created = Group.objects.get_or_create(name=name)
        if created:
            print(f"Grupo '{name}' criado automaticamente.")
