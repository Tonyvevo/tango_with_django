from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):
    request.session.set_test_cookie()
    # Query db for first 5 categories with highest likes
    category_list = Category.objects.order_by('-likes')[:5]
    # Query db for first 5 pages with most views
    page_list = Page.objects.order_by('-views')[:5]
    # Add these lists to the template context
    context_dict = {'categories': category_list,
                    'pages': page_list }

    # Helper function handles the cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
 

    # Obtain response object
    return render(request, 'rango/index.html',
                             context=context_dict)

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    # A dictionary to pass context to the template renderer
    context_dict = {'my_name': "TonyVEVO"}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    
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

@login_required
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

@login_required
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

def register(request):
    # Tells the template whether the registration was successful.
    registered = False

    # Process registration form data.
    if request.method == 'POST':
        # Grab information from the raw form data.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()
            # Hash the password and update the user object.
            user.set_password(user.password)
            user.save()
            # Delay saving the user UserProfile instance
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            # If a profile picture is provided in the user form data,
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.save()
                # Indicate that template registration was successful
                registered = True
        else:
            # Invalid form(s) and/or other problems
            print(user_form.errors, profile_form.errors)
    else:
        # Render a blank form using our two ModelForm instances.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # Obtain the username & password from the login form.
        # Use request.POST.get('variable') to return None if the
        # value does not exist instead of a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check the username/password combination and return a
        # User object if ir is valid.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None, no matching credentials were found.
        if user:
            # Is the user account active or disabled?
            if user.is_active:
                # Log the user in & send them back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used.
                return HttpResponse("Your Rango account was disabled.")
        else:
            # Bad login details were provided.
            print("Invalid login details: {0}, {1}".format(username,
                                                           password))
            return HttpResponse("Invalid login details supplied.")
    # If the request is not a HTTP POST..
    else:
        # Display a blank login form
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# Site counter helper function
def visitor_cookie_handler(request):
    # Use the COOKIES.get() function to obtain the visits cookie.
    # Cast the value returned to an integer or set the value to
    # 1 if the cookie doesn't exist.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit',
                                            str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # if it's been more than a day since the last visit..
    if (datetime.now() - last_visit_time).days > 0:
        # Update the cookie visits count & last_visit time
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits
    
# Helper function that asks the request for a cookie
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

