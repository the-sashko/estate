import re
import hashlib

from typing  import Union
from sqlite3 import Error as SQLiteError

from tools.logger   import Logger
from tools.store    import Store
from tools.telegram import Telegram

class Card:
    __hash     = None
    __url      = None
    __title    = None
    __price    = None
    __imageUrl = None

    __logger = None
    __store  = None

    def __init__(
        self,
        url:      str,
        title:    Union[str, None] = None,
        price:    Union[str, None] = None,
        imageUrl: Union[str, None] = None
    ) -> bool:
        self.__logger   = Logger()
        self.__telegram = Telegram()

        try:
            self.__store = Store()
        except SQLiteError as error:
            self.__logger.logError(error)

            raise Exeption('Can Not Init Store')

        self.__url = url
        self.__logger.log('Card URL: %s' % url)

        self.__hash = hashlib.md5(self.__url.encode('utf-8')).hexdigest()
        self.__logger.log('Card Hash: %s' % self.__hash)

        title = self.__formatTitle(title)

        if title is not None:
            self.__title = title
            self.__logger.log('Card Title: %s' % title)

        price = self.__formatPrice(price)

        if price > 0:
            self.__price = price
            self.__logger.log('Card Price: %i' % price)

        if imageUrl is not None:
            self.__imageUrl = imageUrl
            self.__logger.log('Card Image URL: %s' % imageUrl)

    def isCardExists(self) -> bool:
        try:
            row = self.__store.getRowByHash(self.__hash)

            if row is not None:
                return True
        except SQLiteError as error:
            self.__logger.logError(error)

        return False

    def save(self) -> bool:
        if not self.__isValidFormatUrl():
            self.__logger.logError('Card URL %s Has Bad Format' % self.__url)
            return False

        if (self.isCardExists()):
            self.__logger.log('Card Already Exists')
            return False

        try:
            return self.__store.insertRow(
                self.__hash,
                self.__url,
                self.__title,
                self.__price,
                self.__imageUrl
            )
        except SQLiteError as error:
            self.__logger.logError(error)
            return False

    def send(self):
        message = self.__url

        if self.__price is not None:
            message = 'Price %s $\n%s' % (f'{self.__price:,}'.replace(',', ' '), message)

        if self.__title is not None:
            message = '%s\n%s' % (self.__title.upper(), message)

        self.__telegram.sendToChannel(message)

        self.__logger.log('Card Sent To Channel')

    def __isValidFormatUrl(self) -> bool:
        pattern = re.compile('^http.*?$')

        return pattern.match(self.__url) is not None

    def __formatPrice(
        self,
        price: Union[str, None]
    ) -> int:
        if price is None:
            return 0

        return int(price.replace(' ', ''))

    def __formatTitle(
        self,
        title: Union[str, None]
    ) -> Union[str, None]:
        if title is None:
            return None

        return title.replace('<sup>2</sup>', '²')
