from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from rango.views import IndexView, AboutView, ShowCategoryView, AddCategoryView
from rango.views import AddPageView, RestrictedView, WebSearchView
from rango.views import TrackUrlView, RegisterProfile 
from rango import views

app_name = 'rango'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^add_category/$', login_required(AddCategoryView.as_view()),
        name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        ShowCategoryView.as_view(), name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',
        login_required(AddPageView.as_view()), name='add_page'),
    url(r'^restricted/$', login_required(RestrictedView.as_view()),
        name='restricted' ),
    url(r'^search/$', login_required(WebSearchView.as_view()), name='search'),
    url(r'^goto/$', TrackUrlView.as_view(), name='goto'),
    url(r'^register_profile/$', login_required(RegisterProfile.as_view()),
        name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profiles/$', views.list_profiles, name='list_profiles'),
]
