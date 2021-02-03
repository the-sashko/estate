import sys

from tools import *
from parser import *

__logger   = None
__parser   = None

class App():
    def __init__(self):
        self.__logger = logger.Logger()

        parserConfig  = settings.Settings().getParserConfig()
        self.__parser = parser.Parser(parserConfig)
        
    def run(self):
        self.__logger.log('Start Parser')

        try:
            self.__parser.parse()
        except Exception as exp:
            self.__logger.logError(exp)
            sys.exit()

        self.__logger.log('Finish Parser')
