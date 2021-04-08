import logging, sys, os, time
import datetime

logger = logging.getLogger('shifty-logger')
logger.setLevel(logging.DEBUG)

filename = os.path.join('../logs', 'Shifty_Log - ' + str(datetime.datetime.utcnow().date()) + '.txt')
if not os.path.exists(filename):
    os.mkdir('../logs')
    
file_handler = logging.FileHandler(filename=filename)
file_formatter = logging.Formatter("[%(module)s] %(asctime)s [%(levelname)s]: %(message)s")
file_formatter.converter = time.gmtime
file_handler.setFormatter(file_formatter)
console_formatter = logging.Formatter("[%(module)s] %(asctime)s [%(levelname)s]: %(message)s")
console_formatter.converter = time.gmtime
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def create_logger():
    """
    Creates a logger using json_logging library
    """
    return logger
