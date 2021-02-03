from tools import *

class Site():
    url      = None
    settings = None
    content  = None
    logger   = None

    def __init__(self, settings):
        self.url      = url.Url()
        self.remote   = remote.Remote()
        self.content  = content.Content()
        self.logger   = logger.Logger()
        self.settings = settings
