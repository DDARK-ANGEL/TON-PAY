from django.db import models


class Users(models.Model):
    name = models.TextField('Имя мерчанта')
    email = models.TextField('Email мерчанта')
    password = models.TextField('Пароль мерчанта')
    token = models.TextField('Токен')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Мерчант'
        verbose_name_plural = 'Мерчанты'
