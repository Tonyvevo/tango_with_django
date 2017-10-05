import json
import urllib.parse
import urllib.request

def read_webhose_key():
    #Reads the Webhose API key from a file called 'search.key'
    #Returns either None or a string representing the key.
    webhose_api_key = None

    try:
        with open('search.key', 'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, size=10):
    # Returns a list of 10 results from the Webhose API
    # from a string containing search terms (query).
    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    # Base URL for the Webhose API
    root_url = 'http://webhose.io/filterWebContent'

    # Format the query string - escape special characters
    query_string = urllib.parse.quote(search_terms)
    

    # String formatting to construct the complete API URL
    search_url = ('{root_url}?token={key}&format=json&'
                  'ts=1504567985771&sort=relevancy&size={size}&'
                  'q=language%3Aenglish%20{query}').format(
                      root_url=root_url, key=webhose_api_key,
                      query=query_string, size=size)


    results=[]

    try:
        #Convert the Webhose API response to a Python dictionary
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        # Append each post to the results list as a dictionary,
        # restricting the summary to the first 200 characters
        for post in json_response['posts']:
            results.append({'title': post['title'],
                           'link': post['url'],
                           'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    # Return the list of results
    return results
