from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category, Page

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
        context_dict['category']=None
        context_dict['pages']=None
        
    return render(request, 'rango/category.html', context_dict)

        
