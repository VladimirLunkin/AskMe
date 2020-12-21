from django.db import models
from django.contrib.auth.models import User
from random import sample, randint


class ProfileManager(models.Manager):
    def sample_profile(self, count):
        profile_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        return Profile.objects.filter(id__in=sample(profile_ids, k=count))


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name='Профиль')
    avatar = models.ImageField(default='img/no_avatar.png', verbose_name='Аватар')

    objects = ProfileManager()

    def __str__(self):
        return self.user_id.get_username()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class TagManager(models.Manager):
    def create_question(self):
        tag_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        return Tag.objects.filter(id__in=sample(tag_ids, k=randint(1, 3)))


class Tag(models.Model):
    tag = models.CharField(max_length=32, verbose_name='Тег')

    objects = TagManager()

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def all(self):
        return self.order_by('-date_create')

    def by_tag(self, tag):
        return self.filter(tags__tag=tag).order_by('-date_create')

    def hot(self):
        return self.order_by('-like', '-date_create')


class Question(models.Model):
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст вопроса')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    like = models.IntegerField(default=0, verbose_name='Лайки')
    number_of_answers = models.IntegerField(default=0, verbose_name='Количество ответов')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerManager(models.Manager):
    def by_question(self, pk):
        return self.filter(question_id=pk).order_by('-like', 'date_create')


class Answer(models.Model):
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор')
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    text = models.TextField(verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Корректность ответа')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    like = models.IntegerField(default=0, verbose_name='Лайки')

    objects = AnswerManager()

    def __str__(self):
        return self.question_id.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.question_id.number_of_answers += 1
            self.question_id.save()
        super(Answer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.question_id.number_of_answers -= 1
        self.question_id.save()
        super(Answer, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class LikeQuestion(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос')
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Профиль')
    is_like = models.BooleanField(default=True, verbose_name='Лайк или дизлайк')

    def __str__(self):
        return self.profile_id.user_id.get_username() + ' лайкнул "' + self.question_id.title + '"'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_like:
                self.question_id.like += 1
            else:
                self.question_id.like -= 1
            self.question_id.save()
        super(LikeQuestion, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_like:
            self.question_id.like -= 1
        else:
            self.question_id.like += 1
        self.question_id.save()
        super(LikeQuestion, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ('question_id', 'profile_id')
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'


class LikeAnswer(models.Model):
    answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='Ответ')
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Профиль')
    is_like = models.BooleanField(default=True, verbose_name='Лайк или дизлайк')

    def __str__(self):
        return self.profile_id.user_id.get_username() + ' лайкнул "' + self.answer_id.question_id.title + '"'

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_like:
                self.answer_id.like += 1
            else:
                self.answer_id.like -= 1
            self.answer_id.save()
        super(LikeAnswer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_like:
            self.answer_id.like -= 1
        else:
            self.answer_id.like += 1
        self.answer_id.save()
        super(LikeAnswer, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ('answer_id', 'profile_id')
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
