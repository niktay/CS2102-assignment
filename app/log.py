import logging


def setup_logger(name):
    log_format = '%(asctime)s : %(levelname)s : %(module)s - %(message)s'

    logging.basicConfig(
        level=logging.DEBUG, format=log_format,
        handlers=[logging.StreamHandler(), ],
    )

    return logging.getLogger(name)
