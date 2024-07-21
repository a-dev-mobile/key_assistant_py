import logging

def setup_logger(log_level):
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(log_level)
    logging.debug(f'Logger set to {log_level}')
