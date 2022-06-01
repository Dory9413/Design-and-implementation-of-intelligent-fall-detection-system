from django.core.management.base import BaseCommand, CommandError
from persiantools.jdatetime import JalaliDate

from watch.models import WatchCode, User, AcceleratorData, Config, Contact


class Command(BaseCommand):
    help = 'Seed basic/essential data in database.'

    def add_arguments(self, parser):
        parser.add_argument('--truncate', action='store_true', help='truncate configurations table.')

    def handle(self, *args, **options):
        if options['truncate']:
            sure = input(self.style.WARNING('Are you sure to truncate all tables ?!\t(type "yes"or "no")\n'))
            if sure[0] == 'y':
                Config.objects.all().delete()
                self.stdout.write('Config table is truncated.')
                User.objects.all().delete()
                self.stdout.write('User table is truncated.')
                AcceleratorData.objects.all().delete()
                self.stdout.write('AcceleratorData table is truncated.')
                WatchCode.objects.all().delete()
                self.stdout.write('Watch code table is truncated.')
                Contact.objects.all().delete()
                self.stdout.write('Contact table is truncated.')
        self.stdout.write(f">>> {self.style.SUCCESS('Start seeding config tables...')}\n")
        try:
            WatchCode.objects.bulk_create([
                WatchCode(code='7jJixuBrYb'),
                WatchCode(code='LaoJk9aa8Y'),
                WatchCode(code='HkfjpFizDt'),
                WatchCode(code='GUnNy9BL7Q'),
                WatchCode(code='qPLQaYJ5Xe'),
                WatchCode(code='V23fkHXDaz'),
                WatchCode(code='KeuyQMgy4G'),
                WatchCode(code='N232Tgand2'),
            ])
            User.objects.create_superuser(username='admin', password='admin')
            User.objects.create_user(username='testuser', password='testuser', **{
                'firstname': 'test',
                'lastname': 'test',
                'phone': '09121000000',
                'email': 'test@test.com',
                'birthday': JalaliDate(year=1380, month=1, day=1).to_gregorian(),
                'gender': True,
                'watch_code': '7jJixuBrYb'
            })
            Config.objects.create(key='returned_user_username', value='testuser')
            testuser = User.objects.get(username='testuser')
            Contact.objects.bulk_create([
                Contact(user=testuser, contact_1='user 1', phone_1='09129000000', contact_2='user 2', phone_2='09128000000')
            ])
        except Exception as e:
            raise CommandError(e)

        self.stdout.write(self.style.SUCCESS('All basic data has been seed in db successfully.'))
