from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models import signals



class Category(models.Model):
    slug = models.CharField(max_length=128)
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.slug})'
class PriorityCount(models.Model):
    name = models.CharField(max_length=256)
    count = models.PositiveIntegerField(default=0)

class TodoItem(models.Model):
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3

    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, "Высокий приоритет"),
        (PRIORITY_MEDIUM, "Средний приоритет"),
        (PRIORITY_LOW, "Низкий приоритет"),
    ]

    description = models.TextField("описание")
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    priority = models.IntegerField(
        "Приоритет", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])

def create_todo(sender, instance, created, **kwargs):
    #получаем расчетные значения счетчиков или присваиваим им 0
    #высокий
    try:
        high_count = TodoItem.objects.filter(priority=1).count()
    except:
        high_count = 0
    #средний
    try:
        medium_count = TodoItem.objects.filter(priority=2).count()
    except:
        medium_count = 0
    #низкий
    try:
        low_count = TodoItem.objects.filter(priority=3).count()
    except:
        low_count = 0
    print ("Save is called")
    print ('Высокий: {} Средний: {} Низкий: {}'.format(high_count,medium_count,low_count))
    #блок сохранения высокого приоритета
    try:
        #получаем текщее значение из БД
        get_high_count = PriorityCount.objects.get(name='high_count')
        #присваиваем расчетное значение
        get_high_count.count = high_count
        #сохраняем
        get_high_count.save()
    except:
        #если в базе счетчика нет, то инициализируем его
        PriorityCount(name='high_count', count=high_count).save()
    #блок сохранения среднего приоритета
    try:
        #получаем текщее значение из БД
        get_medium_count = PriorityCount.objects.get(name='medium_count')
        #присваиваем расчетное значение
        get_medium_count.count = medium_count
        #сохраняем
        get_medium_count.save()
    except:
        #если в базе счетчика нет, то инициализируем его
        PriorityCount(name='medium_count', count=medium_count).save()
    #блок сохранения низкого приоритета
    try:
        #получаем текщее значение из БД
        get_low_count = PriorityCount.objects.get(name='low_count')
        #присваиваем расчетное значение
        get_low_count.count = low_count
        #сохраняем
        get_low_count.save()
    except:
        #если в базе счетчика нет, то инициализируем его
        PriorityCount(name='low_count', count=low_count).save()
    print ('Высокий: {} Средний: {} Низкий: {}'.format(PriorityCount.objects.get(name='high_count').count,PriorityCount.objects.get(name='medium_count').count,PriorityCount.objects.get(name='low_count').count))
signals.post_save.connect(create_todo, sender=TodoItem)