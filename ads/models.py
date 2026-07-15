from django.db import models
from users.models import CustomUser

class Advertisement(models.Model):

    title = models.CharField(max_length=150, verbose_name="Название")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(to=CustomUser,
                               related_name="advertisements",
                               on_delete=models.CASCADE,
                               verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
