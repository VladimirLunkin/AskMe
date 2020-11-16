from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(null=True)

    def __str__(self):
        return self.user_id.get_username()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Tag(models.Model):
    tag = models.CharField(max_length=32, verbose_name='Тег')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class QuestionManager(models.Manager):
    def get_queryset(self):
        return super(QuestionManager, self).get_queryset()

    def by_tag(self, tag):
        return super(QuestionManager, self).get_queryset().filter(tags__tag=tag)


class Question(models.Model):
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    tags = models.ManyToManyField(Tag)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    objects1 = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    is_correct = models.BooleanField(default=False, verbose_name='Чекбокс')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.question_id.title

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class LikeQuestion(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name='Лайк или дизлайк')

    def __str__(self):
        return self.profile_id.user_id.get_username() + ' лайкнул "' + self.question_id.title + '"'

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'


class LikeAnswer(models.Model):
    answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE)
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name='Лайк или дизлайк')

    def __str__(self):
        return self.profile_id.user_id.get_username() + ' лайкнул "' + self.answer_id.question_id.title + '"'

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
