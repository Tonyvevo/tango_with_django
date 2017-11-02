import inflection
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseGone
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import RedirectView


from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.forms import SearchForm
from rango.webhose_search import WebhoseMixin


class IndexView(TemplateView):    
    template_name = "rango/index.html"

    def get_context_data(self, **kwargs):
        # Test cookie to determine brower cookie support
        self.request.session.set_test_cookie()
        # Helper function to handle the cookies
        # Query db for first 5 categories with highest likes
        category_list = Category.objects.order_by('-likes')[:5]
        # Query db for first 5 pages with most views
        page_list = Page.objects.order_by('-views')[:5]
        # Create proxy object for the template context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Add these lists to the context
        context['categories'] = category_list
        context['pages'] = page_list
        # Add the number of session visits to the context
        context['visits'] = self.visitor_cookie_handler(self.request)

        # Obtain response object
        return context

    # Site counter helper function
    def visitor_cookie_handler(self, request):
        # Use the COOKIES.get() function to obtain the visits cookie.
        # Cast the value returned to an integer or set the value to
        # 1 if the cookie doesn't exist.
        visits = int(self.get_server_side_cookie(request, 'visits', '1'))
        last_visit_cookie = self.get_server_side_cookie(request, 'last_visit',
                                                str(datetime.now()))
        last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                            '%Y-%m-%d %H:%M:%S')
        # if it's been more than a day since the last visit..
        if (datetime.now() - last_visit_time).seconds >= 86400:
            # Update the cookie visits count & last_visit time
            visits = visits + 1
            request.session['last_visit'] = str(datetime.now())
            # Set the last visit cookie
            request.session['last_visit'] = last_visit_cookie
            # Update/set the visits cookie
            request.session['visits'] = visits
        visits = inflection.ordinalize(visits)
        return visits
    
    # Helper function that asks the request for a cookie
    def get_server_side_cookie(self, request, cookie, default_val=None):
        val = request.session.get(cookie)
        if not val:
            val = default_val
        return val
   

class AboutView(TemplateView):    
    template_name = "rango/about.html"
    
    def get_context_data(self, **kwargs):
        if self.request.session.test_cookie_worked():
            print("TEST COOKIE WORKED!")
            self.request.session.delete_test_cookie()
        # Create proxy object for the template context
        context = super(AboutView, self).get_context_data(**kwargs)
        context['my_name'] = "TonyVEVO"
        return context
    

class ShowCategoryView(WebhoseMixin, TemplateView, FormView):
    template_name = "rango/category.html"
    model = Category, Page
    form_class = SearchForm
    
    def get_context_data(self, category_name_slug, **kwargs):
        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')
        except Category.DoesNotExist:
            category = None
            pages = None
        kwargs['category'] = category
        kwargs['pages'] = pages        
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs
    
    def form_invalid(self, category_name_slug, query):
        return self.render_to_response(self.get_context_data(
            category_name_slug, form=query))

    def form_valid(self, category_name_slug, query):
        return self.render_search_response(self.get_context_data(
            category_name_slug, form=query))
        
    def post(self, request, *args, **kwargs):
        category_name_slug = kwargs['category_name_slug']
        query = self.get_form()
        if query.is_valid():
            return self.form_valid(category_name_slug, query)
        else:
            return self.form_invalid(category_name_slug, query)


class AddCategoryView(FormView):
    template_name = "rango/add_category.html"
    form_class = CategoryForm
    success_url = "/rango/"

    def form_valid(self, form):
        form.save(commit=True)
        # Direct the user back to the index page
        return super(AddCategoryView, self).form_valid(form)

    def form_invalid(self, form):
        # Print errors in the supplied form on the terminal
        print(form.errors)
        return super(AddCategoryView, self).form_invalid(form)

    
class AddPageView(FormView, TemplateView):     
    template_name = "rango/add_page.html"
    model = Page, Category
    form_class = PageForm

    def get_context_data(self, category_name_slug, **kwargs):
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None
        kwargs['category'] = category
        
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def form_invalid(self, form, category_name_slug):
        return self.render_to_response(self.get_context_data(
            category_name_slug, form=form))        

    def form_valid(self, form, category_name_slug):
        page = form.save(commit=False)
        category = Category.objects.get(slug=category_name_slug)
        page.category = category
        page.save()
        return HttpResponseRedirect(self.get_success_url(
            category_name_slug))
    
    def get_success_url(self, category_name_slug):
        self.success_url = "/rango/category/{}/".format(category_name_slug)
        if self.success_url:
            url = self.success_url
        else:
            raise improperlyConfigured(
                "No URL to redirect to. Provide a success URL"
                )
        return url

    def post(self, request, category_name_slug, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, category_name_slug)
        else:
            return self.form_invalid(form, category_name_slug)      

            
class RestrictedView(TemplateView):
    template_name = "rango/restricted.html"
    def get_context_data(self, **kwargs):
        return super(RestrictedView, self).get_context_data(**kwargs)


class PageSearchView(FormView):
    form_class = SearchForm
    template_name = "rango/search.html"

    def get_context_data(self, query=None, **kwargs):
        context = {}
        context['form'] = self.get_form()
        if query:
            context['query'] = query
            context['result_list'] = self.get_queryset(query)
        return context
    
    def get_queryset(self, query):
        page_list = Page.objects.filter(title__icontains=query)
        queryset = []
        for page in page_list:
            queryset.append(page)
        self.queryset = queryset

        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                        }
                    )
        return queryset
                
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        query = request.POST.get('query')
        return self.render_to_response(self.get_context_data(
            query=query, form=form))
    
    
class TrackUrlView(RedirectView):
    url = "/rango/"
    def get(self, request, *args, **kwargs):
        url = None
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views+=1
                page.save()
                url = page.url
            except:
                pass
        if url:
            if self.permanent:
                return http.HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            try:
                url = self.get_redirect_url(*args, **kwargs)
                return HttpResponseredirect(url)
            except:
                logger.warning(
                    'Gone: %s', request.path,
                    extra={'status_code':410, 'request': request}
                )
            return HttpResponseGone()
        
            
class RegisterProfile(FormView):
    form_class = UserProfileForm
    template_name = "rango/profile_registration.html"
    success_url = "/rango/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
    return render(request, 'rango/profile.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'rango/list_profiles.html',
                  {'userprofile_list': userprofile_list})

@login_required
def like_category(request):
    cat_id = None
    if request.method == "GET":
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    response = "{} people like this category".format(likes)
    return HttpResponse(response)

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list

def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cats': cat_list})

@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category,
                                           title=title, url=url)
            pages = Page.objects.filter(category=category).order_by('-views')
            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages
    return render(request, 'rango/page_list.html', context_dict)
