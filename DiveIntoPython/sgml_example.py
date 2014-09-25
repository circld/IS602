# Example demonstrating use of SGMLParser
import urllib
from sgmllib import SGMLParser

page = urllib.urlopen('http://www.diveintopython.net')
source = page.read()
page.close()

# verify that we've grabbed the source code
# print(source[:1000])

class URLLister(SGMLParser):
    def reset(self):
        """
        Called by __init__ of SGMLParser (this is an override);
        Can be called to re-initialize (in lieu of __init__)
        """
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        """
        Called whenever <a> tag is found
        :param attrs: [(attribute, value), ...]
        """
        # SGMLParser converts to lowercase, so k == 'href' is robust
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)

# Now we use the URLLister parser to parse the html source code
page = urllib.urlopen('http://www.diveintopython.net')
parser = URLLister()
parser.feed(page.read())  # use feed() method on page source code
page.close()
parser.close()  # close() to flush buffer and process (may not process otherwise)
for url in parser.urls: print url
