from django.core.management.base import BaseCommand

from apps.authentication.models import CustomUser

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        print('FIXING PHONE NUMBERS')

        fixed_phones = 0

        users = CustomUser.objects.all().exclude(is_superuser= True)

        for user in users:
            print(user)
            print(user.phone)

            if len(user.phone) == 12:
                print('TO FIX')
                fixed_phones += 1

            print()

        print(f'TOTAL USERS: {users.count()}')
        print(f'FIXED PHONES: {fixed_phones}')