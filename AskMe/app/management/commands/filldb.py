from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag
from random import choice
from faker import Faker

f = Faker()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--users', nargs='+', type=int)
        parser.add_argument('--questions', nargs='+', type=int)
        parser.add_argument('--answers', nargs='+', type=int)
        parser.add_argument('--tags', nargs='+', type=int)

        parser.add_argument('--db_size', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            users = options['users'][0]
            tags = options['tags'][0]
            questions = options['questions'][0]
        except Poll.DoesNotExist:
            raise CommandError('Users does not exist')
        self.fill_profile(users)
        self.fill_tag(tags)
        self.fill_questions(questions)
        #self.fill_profile(users)

        self.stdout.write(self.style.SUCCESS('Successfully closed poll '))

    @staticmethod
    def fill_profile(cnt):
        for i in range(cnt):
            Profile.objects.create(
                user_id=User.objects.create(
                    username=f.user_name(),
                    email=f.email(),
                    password=1
                ),
                avatar="img/ava" + str(i % 7) + ".png",
            )

    @staticmethod
    def fill_tag(cnt):
        for i in range(cnt):
            Tag.objects.create(
                tag=f.word(),
            )

    @staticmethod
    def fill_questions(cnt):
        profile_ids = list(
            Tag.objects.values_list(
                'pk', flat=True
            )
        )
        tag_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        profile_count = Profile.objects.cou
        for i in range(cnt):
            Question.objects1.create(
                profile_id=Profile.objects.get(id=randint(1, )),
                title=f.sentence(),
                text=f.text(),
                # tags=,
            )

    # @staticmethod
    # def fill_profile(cnt):
    #     user_ids = list(
    #         User.objects.values_list(
    #             'id', flat=True
    #         )
    #     )
    #     print(user_ids)
    #     print(User.objects.all())
    #     v = Profile.objects.count() + 1
    #     for i in range(cnt):
    #         Profile.objects.create(
    #             user_id=choice(user_ids),  #User.objects.get(id=i+1)+v, #user_ids[i], #
    #             avatar="img/ava" + str(i % 7) + ".png",
    #         )
