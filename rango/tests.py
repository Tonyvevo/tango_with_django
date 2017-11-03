from datetime import datetime
import pytz

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from rango.models import Category, Page


class CategoryMethodTests(TestCase):
    
    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should results True for categories
        where views are zero or positive
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)
        
    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add
        a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        cat = Category(name='Random Category String', views=0, likes=0)
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')
        

class IndexViewTests(TestCase):

    def test_index_view_with_no_category(self):
        """
        If no questions exist, an appropriate message should be displayed
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def add_cat(self, name, views, likes):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c

    def test_index_view_with_categories(self):
        """
        Check to make sure that the index has categories displayed
        """
        self.add_cat('test',1,1)
        self.add_cat('temp',1,1)
        self.add_cat('tmp',1,1)
        self.add_cat('tmp test temp',1,1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)

    def test_future_first_or_last_visit(self):
        """
        Check to ensure last visit is not in the future
        """
        page = Page(category=self.add_cat('time',2,2), title='timer', 
                    url = 'http://example.com', views=32,
                    last_visit=datetime(2030, 5, 12, 23))
        page.save()
        aware_last_visit = page.last_visit.replace(tzinfo=pytz.UTC)
        self.assertEqual((page.last_visit <= datetime.now()), True)
        self.assertEqual((aware_last_visit >= page.first_visit), True)
      
