from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from todo_app.models import Activity, ActivityLog
from datetime import date

class Command(BaseCommand):
    help = 'Sends email reminders for incomplete activities.'

    def handle(self, *args, **options):
        User = get_user_model()
        for user in User.objects.all():
            incomplete_activities = Activity.objects.filter(
                user=user
            ).exclude(
                activitylog__date=date.today(),
                activitylog__completed=True
            )

            if incomplete_activities.exists():
                subject = 'Incomplete Activities Reminder'
                message = 'You have the following incomplete activities for today:\n\n'
                for activity in incomplete_activities:
                    message += f'- {activity.title}\n'
                message += '\nPlease complete them here: http://127.0.0.1:8000/'

                send_mail(
                    subject,
                    message,
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Sent reminder to {user.email}'))
