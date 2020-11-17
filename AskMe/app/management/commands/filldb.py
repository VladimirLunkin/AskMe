from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag
from random import sample
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
        # try:
        #     self.fill_profile(options['users'][0])
        # except Profile.DoesNotExist:
        #     raise CommandError('Users does not exist')

        # try:
        #     self.fill_tag(options['tags'][0])
        # except Tag.DoesNotExist:
        #     raise CommandError('Users does not exist')

        try:
            self.fill_questions(options['questions'][0])
        except Question.DoesNotExist:
            raise CommandError('Users does not exist')

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
        profile_count = Profile.objects.count() - 1
        for i in range(cnt):
            q = Question.objects1.create(
                profile_id=Profile.objects.get(id=i+1),#f.random_int(min=1, max=profile_count)),
                title=f.sentence(),
                text=f.text(),
                # tags=Tag.objects.filter(id__in=sample(list(Tag.objects.all()), k=f.random_int(min=1, max=3))),
            )
            q.tags.set(Tag.objects.create_question()),

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
