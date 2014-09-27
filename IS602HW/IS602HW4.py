"""
HW4
Paul Garaud
1. Scrape text off of a webpage, and
2. Process it using AlchemyAPI
3. Return top ten keywords and their relevance to user prompt

AlchemyAPI: www.alchemyapi.com
"""

from bs4 import BeautifulSoup
import urllib2 as ul2


class Webpage:
    """
    A class designed to retrieve and parse a webpage with an div
    class = 'article_body', and provide a simple interface for
    accessing this data. Only the get_text() and get_html() functions
    are user-facing for parsimony.
    """
    def __init__(self, address):
        self.address = address
        self.html = self.__download_html()
        self.text = self.html and self.__extract_text() or None

    def __download_html(self):
        output = None
        try:
            con = ul2.urlopen(self.address)
        except:
            print('Error opening URL.')
        else:
            output = con.readlines()
            output = ' '.join(output)
        finally:
            try:
                con.close()
            except:
                pass
        return output

    def __extract_text(self):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(self.html)
        # don't need contact info, so only need up to n-2 paragraphs
        p_text = soup.select('div[class="article_body"] > p')[:-2]
        text = ' '.join([i.text for i in p_text])
        return text

    def get_text(self):
        return self.text


def parse_keyword_output(output):
    """
    Helper function to parse AlchemyAPI keyword output for printing
    :param output: AlchemyAPI keyword() method output
    :return: list of tuple of relevance, keyword pairs
    """
    keywords = output['keywords']
    return [(i['relevance'], i['text']) for i in keywords]


def print_keywords(keywords):
    """
    Print list of relevance-keyword tuples in prettier fashion
    :param keywords: list of two element tuples
    :return: None
    """
    template = "{0: <12}{1}"
    print(template.format('Relevance', 'Keyword'))
    for element in keywords:
        print(template.format(element[0], element[1]))


def main():

    from alchemyapi.alchemyapi import AlchemyAPI
    # Extract text from a webpage for analysis
    url = 'http://www.bloombergview.com/articles/2014-09-26/the-secret-goldman-sachs-tapes'
    article = Webpage(url)
    text = article.get_text()

    # Extract keywords
    alchemyapi = AlchemyAPI()
    output = alchemyapi.keywords('text', text)
    keywords = parse_keyword_output(output)
    keywords.sort(reverse=True)

    # Print to console
    print_keywords(keywords[:10])


if __name__ == '__main__':
    main()
