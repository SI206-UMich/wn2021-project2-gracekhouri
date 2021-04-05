from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    with open(filename) as f:
        lines = f.read()
    soup = BeautifulSoup(lines, 'lxml')
    title_list = []
    author_list = []
    tup_list = []
    title_tags = soup.find_all('a', class_ = 'bookTitle')
    for a_tags in title_tags:
        #a_tags = a_tags.strip()
        title_list.append(a_tags.text.strip())
    author_tags = soup.find_all('span', itemprop = 'author')
    for tag in author_tags:
        #tag = tag.strip()
        author_list.append(tag.text.strip())
    for i in range(len(title_list)):
        tup_list.append((title_list[i], author_list[i]))
    return tup_list


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    url_list = []
    url_tags = soup.find_all('a', class_ = 'bookTitle')
    for link in url_tags:
        if link.get("href").startswith("/book/show/"):
            url_list.append("https://www.goodreads.com" + link.get("href"))
    return url_list[:10]
    


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    book_title = soup.find('h1', id = 'bookTitle').text.strip()
    book_author_anchor = soup.find('div', class_ = 'authorName__container')
    book_author = book_author_anchor.find('span').text.strip()
    book_pages = int(soup.find('span', itemprop = 'numberOfPages').text.strip()[:-6])
    tup = (book_title, book_author, book_pages)
    return tup


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    with open(filepath) as f:
        lines = f.read()
    soup = BeautifulSoup(lines, 'html.parser')
    categories = []
    book_titles = []
    urls = []
    tup_list = []
    cat_tags = soup.find_all('h4', class_ = 'category__copy')
    for tag in cat_tags:
        categories.append(tag.text.strip())
    book_tags = soup.find_all('img', class_ = 'category__winnerImage')
    for tag in book_tags:
        book_titles.append(tag.get('alt'))
    url_tags = soup.find_all('div', class_='category clearFix')
    for tag in url_tags:
        ut = tag.find('a')
        urls.append(ut.get('href'))
    for i in range(len(cat_tags)):
        tup_list.append((categories[i], book_titles[i], urls[i]))
    return tup_list


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    outFile = open(filename, 'w')
    csv_writer = csv.writer(outFile, delimiter = ',')
    csv_writer.writerow(['Book Title','Author Name'])
    for line in data:
        csv_writer.writerow(line)
    outFile.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r') as f:
        lines = f.read()
    soup = BeautifulSoup(lines, 'lxml')
    data = soup.find('div', class_ = 'readable stacked')
    data1 = data.find('span', id = 'freeText4791443123668479528').text
    entities = re.findall(r'([A-Z]{1}\w+ [A-Z]\w+ ?([A-Z]\w+)? ?([A-Z]\w+)? ?([A-Z]\w+)?)', data1)
    entity_list = []
    for entity in entities:
        entity_list.append(entity[0])
    return entity_list

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        list_of_tup = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(list_of_tup), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(list_of_tup), list)
        # check that each item in the list is a tuple
        for i in list_of_tup:
            self.assertEqual(type(i), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(list_of_tup[0][0], 'Harry Potter and the Deathly Hallows (Harry Potter, #7)')
        self.assertEqual(list_of_tup[0][1], 'J.K. Rowling')
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(list_of_tup[-1][0], 'Harry Potter: The Prequel (Harry Potter, #0.5)')
        self.assertEqual(list_of_tup[-1][1], 'J.K. Rowling')

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(self.search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for i in self.search_urls:
            self.assertEqual(type(i), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertTrue(i.startswith('https://www.goodreads.com/book/show/'))
        

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            result_tup = get_book_summary(url)
            summaries.append(result_tup)
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for item in summaries:
            self.assertEqual(type(item), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(item), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(item[0]), str)
            self.assertEqual(type(item[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(item[2]), int) 
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)   

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        result = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertEqual(len(result), 20)
        for item in result:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(item), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(result[0], ("Fiction", "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(result[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        outF = open('test.csv', 'r')
        lines = csv.reader(outF)
        csv_lines = []
        for line in lines:
            csv_lines.append(line)
        outF.close()
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ["Book Title","Author Name"])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ["Harry Potter and the Deathly Hallows (Harry Potter, #7)", 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ["Harry Potter: The Prequel (Harry Potter, #0.5)", 'J.K. Rowling'])
        


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



