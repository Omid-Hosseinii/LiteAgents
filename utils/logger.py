import logging


def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s", )

    return logging.getLogger(name)


"""
logger = get_logger(__name__)
logger.info("Reading PDF: %s", pdf_path)
"""
