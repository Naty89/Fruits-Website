from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Fruit
import os
import sqlite3
from PIL import Image
from .forms import FruitData
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages


# Create your views here.
def index(request):
    # os.system('python Fruit/media/images.py')
    fruits = Fruit.objects.all()

    paginator = Paginator(fruits, 5)
    page = request.GET.get('page')

    fruits = paginator.get_page(page)

    return render(request, 'fruits/index.html', {'fruits': fruits})


def insert(request):
    if request.method == 'POST':
        form = FruitData(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            dire = os.getcwd()
            db = sqlite3.connect(f'{dire}/db.sqlite3')
            conn = db.cursor()
            conn.execute("select * from App_fruit")
            fruit_list = []
            for fruit in conn.fetchall():
                fruit_list.append(fruit[1])

            if name in fruit_list:
                form = FruitData()
            else:
                form.save()

            for filename in os.listdir(f'{dire}/media/images/'):
                img = Image.open(f'{dire}/media/images/{filename}')
                if img.size != (100, 75):
                    new_img = img.resize((100, 75))
                    clean = os.path.splitext(filename)[0]
                    new_img.save(f'{dire}/media/images/{clean}_new.jpg', 'JPEG')
                    print('all done')
                    os.rename(f'{dire}/media/images/{clean}_new.jpg', f'{dire}/media/images/{filename}')

            img_obj = form.instance
            return render(request, 'fruits/form.html', {'form': form, 'img_obj': img_obj})

    else:
        form = FruitData()
    return render(request, 'fruits/form.html', {'form': form})


def search(request):
    template = 'fruits/search_results.html'
    query = request.GET.get('q')

    if query:
        results = Fruit.objects.filter(Q(name__icontains=query) |
                                       Q(origin__icontains=query))
        if results:
            paginator = Paginator(results, 5)
            page = request.GET.get('page')
            results = paginator.get_page(page)
            return render(request, template, {'results': results})
        else:
            messages.error(request, 'no results found')
    else:
        return HttpResponseRedirect('/search/')