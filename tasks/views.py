from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from tasks.models import TodoItem, Category,PriorityCount
import functools
import datetime
from django.views.decorators.cache import cache_page

@cache_page(300)
def time_view(request):
    data_now = datetime.datetime.now()
    return render(request, "tasks/time.html",{"data_now":data_now})


def index(request):

    # 1st version
    # counts = {t.name: random.randint(1, 100) for t in Tag.objects.all()}

    # 2nd version
    # counts = {t.name: t.taggit_taggeditem_items.count()
    # for t in Tag.objects.all()}

    # 3rd version
    #@functools.lru_cache
    from django.db.models import Count
    counts_tasks = Category.objects.annotate(total_tasks=Count('todoitem')).order_by("-total_tasks")
    #считаем высокий приоритет
    try:
        high_count = TodoItem.objects.filter(priority=1).count()
    except:
        high_count=0
    #считаем средний приоритет
    try:
        medium_count = TodoItem.objects.filter(priority=2).count()
    except:
        medium_count=0
    #считаем низкий приоритет
    try:
        low_count = TodoItem.objects.filter(priority=3).count()
    except:
        low_count=0
    #здесь мы делаем словарь имя категории - количество задач
    @functools.lru_cache
    def create_dic(counts):
        counts = {c.name: c.total_tasks for c in counts}
        return counts
    #берем значения счетчика приоритетов из объектов
    try:
        medium_count_signal = PriorityCount.objects.get(name='medium_count').count
    except:
        medium_count_signal = 0
    try:
        high_count_signal = PriorityCount.objects.get(name='high_count').count
    except:
        high_count_signal = 0
    try:
        low_count_signal = PriorityCount.objects.get(name='low_count').count
    except:
        low_count_signal = 0
    return render(request, "tasks/index.html", {"counts": create_dic(counts_tasks),
    "high_count":high_count,"medium_count":medium_count,"low_count":low_count, "high_count_signal": high_count_signal,"medium_count_signal":medium_count_signal,"low_count_signal":low_count_signal})
    #return render(request, "tasks/index.html", {"counts": counts})


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for t in user_tasks:
            tags.append(list(t.category.all()))

        categories = []
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)
        context["categories"] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"
