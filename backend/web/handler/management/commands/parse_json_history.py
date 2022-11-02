from django.core.management import BaseCommand, CommandError
from handler.models import User, Session, Entry
from datetime import datetime
import random
from django.utils.timezone import make_aware
from utils.get_entries import SessionList, session_history
from utils.get_user_history import entries
import pandas as pd


class Command(BaseCommand):
    help = 'Parses user history data and adds to database'

    # internal function to grab random user ID's
    @staticmethod
    def __random_userid(n: int):
        if n == 1:
            return random.randint(10000, 99999)
        else:
            for i in range(n):
                yield random.randint(10000, 99999)

    @staticmethod
    def __usec_ts(stamp):
        times = stamp / 1000000
        naive = datetime.utcfromtimestamp(times)
        aware_datetime = make_aware(naive)
        return aware_datetime

    # internal function to grab random user ID's
    def add_arguments(self, parser):
        parser.add_argument('--file',
                            type=str,
                            action='store',
                            help='What file should be loaded',
                            dest='data',
                            default='cleaned_history_.json'
                            )

        parser.add_argument('--root-data-folder',
                            type=str,
                            action='store',
                            help='If using a different root folder other than /data/user_data/',
                            default='/data/user_data',
                            dest='root_data_folder'
                            )

    def handle(self, *args, **options):
        sessions = session_history(options['root_data_folder'] + '/' + options['data'])
        user_id = random.randint(10000, 99999)

        # Create User object
        try:
            User.objects.create(user_id=user_id)

        except Exception as e:
            raise CommandError(f'User with user_id {user_id} does not exist.', e)
        # Create Session Objects:

        # Add Sesssions
        # y = 0
        # x = 0
        # for session in sessions:
        #     session_id = random.randint(10000, 99999)
        #     new_session = Session.objects.create(session_id=session_id, user=user_id)
        #     for entry in session:
        #         try:
        #             related_entry = Entry.objects.get(entry_id=int(str(entry['id'])+str(user_id)))
        #             related_entry.session = new_session
        #             related_entry.save(update_fields=['session'])
        #             x += 1
        #         except Entry.DoesNotExist:
        #             raise CommandError(f'Entry with entry_id {entry[0]} does not exist.')
        #     y += 1
        #
        # self.stdout.write(self.style.SUCCESS(
        #      f'Added {y} sessions for user {user_id} containing {x} entries.'))

        # Create Entries
        #{'id': 322,
        # 'favicon_url': 'https://www.tv2.no/view-resources/baseview/public/common/lab_assets/img/favicon/favicon.ico',
        # 'page_transition': 'LINK',
        # 'title': 'Lasse Matberg måtte flytte fra egen leilighet på…',
        # 'url': 'https://www.tv2.no/underholdning/lasse-matberg-matte-flytte-fra-egen-leilighet-pa-grunn-av-paparazzi/15037658/',
        # 'client_id': 'Iiteen/E0kB7QdKeRu1j8Q==',
        # 'time_usec': 1661348929445939,
        # 'link': 'www.tv2.no'}
        i = 0
        for entry in entries(options['root_data_folder'] + '/' + options['data']):

            new_entry = Entry.objects.create(entry_id=int(str(entry['id'])+str(user_id)),
                                             favicon=entry['favicon_url'],
                                             url=entry['url'],
                                             usec=self.__usec_ts(entry['time_usec']),
                                             page_transition=entry['page_transition'],
                                             client_id=entry['client_id'],
                                             source=entry['link'],
                                             user=User.objects.get(user_id=user_id))

            i += 1
            new_entry.save()
            if i % 50 == 0:
                self.stdout.write(self.style.SUCCESS(
                         f'Added {i} entries for user {user_id}'))
            # except Exception as e:
            #     raise CommandError(f'Error ingesting {entry}', e)

        self.stdout.write(self.style.SUCCESS(
                     f'Added {i} entries for user {user_id}'))
        #   new_entry = Entry.objects.create(entry_id=int(str(entry['id'])+str(user_id)),
        # Add Sesssions
        y = 0
        x = 0
        session_length = len(sessions)
        for session in sessions:
            session_id = random.randint(10000, 99999)
            new_session = Session.objects.create(session_id=session_id, user=User.objects.get(user_id=user_id), total_time = session.total_time)
            for entry in session.as_list():
                try:
                    related_entry = Entry.objects.get(entry_id=int(str(entry[0])+str(user_id)))
                    related_entry.session = new_session
                    related_entry.save(update_fields=['session'])
                    x += 1
                    if x % 100 == 0:
                        self.stdout.write(self.style.WARNING(
                            f'Session {session_id} is long: processed {x}'))

                except Entry.DoesNotExist:
                    raise CommandError(f'Entry with entry_id {entry[0]} does not exist.')
            y += 1
            if session_length > 200:
                if y % 50 == 0:
                    self.stdout.write(self.style.SUCCESS(
                     f'{y} / {session_length} processed'))
            else:
                self.stdout.write(self.style.SUCCESS(
                     f'{y} / {session_length} processed'))

        self.stdout.write(self.style.SUCCESS(
             f'Added {y} sessions for user {user_id} containing {x} entries.'))





