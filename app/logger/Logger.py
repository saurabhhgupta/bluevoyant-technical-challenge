import logging


class Logger:

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')

    def log(message: str):
        logging.info(message)

    def logError(message: str):
        logging.error(message)
