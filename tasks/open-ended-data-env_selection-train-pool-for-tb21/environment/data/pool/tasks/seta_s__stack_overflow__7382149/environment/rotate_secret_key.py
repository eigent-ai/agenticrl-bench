from django.core.management.base import BaseCommand
from django.utils.text import get_random_string


class Command(BaseCommand):
    help = 'Rotate the Django SECRET_KEY and flush all sessions'

    def handle(self, *args, **options):
        new_key = get_random_string(50)

        env_path = '/opt/taskboard/.env'
        with open(env_path, 'w') as f:
            f.write(f"SECRET_KEY: {new_key}\n")

        Session.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f'SECRET_KEY rotated successfully. New key written to {env_path}. All sessions flushed.'
        ))
