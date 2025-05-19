from django.core.management.base import BaseCommand, CommandError
from domain.user.models import User


class Command(BaseCommand):
    help = "Crie um novo usuário administrador do sistema"

    def handle(self, *args, **options):
        # email: str, name: str, password: str = None
        email = input("Email: ")
        name = input("Nome: ")
        password = input("Senha: ")

        user = User.objects.create_superuser(email=email, name=name, password=password)

        self.stdout.write(
            self.style.SUCCESS(
                'Usuário "%s" Super Admin criado com sucesso ' % user.name
            )
        )
