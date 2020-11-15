from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(null=True)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Questions(models.Model):
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Questions', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст')
    is_correct = models.BooleanField(verbose_name='Чекбокс')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.question_id

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class Tag(models.Model):
    question_id = models.ManyToManyField('Questions')
    tag = models.CharField(max_length=32, verbose_name='Тэг')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

class Like(models.Model):
    question_id = models.ForeignKey('Questions', on_delete=models.CASCADE)
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
