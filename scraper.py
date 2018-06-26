import argparse
import pandas as pd

from Bio import Entrez
from collections import defaultdict

"""
Script usage:

To get help, enter this: python scraper.py -h
To get actual data, enter this: python scraper.py search_term num_articles user_email
"""


class ArticleParser:
    """
    Parser for PubMed articles
    """

    def __init__(self, retmax, email, token=None):
        self.retmax = retmax
        self.email = email
        self.token = token

    def find_term(self, term):
        """
        Finds articles containing a specified term

        Args:
        term (str) - term to search for

        Returns:
        result (dict) - dictionary with article IDs
                        and some meta information
        """

        Entrez.email = self.email

        query = Entrez.esearch(db='pubmed', sort='relevance',
                               retmode='xml', term=term, retmax=self.retmax,
                               api_key=self.token)
        result = Entrez.read(query)

        return result

    def fetch_info(self, id_list):
        """
        Fetches article abstracts

        Args:
        id_list (list) - list of article IDs to process

        Returns:
        result (dict) - dictionary containing raw article information,
                        including its abstract
        """

        Entrez.email = self.email

        ids = ','.join(id_list)
        query = Entrez.efetch(db='pubmed', retmode='xml',
                              id=ids, api_key=self.token)
        result = Entrez.read(query)

        return result

    def parse_info(self, articles):
        """
        Parses a dictionary returned by fetch_info()

        Args:
        articles (dict) - dictionary containing raw article information,
                          including its abstract

        Returns:
        article_dict (dict) - dictionary containing parsed article information,
                              including its title, creation date, author(s),
                              and abstract
        """

        article_dict = defaultdict(dict)

        for idx, article in enumerate(articles['PubmedArticle']):

            authors = []

            # gets the article title
            title = article['MedlineCitation']['Article']['ArticleTitle']

            # gets the article creation date
            try:
                date_dict = article['MedlineCitation']['Article']['ArticleDate'][0]
            except IndexError:
                date_dict = article['MedlineCitation']['DateCompleted']
            date = '{}-{}-{}'.format(date_dict['Year'], date_dict['Month'], date_dict['Day'])

            # gets the article author(s)
            author_list = article['MedlineCitation']['Article']['AuthorList']
            for author in author_list:
                if 'CollectiveName' not in author:
                    authors.append('{} {} {}'.format(author['ForeName'],
                                                     author['LastName'],
                                                     author.get('Suffix', '')).strip())
            authors = ', '.join(authors)

            # gets the text of the article abstract
            abstract_text = ''
            try:
                abstract_raw = article['MedlineCitation']['Article']['Abstract']['AbstractText']
                abstract_text = ' '.join([str_el.split('attributes=')[0] for str_el in abstract_raw])
            except KeyError:
                print("There's no abstract for article {}".format(idx))

            # populates the article dictionary
            article_dict[idx]['title'] = title
            article_dict[idx]['date'] = date
            article_dict[idx]['authors'] = authors
            article_dict[idx]['abstract'] = abstract_text

        return article_dict

    def save_to_csv(self, article_data, filename):
        """
        Filters out entries with empty abstracts and
        saves the data to a CSV file

        Args:
        article_data (dict) - dictionary with cleaned article info
        filename (str) - name of the CSV file to save article_data to

        Returns:
        None
        """

        df = pd.DataFrame.from_dict(article_data, orient='index')
        df = df[df.abstract != '']
        df.to_csv(filename, index_label='id')


def main():
    """
    Retrives and cleans PubMed article data

    Args:
    None

    Returns:
    None
    """

    # parses command-line arguments
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('search_term', help='Term to search for', type=str)
    arg_parser.add_argument('num_articles', help='Number of articles to retrieve',
                            type=int)
    arg_parser.add_argument('email', help='User email', type=str)
    arg_parser.add_argument('--token', help='PubMed API key', type=str)

    args = arg_parser.parse_args()

    # instantiates the article parser and retrives PubMed info
    pm_parser = ArticleParser(args.num_articles, args.email, args.token)

    print('Retrieving IDs of articles containing the search term...\n')
    raw_dict = pm_parser.find_term(args.search_term)
    print('Fetching article information...\n')
    articles = pm_parser.fetch_info(raw_dict['IdList'])
    print('Parsing the fetched data...\n')
    parsed_dict = pm_parser.parse_info(articles)
    print('Parsing complete. Saving the data to a CSV file...\n')
    pm_parser.save_to_csv(parsed_dict, args.search_term + '.csv')
    print('Done! The data has been saved to {}.'.format(args.search_term + '.csv'))

if __name__ == '__main__':
    main()
