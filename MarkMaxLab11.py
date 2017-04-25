'''
Mark Max 4/22/2017
CIS 117 Lab 11
Developed in PyCharm Community Edition 2016.3.2

The purpose of the this program is to design and test and simple web
crawler that could be used by a marketing department to determine
how often certain topics are included on the company's website.

The file contains the class Collector which is a class designed to
contain a url and every link found in the html file at that url. As
well as an accessor method getLinks() that returns the links in the
html file.

The file also contains methods frequency, analyze and crawlFirstHundred.
frequency takes a list of topics and a string and then increments
each topic with how many times it shows up in the string. In this case
the string is the contents of an html file. Analyze takes a url,
creates a Collector object from it, runs frequency on the contents,
and returns a list of urls in the contents. crawlFirstHundred, is a
recursive method that goes to the first 100 internal links from the
seed link and runs analyze on them.

These methods are tested using the National Academy of Sciences website.
'''


from urllib.request import urlopen
from urllib.parse import urljoin
from html.parser import HTMLParser

'''
class Collector(HTMLParser):

instance variables:
    url
        a string variable for storing the classes url
    links
        a list of all the links in url's html file

constructor:
    def __init__(self, url):
        initializes url to the parameter url
        initializes links to an empty list

methods:
    def handle_starttag(self, tag, attrs):
        overrides the handle_starttag method in HTMLParser
        pre: links is a blank list
        post: links contains a list of all urls included in the html
            file located at instance variable url

    def getLinks(self):
        pre: Collect object exists
        post: the instance variable links is returned
'''
class Collector(HTMLParser):

    def __init__(self, url):
        HTMLParser.__init__(self)
        self.url = url
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    absolute = urljoin(self.url, attr[1])
                    if absolute[:4] == 'http':
                        self.links.append(absolute)

    def getLinks(self):
        return self.links

# visited is a global variable list of all urls the crawler has visited
visited = set()
# the topics of interest to the marketing department
topics = {'research': 0, 'climate': 0, 'evolution': 0, 'cultural': 0,
          'leadership': 0, 'engineering': 0}

'''
def frequency(content, topics):
    pre: a string, content, and a dictionary, topics, that has keywords
        and their frequencies, exist
    post: the dictionary, topics, has each keyword incremented by the
        number of times it shows up in content.
'''
def frequency(content, topics):
    for topic in topics:
        freq = content.count(topic)
        topics[topic] += freq

'''
def analyze(url):
    pre: a string url exists
    post: a Collector object is created using parameter url.
        the contents of the html file at url are run through method
        frequency using the global variable topics.
        the links contained in the html file at url are returned
'''
def analyze(url):
    content = urlopen(url).read().decode()
    collector = Collector(url)
    collector.feed(content)
    urls = collector.getLinks()

    content = content.lower()
    frequency(content, topics)

    return urls

'''
def crawlFirstHundred(url):

    pre: a url exists
    post: the first 100 unique children links after the seed url have
        been analyzed.

    This crawler only checks for links that are children of the seed url.
    This is to ensure that information provided to marketing is completely
    relevant to the website they are interested in examining, and that
    links to websites like facebook, that would throw off the keyword
    analysis, are ignored.
'''
def crawlFirstHundred(url):

    global visited
    visited.add(url)

    # save the first visited website to the baseURL
    if len(visited) == 1:
        baseURL = url

    links = analyze(url)

    for link in links:
        # filter on unique urls that are children of the baseURL
        if link not in visited and len(visited)<100 and baseURL in link:
            try:
                crawlFirstHundred(link)
            except:
                pass



crawlFirstHundred('http://www.nasonline.org')

for topic,freq in topics.items():
    print(topic + " appears " + str(freq) + " times")


'''
research appears 182 times
climate appears 25 times
evolution appears 13 times
cultural appears 194 times
leadership appears 181 times
engineering appears 126 times
'''

