import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'typing_speed_game.settings')

application = get_wsgi_application()
