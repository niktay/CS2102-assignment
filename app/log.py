import logging


def setup_logger(name):
    log_format = '{[%(levelname)s] : %(module)s.%(funcName)s()}'
    log_format += ' - %(message)s'

    logging.basicConfig(
        level=logging.DEBUG, format=log_format,
        handlers=[logging.StreamHandler(), ],
    )

    return logging.getLogger(name)
