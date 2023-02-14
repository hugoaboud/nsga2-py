import logging

"""
    Util class for setting up python logging.
"""
class Log:

    @classmethod
    def setup(self, logfile=None, level='INFO'):
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        rootLogger = logging.getLogger()
        rootLogger.setLevel(level)

        if (logfile):
            fileHandler = logging.FileHandler(logfile)
            fileHandler.setFormatter(logFormatter)
            rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
