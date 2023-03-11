from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from .models import Task
from .forms import TaskForm

# Create your views here.


class IndexView(View):
    def get(self, request):
        return redirect("home")


class TasksView(View):
    @method_decorator(login_required)
    def get(self, request):
        tasks = Task.objects.filter(creator=request.user)
        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"
        return render(
            request,
            "tasks.html",
            {
                "base_template": base_template,
                "tasks_list": tasks,
                "show_all": "checked",
                "show_priorities": "",
                "title": "All Tasks",
            },
        )


class SearchTasksView(View):
    @method_decorator(login_required)
    def post(self, request):
        terms = request.POST.get("search")
        tasks = Task.objects.filter(creator=request.user).filter(
            Q(title__icontains=terms) | Q(body__icontains=terms)
        )
        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"
        return render(
            request,
            "tasks.html",
            {
                "base_template": base_template,
                "tasks_list": tasks,
                "show_all": "checked",
                "show_priorities": "",
                "title": "All Tasks",
            },
        )


class PriorityTasksView(View):
    @method_decorator(login_required)
    def get(self, request):
        tasks = Task.objects.filter(creator=request.user, is_priority=True)
        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"
        return render(
            request,
            "tasks.html",
            {
                "base_template": base_template,
                "tasks_list": tasks,
                "show_all": "",
                "show_priorities": "checked",
                "title": "Priority Tasks",
            },
        )


class TaskView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        task = Task.objects.filter(Q(id=pk) & Q(creator=request.user)).all()
        if task:
            task = Task.objects.get(pk=pk)
            if request.htmx:
                base_template = "main.html"
            else:
                base_template = "base.html"
            return render(
                request,
                "task.html",
                {
                    "base_template": base_template,
                    "task": task,
                },
            )
        else:

            return render(
                request,
                "no_task.html",
                {
                    "base_template": "base.html",
                },
            )


class TasksSaveView(View):
    @method_decorator(login_required)
    def post(self, request, pk=None):
        if pk:
            form = TaskForm(request.POST, instance=Task.objects.get(pk=pk))
        else:
            form = TaskForm(request.POST)
        if form.is_valid():
            task = form.customSave(commit=pk is None, creator=request.user)
            if pk:
                id = pk
            else:
                id = task.pk
            return redirect("task", id)

        context = {"base_template": "main.html", "form": form}
        return render(request, "task_form.html", context)


class TasksCreateView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = TaskForm()
        # task = Task.objects.last()
        if request.htmx:
            base_template = "main.html"
        else:
            base_template = "base.html"
        context = {
            "base_template": base_template,
            "form": form,
            "action": "Add Task",
            "url": f"{request.path}",
            "push_url": f"/task/create/",
        }
        return render(request, "task_form.html", context)

    def post(self, request):
        view = TasksSaveView.as_view()
        return view(request)


class TasksEditView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        task = Task.objects.filter(Q(id=pk) & Q(creator=request.user))
        if task:
            task = Task.objects.get(pk=pk)
            form = TaskForm(instance=task)
            if request.htmx:
                base_template = "main.html"
            else:
                base_template = "base.html"
            context = {
                "base_template": base_template,
                "form": form,
                "task": task,
                "action": "Edit",
                "url": f"{request.path}",
                "push_url": f"/task/{task.id}/",
            }
            return render(request, "task_form.html", context)
        else:

            return render(
                request,
                "no_task.html",
                {
                    "base_template": "base.html",
                },
            )

    def post(self, request, pk=None):
        view = TasksSaveView.as_view()
        return view(request, pk)


class TaskDelete(View):
    @method_decorator(login_required)
    def get(self, request, pk):

        task = Task.objects.filter(Q(id=pk) & Q(creator=request.user))
        if task:
            task = Task.objects.get(pk=pk)
            if request.htmx:
                base_template = "main.html"
            else:
                base_template = "base.html"
            context = {"base_template": base_template, "task": task}
            return render(request, "task_delete.html", context)
        else:
            return render(
                request,
                "no_task.html",
                {
                    "base_template": "base.html",
                },
            )

    @method_decorator(login_required)
    def post(self, request, pk):
        task = Task.objects.filter(Q(id=pk) & Q(creator=request.user))
        if task:
            task = Task.objects.get(pk=pk)
            task.delete()
            return redirect("home")
        else:
            return render(
                request,
                "no_task.html",
                {
                    "base_template": "base.html",
                },
            )
