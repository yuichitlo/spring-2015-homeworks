import requests
import xml.dom.minidom

#key = ""
#with open('key.txt','r') as f:
#    key = f.readline().strip()

#if len(key) > 0:
#    print "Succesfully retrieved API key"

#response = requests.get("http://api.nytimes.com/svc/books/v3/lists/names.xml?api-key=%s"%(key))
response = requests.get("http://api.nytimes.com/svc/books/v3/lists/2014-06-21/hardcover-fiction.json?api-key=%s"%(key))
#xml_parser = xml.dom.minidom.parseString(response.text)
#pretty_response = xml_parser.toprettyxml()

#def print_names_from_XML(response):
def print_names_from_XML(pretty_response):
    """Prints the names of all the best-seller lists that are in the response.
    
    Parameters:
        response: Response object
        The response object that is a result of a get request for the names of the
        best-selling lists from the Books API. 
    
    """   
    #xml_parser = xml.dom.minidom.parseString(response.text)
    #pretty_response = xml_parser.toprettyxml().split('\n')

    pretty_response_clean = pretty_response.split('\n')
    for section in pretty_response_clean:
        section = section.strip('u\'').strip('\t')
        if section.startswith('<list_name>'):
            print section.strip('<list_name>').strip('</')
    

#response = requests.get("http://api.nytimes.com/svc/books/v3/lists/names.xml?api-key=%s"%(key))
#print_names_from_XML(response)

def print_names_from_JSON(response):
    """Prints the names of all the best-seller lists that are in the response.
    
    Parameters:
        response: Response object
        The response object that is a result of a get request for the names of the
        best-selling lists from the Books API. 
    
    """     
    response = response.json()
    names = [section['list_name'] for section in response['results']]
    
    for name in names:
        print name

def print_list_from_date(date):
    date = '2014-06-21'
    response = requests.get('http://api.nytimes.com/svc/books/v3/lists/' + date + '/hardcover-fiction.json?api-key=%s'%(key))
    response = response.json()

    print 'Number of books: ' + response['num_results']
    print 'List date: ' + date
    print

    names = [book['title'] for book in response['results']['books']]

    response = requests.get('http://api.nytimes.com/svc/books/v3/lists/' + date + '/hardcover-fiction.json?offset=20&api-key=%s'%(key))
    response = response.json()

    names += [book['title'] for book in response['results']['books']]

    for name in names:
        print name

import datetime
import time

import datetime
import time

def get_books(date, list_name):
    """Returns a tuple containing the list of books and the publication date of the list
    
    Parameters:
        date: datetime
            The day for which  we want to check the best-selling list.
    
        list_name: string
            The name of best-selling list that want to check. This needs to follow
            the Books API guidelines, e.g. 'hardcore-fiction'.
    
    Returns:
        books_set: set
            The set of books that were best-sellers according to NYT.
        
        published_date: datetime
            The date on which the list was published.
            
    """
    
    response = requests.get('http://api.nytimes.com/svc/books/v3/lists/%s/%s.json?api-key=%s'%(str(date), list_name, key))
    response = response.json()

    num_results = response['num_results']
    fetched = 20
    names = [book['title'] for book in response['results']['books']]

    while num_results > fetched:
        time.sleep(0.125)
        response = requests.get('http://api.nytimes.com/svc/books/v3/lists/%s/%s.json?offset=%d&api-key=%s'%(str(date), list_name, fetched, key))
        response = response.json()
        names += [book['title'] for book in response['results']['books']]
        fetched += 20

    return set(names), datetime.datetime.strptime(response['results']['published_date'], "%Y-%m-%d")

    import datetime

def most_popular(start_date, end_date, list_name):
    """Returns the books and the number of weeks that were best-sellers for the given time window
    
    Parameters:
        start_date: datetime
            The first day to check.
        
        end_date: datetime
            The last day to check.
            
        list_name: string
            The name of best-selling list that want to check. This needs to follow
            the Books API guidelines, e.g. 'hardcore-fiction'.
    
    Returns:
        books_dict: dictionary
            Dictionary of book titles with the number of weeks on the requested NYT
    """

    books_dict = {}
    cur_date = start_date

    while cur_date <= end_date:
        book_list, book_date = get_books(cur_date, list_name)

        for book in book_list:
            if book not in books_dict:
                books_dict[book] = 1
            else:
                books_dict[book] += 1

        cur_date = cur_date + datetime.timedelta(weeks=1)

    return books_dict