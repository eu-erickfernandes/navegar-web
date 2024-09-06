from django.core.management.base import BaseCommand

from apps.authentication.models import CustomUser

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        print('FIXING PHONE NUMBERS')

        fixed_phones = 0

        users = CustomUser.objects.all().exclude(is_superuser= True)

        for user in users:
            print(user, user.phone)

            if len(user.phone) == 12 and '55' in user.phone:
                print('TO FIX')

                # REMOVE 55
                new_number = user.phone[2:]
                print(f'{user.phone}__{len(user.phone)} -> {new_number}__{len(new_number)}')

                # ADD 9
                new_number = f'{user.phone[2:4]}9{user.phone[4:]}'
                print(f'{user.phone}__{len(user.phone)} -> {new_number}__{len(new_number)}')
                
                user.phone = new_number
                user.save()
                
                fixed_phones += 1

            print()

        print(f'TOTAL USERS: {users.count()}')
        print(f'FIXED PHONES: {fixed_phones}')