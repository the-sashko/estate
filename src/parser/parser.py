from parser.sites import *

__settings = None

class Parser:
    def __init__(self, settings: dict):
        self.__settings = self.__prepareSetting(settings)

    def parse(self):
        prian.Prian(self.__settings['prian']).parse()
        #prian_cyprus.PrianCyprus(self.__settings['prian_cyprus']).parse()
        realeast.RealEast(self.__settings['real_east']).parse()

    def __prepareSetting(self, settings: dict) -> dict:
        settings['prian']['url_params']['maxprice'] = settings['max_price']

        settings['real_east']['url_params']['price'] = str(
            int(settings['max_price'] / 1000)
        )

        settings['prian_cyprus']['url_params']['maxprice'] = settings['max_price']

        return settings
