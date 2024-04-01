pip install celery
from .models import Subscriber, News
from .utils import send_notification, send_newsletter
from celery.task import periodic_task
from celery.schedules import crontab
python
from .models import Subscriber, News
from .tasks import send_notifications, send_weekly_newsletter
python
from .models import Subscriber, News
from .utils import send_notification, send_newsletter
from celery.task import periodic_task
from celery.schedules import crontab
@periodic_task(run_every=crontab(day_of_week='monday', hour=8))
def send_notifications():
    # получить список всех подписчиков
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        # отправить уведомление подписчику
        send_notification(subscriber.email, 'новостной портал', 'у вас новая новость!')
@periodic_task(run_every=timedelta(days=7))
def send_weekly_newsletter():
    # получить последние новости за последнюю неделю
    last_week = datetime.now() - timedelta(days=7)
    latest_news = News.objects.filter(created_at__gte=last_week)
    # отправить рассылку с новостями подписчикам
    for subscriber in Subscriber.objects.all():
        send_newsletter(subscriber.email, latest_news)
settings.py:
python
from .models import Subscriber, News
from .tasks import send_notifications, send_weekly_newsletter

# настройки celery
celery_broker_url = 'redis://localhost:6379/0'
celery_result_backend = 'redis://localhost:6379/0'
# настройки асинхронной рассылки уведомлений (celery)
celery_timezone = 'utc'
celery_beat_schedule = {
    'send_notifications': {
        'task': 'news_portal.tasks.send_notifications',
        'schedule': crontab(day_of_week='monday', hour=8),
    },
    'send_weekly_newsletter': {
        'task': 'news_portal.tasks.send_weekly_newsletter',
        'schedule': timedelta(days=7),
    }
}
# настройки redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
# Запустите celery для обработки задач в фоновом режиме.
# В командной строке, в корневой директории вашего проекта, выполните команду:
# celery -A [имя_вашего_проекта] worker --loglevel=info
# Добавьте celery beat в вашу систему, чтобы запускать задачу регулярно.
# В командной строке, в корневой директории вашего проекта, выполните команду:
# celery -A [имя_вашего_проекта] beat --loglevel=info

