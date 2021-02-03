from typing import Union

from parser.sites import site
from parser.card import Card

class Prian(site.Site):
    __PATTERN_NEXT_URL = '^.*?href\=\"([^\s]+)\" aria\-label\=\"Next\" class\=\"pagination\-square__nav\" title\=\"Следующая\">Вперед.*?$'

    __PATTERNS_CARD_URL = [
        '<a[^>]+href=\"([^\"]+)\"[^>]+class=\"spec_item[^>]+>',
        '<a[^>]+href=\"([^\"]+)\"[^>]+class=\"detail_item[^>]+>'
    ]

    __PATTERN_CARD_TITLE = '^.*?<h1 class\=\"c\-header__title\">(.*?)<\/h1>.*?$'

    __PATTERN_CARD_PRICE = '^.*?<p class\=\"c\-header__price\">\s+([^>]+)\$\s+<\/p>.*?$'

    def parse(self):
        self.logger.log('Start Parsing prian.ru')

        prianUrl = self.url.getUrl(
            self.settings['base_url'],
            self.settings['url_params']
        )

        html    = self.remote.getHtml(prianUrl)
        nextUrl = self.__getNextUrl(html, prianUrl)

        while nextUrl is not None:
            self.__parseCardsFromHtml(html, nextUrl)

            html    = self.remote.getHtml(nextUrl)
            nextUrl = self.__getNextUrl(html, nextUrl)

        self.logger.log('End Parsing prian.ru')

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
        cardUrls = list()

        for pattern in self.__PATTERNS_CARD_URL:
            cardUrls = cardUrls + list(self.content.getSubstrings(html, pattern))

        cardUrls = list(set(cardUrls))

        if len(cardUrls) < 1:
            return None

        return cardUrls

    def __getNextUrl(
        self,
        html:       Union[str, None],
        currentUrl: str
    ) -> Union[str, None]:
        if html is None:
            return None

        nextUrl = self.content.getSubstring(html, self.__PATTERN_NEXT_URL)

        if nextUrl is None or len(nextUrl) < 1:
            return None

        return self.url.getNormalizedUrl(
            nextUrl,
            currentUrl,
            self.settings['protocol'],
            self.settings['host']
        )
