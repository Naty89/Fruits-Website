# Fruits-Website

This website project was made using the django framework. It has a list of fruits and the origin of the fruits. Furthermore, there is a form that allows a person to add to the fruit list by uploading a picture of the fruit, the name, and the origin. Another feature that is on website is that a user is able to search for a fruit by its name or origin along with their pictures. Additionally, I used pagination in order to organize the list of fruits.


## Installation

The project has requirement.txt file that needs to be installed before launching website

```bash
pip install requirement.txt
```

## Form

When a user is inserting a new fruit to the website using the form, I made it so that it checks that fruit isn't in the sqlite database. If the fruit that user is trying to add is not in the database, then the new fruit is added to the database with all its attributes.

```bash
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
```            

## Search Feature

The user is able to search for a fruit by searching for its name or its origin. The search feature works by getting the request for the fruit and making it a variable.

```bash
def search(request):
    template = 'fruits/search_results.html'
    query = request.GET.get('fruit')
```

Afterwards, we filter through the fruit database by using the fruit name or the origin.

```bash
    if query:
        results = Fruit.objects.filter(Q(name__icontains=query) |
                                       Q(origin__icontains=query))
```

## Pagination

In order to allow pagination on the website, I used the Pagination library that came included with the django framework. To achieve pagination you need to give it all the fruit objects, and also the desired amount of objects you want displayed on one page.

```bash
def index(request):
    # os.system('python Fruit/media/images.py')
    fruits = Fruit.objects.all()

    paginator = Paginator(fruits, 5)
    page = request.GET.get('page')

    fruits = paginator.get_page(page)

    return render(request, 'fruits/index.html', {'fruits': fruits})
```

I then used css to prettify the page (code can be seen in templates/css/pagination.css)

This was a very fun project and I was able to learn a lot of things throughout the process
