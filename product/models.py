from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ticket(models.Model):
    title = models.CharField(
        max_length=123,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена билета'
    )
    logo = models.ImageField(
        upload_to='media/ticket_logos',
        verbose_name='Логотип'
    )
    event_date = models.DateTimeField(
        verbose_name='Дата начало мероприятия'
    )
    duration = models.CharField(
        max_length=30,
        verbose_name='Прододжительнось'
    )
    location = models.CharField(
        max_length=223,
        verbose_name='Место проведения'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Кол-во билетов'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создание объекта',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Пользователь'
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.PROTECT,
        verbose_name='Билет'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Кол-во'
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Заказ в обработке'),
            (2, 'Заказ выполнен'),
            (3, 'Заказ отклонен')
        ),
        default=1,
        verbose_name='Статус'
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Общая цена'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return str(self.user)








