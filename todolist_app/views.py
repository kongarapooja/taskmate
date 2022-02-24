from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import tasklist
from todolist_app.forms import TaskForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def todolist(request):
    if request.method =="POST":
        form=TaskForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.manager=request.user
            instance.save()
        return redirect('todolist')
    else:
        all_tasks=tasklist.objects.filter(manager=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        context={"todolist_text":"Welcome to TODOLIST Homepage",}
        return render(request,'todolist.html',{'all_tasks':all_tasks})
@login_required
def delete_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.manager== request.user:
           task.delete()
    else:
        return redirect('todolist')
@login_required
def complete_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    if task.maager==request.user:
        task.done=True
        task.save()
    else:
      return redirect('todolist')
@login_required
def pending_task(request,task_id):
    task=tasklist.objects.get(pk=task_id)
    task.done=False
    task.save()
    return redirect('todolist')
@login_required
def edit_task(request,task_id):
    if request.method=="POST":
                task = tasklist.objects.get(pk=task_id)
                form = TaskForm(request.POST or None,instance=task)
                if form.is_valid():
                    form.save()
                return redirect('todolist')
    else:
        task_obj=tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})

def contact(request):
    context={"contact_text":"Welcome to TODOLIST contact",
             "Home":"Welcome to Homepage"

    }
    return render(request,'contact.html',context)

def about(request):
    context={"about_text":"Welcome to TODOLIST About",
             "Home":"Welcome to Homepage"

    }
    return render(request,'about.html',context)
def index(request):
    context={"index_text":"Welcome to TODOLIST Index",
             "Home":"Welcome to Indexpage"

    }
    return render(request,'index.html',context)