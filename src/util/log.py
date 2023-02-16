import logging

"""
    Util class for setting up python logging.
"""
class Log:

    logger = logging.getLogger('nsga2-py')

    @classmethod
    def setup(self, logfile=None, level='INFO'):
        self.logger.propagate = False
        
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()

        self.logger.setLevel(level)
        
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

        if (logfile):
            fileHandler = logging.FileHandler(logfile)
            fileHandler.setFormatter(logFormatter)
            self.logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)
