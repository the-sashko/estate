import re
import html

from typing       import Union
from urllib.parse import urlencode

class Url:
    def getUrl(self, baseUrl: str, urlParams: dict = {}) -> str:
        urlParams = urlencode(urlParams)

        if len(urlParams) < 1:
            return baseUrl

        return self.getNormalizedUrl("%s?%s" % (baseUrl, urlParams))

    def getNormalizedUrl(
        self,
        url:        str,
        currentUrl: Union[str, None] = None,
        protocol:   Union[str, None] = None,
        host:       Union[str, None] = None
    ) -> Union[str, None]:
        if currentUrl is not None:
            currentUrl = next(iter(currentUrl.split('#')), None)
            currentUrl = next(iter(currentUrl.split('&')), None)
            currentUrl = next(iter(currentUrl.split('?')), None)

        pattern = re.compile('^((http)|(\/)).*?$')

        if not pattern.match(url) and currentUrl is not None:
            url = "%s%s" % (currentUrl, url)

        pattern = re.compile('^\/\/.*?$')

        if pattern.match(url) and protocol is not None:
            url = "%s:%s" % (protocol, url)

        pattern = re.compile('^\/.*?$')

        if pattern.match(url) and host is not None:
            url = "%s%s" % (host, url)

        pattern = re.compile('^http.*?$')

        if not pattern.match(url):
            url = None

        return html.unescape(url)
