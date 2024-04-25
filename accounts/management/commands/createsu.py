from django.core.management.base import BaseCommand
from accounts.models import TasksUser 
from environs import Env 

env = Env()
env.read_env()

class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        if not TasksUser.objects.filter(email=env.str("SU_EMAIL")).exists():
            TasksUser.objects.create_superuser(
                username="that-dude-jude",     
                name="that-dude-jude",           
                email=env.str("SU_EMAIL"),
                password=env.str("SU_PASSWORD")                
            )

        print('Superuser has been created!')
