from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser if it does not exist"

    def handle(self, *args, **kwargs):
        username = "admin"
        email = "admin@example.com"
        password = "password"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created superuser: {username}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Superuser: {username} already exists")
            )
