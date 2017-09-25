from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):    
    # Query db for first 5 categories with highest likes
    category_list = Category.objects.order_by('-likes')[:5]
    # Query db for first 5 pages with most views
    page_list = Page.objects.order_by('-views')[:5]
    # Add these lists to the template context
    context_dict = {'categories': category_list,
                    'pages': page_list}
    
    return render(request, 'rango/index.html', context=context_dict)

def about(request):    
    # A dictionary to pass my name to the template renderer
    context_dict = {'my_name': "TonyVEVO"}
    
    return render (request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    # The context dictionary to pass to the template renderer
    context_dict = {}

    try:
        # Try to find a category with the provided name-slug 
        category = Category.objects.get(slug=category_name_slug)
        # Retreive all pages associated to the given category
        pages = Page.objects.filter(category=category)
        # Add the list of pages to the template context
        context_dict['pages'] = pages
        # Add the existing category object to the template context
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Add None to the template context
        # for the non-existing category
        context_dict['category'] = None
        context_dict['pages'] = None
        
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    #initiate form instance to handle POST requests
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # Direct the user back to the index page
            return index(request)
        else:
            # Print errors in the supplied form on the terminal
            print(form.errors)
            
    # Render a new form for GET requests or the form with errors
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return show_category(request, category_name_slug)

        else:
                print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

