import abc
import requests
from bs4 import BeautifulSoup


class BaseCrawler:
    @abc.abstractmethod
    def construct_url(self):
        raise NotImplementedError

    def get_html(self, url):
        return requests.get(url)

    def get_response_text(self, response):
        return response.text

    def get_soup(self, response):
        return BeautifulSoup(response, features="html.parser")

    @abc.abstractmethod
    def crawl(self):
        raise NotImplementedError
