from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
def same_user(user, email_path):
    return user.email == email_path

def get_list(email):
    try:
        list_ = List.objects.get(email=email)
    except:
        list_ = None
    return list_

def home_page(request):
    if request.user.is_authenticated:
        list_ = get_list(request.user.email)
        if list_ is not None:
            return redirect(list_)

    return render(request, 'index.html')

def view_list(request, email):
    list_ = get_list(email)
    error_message = None

    if not request.user.is_authenticated or list_ is None:
        return redirect('/')

    if not same_user(request.user, email):
        return redirect('/')

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['todo-item'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            item.delete()
            error_message = "You can't have an empty list item"

    return render(request, 'lists.html', {'list': list_, 'error': error_message})

def new_list(request):
    if request.user.is_authenticated and request.method == 'POST':
        list_ = List.objects.create(email=request.user.email)
        item = Item.objects.create(text=request.POST['todo-item'], list=list_)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            list_.delete()
            error_message = "You can't have an empty list item"
            return render(request,'index.html', {'error': error_message})
        return redirect(list_)

    return redirect('/')
