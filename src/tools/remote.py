from os                         import getcwd, path, remove
from selenium                   import webdriver
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay           import Display
from typing                     import Union

from tools.logger import Logger

class Remote:
    __GEKO_DRIVER_PATH     = 'bin/drivers/geckodriver'
    __GEKO_DRIVER_LOG_PATH = 'logs/gecko_driver.log'

    __TIMEOUT = 60

    __MAX_ATTEMPTS = 5

    __browser = None
    __logger  = None
    __display = None

    def __init__(self):
        self.__logger  = Logger()
        self.__display = Display(visible=0, size=(1200, 768))
        self.__display.start()

    def setBrowser(self):
        options          = webdriver.firefox.options.Options()
        options.headless = True

        geckoDriverPath    = self.getGeckoDriverPath()
        geckoDriverLogPath = self.getGeckoDriverLogPath()

        if path.exists(geckoDriverLogPath) and path.isfile(geckoDriverLogPath):
            remove(geckoDriverLogPath)

        self.__browser = webdriver.Firefox(
            executable_path = geckoDriverPath,
            log_path        = geckoDriverLogPath,
            options         = options
        )

        self.__browser.set_page_load_timeout(self.__TIMEOUT)

    def unsetBrowser(self):
        if self.__browser is not None:
            self.__browser.quit()

        self.__browser = None

    def getHtml(self, url: str, attempt: int = 0) -> Union[str, None]:
        if attempt >= self.__MAX_ATTEMPTS:
            return None

        if attempt > 0:
            self.__logger.log('Attempt: %s' % str(attempt + 1))

        if self.__browser is None:
            self.setBrowser()

        try:
            self.__logger.log('Getting Content From %s' % url)

            self.__browser.get(url)

            html = self.__browser.page_source.replace('\n', '')

        except Exception as exp:
            html = None

        except TimeoutException as exp:
            html = None

        finally:
            if html is None or len(html) < 1:
                html = None 

        if html is None or url != self.__browser.current_url:
            self.__logger.logError('Can Not Retrieve Data From %s' % url)

            attempt = attempt + 1

            self.unsetBrowser()

            html = self.getHtml(url, attempt)

        return html

    def getGeckoDriverPath(self) -> str:
        return '%s/%s' % (getcwd(), self.__GEKO_DRIVER_PATH)

    def getGeckoDriverLogPath(self) -> str:
        return '%s/%s' % (getcwd(), self.__GEKO_DRIVER_LOG_PATH)
