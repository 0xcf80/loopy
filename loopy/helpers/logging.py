import logging


def init_logger():
    """
    logFormatter = logging.Formatter("[%(levelname)-7.7s] %(asctime)s %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(loglevel)

    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    """
    logging.basicConfig(level=logging.INFO)