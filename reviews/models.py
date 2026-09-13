from django.db import models
from users.models import CustomUser
from ads.models import Advertisement

class Review(models.Model):

    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(to=CustomUser,
                               on_delete=models.SET_NULL,
                               verbose_name="Автор отзыва",
                               related_name="reviews",
                               null=True)
    ad = models.ForeignKey(to=Advertisement,
                           on_delete=models.CASCADE,
                           verbose_name="Объявление",
                           related_name="reviews"
                           )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата и время создания отзыва")
