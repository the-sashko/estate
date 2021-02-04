from typing import Union

from parser.sites import site
from parser.card  import Card

class RealEast(site.Site):
    __PATTERN_CARD_URL = '<a[^>]+href=\"(\?id=[0-9]+)\">'

    __PATTERN_CARD_TITLE = '^.*?<h3 class=\"saddress\">(.*?)<\/h3>.*?$'

    __PATTERN_CARD_PRICE = '^.*?<span class=\"ltr\">(.*?)<\/span> <span class=\"cur\">\$<\/span>.*?$'

    def parse(self):
        self.logger.log('Start Parsing realeast.su')

        realEastUrl = self.url.getUrl(
            self.settings['base_url'],
            self.settings['url_params']
        )

        html = self.remote.getHtml(realEastUrl)

        self.__parseCardsFromHtml(html, realEastUrl)

        self.logger.log('End Parsing realeast.su')

    def __parseCardsFromHtml(self, html: str, currentUrl: str) -> bool:
        cardUrls = self.__getCardsUrlFromHtml(html)

        if cardUrls is None:
            return False

        for cardUrl in cardUrls:
            self.__parseCard(cardUrl, currentUrl)

        return True

    def __parseCard(self, url: str, currentUrl: str) -> bool:
        url = self.url.getNormalizedUrl(
            url,
            currentUrl,
            self.settings['protocol'],
            self.settings['host']
        )

        if url is None:
            return False

        if (self.__isCardExists(url)):
            self.logger.log('Card Already Exists')
            return False

        self.logger.log('Parsing Card By URL %s' % url)

        html = self.remote.getHtml(url)

        if html is None:
            self.logger.logError('Can Not Get Card Content From URL %s' % url)
            return False

        title = self.content.getSubstring(html, self.__PATTERN_CARD_TITLE)
        title = next(iter(title.split(' / ')), None)

        price = self.content.getSubstring(html, self.__PATTERN_CARD_PRICE)

        card = Card(url, title, price)

        if card.save():
            self.logger.log('Card Saved')
            card.send()

        return True

    def __isCardExists(self, url: str) -> bool:
        card = Card(url)

        return card.isCardExists()

    def __getCardsUrlFromHtml(self, html: str) -> Union[list, None]:
        cardUrls = self.content.getSubstrings(html, self.__PATTERN_CARD_URL)

        cardUrls = list(set(list(cardUrls)))

        if len(cardUrls) < 1:
            return None

        return cardUrls
