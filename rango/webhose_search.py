import json
import urllib.parse
import urllib.request


class WebhoseMixin(object):
    
    def render_search_response(self, kwargs, **response_kwargs):
        form = kwargs['form']
        search_terms = form.cleaned_data['query']
        search_results = self.search_query(search_terms)
        kwargs['search_list'] = search_results
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=kwargs,
            using=self.template_engine,
            **response_kwargs
            )
        
    
    def search_query(self, search_terms):
        # Returns a list of 10 results from the Webhose API
        # from a string containing search terms (query).
        webhose_api_key = None
        try:
            with open('search.key', 'r') as f:
                webhose_api_key = f.readline().strip()
        except:
            raise IOError('Search key file not found')
        if not webhose_api_key:
            raise KeyError('Webhose key not found')
        # Base URL for the Webhose API
        root_url = 'http://webhose.io/filterWebContent'
        # Format the query string - escape special characters
        query_string = urllib.parse.quote(search_terms)
        # String formatting to construct the complete API URL
        search_url = ('{root_url}?token={key}&format=json&'
                      'ts=1505823665729&sort=crawled&size={size}&'
                      'q=language%3Aenglish%20{query}').format(
                          root_url=root_url, key=webhose_api_key,
                          query=query_string, size=8)
        results=[]
        try:
            #Convert the Webhose API response to a Python dictionary
            json_response = urllib.request.urlopen(search_url).read().decode('utf-8')
            dict_response = json.loads(json_response)
            #Append each post to the results list as a dictionary,
            #restricting the summary to the first 200 characters
            for post in dict_response['posts']:
                results.append({'title': post['title'],
                                'link': post['url'],
                                'summary': post['text'][:222]})
        except:
            print("Error when querying the Webhose API")
        # Return the list of results
        return results
