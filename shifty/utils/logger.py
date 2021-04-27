import logging, sys, os, time
import datetime

logger = logging.getLogger('shifty-logger')
logger.setLevel(logging.DEBUG)
log_path = os.environ.get('SHIFTY_LOG_PATH')

filename = os.path.join(log_path, 'Shifty_Log - ' + str(datetime.datetime.utcnow().date()) + '.txt')
if not os.path.exists(log_path):
    os.mkdir(log_path)
    
file_handler = logging.FileHandler(filename=filename)
file_formatter = logging.Formatter("[%(module)s] %(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
file_formatter.converter = time.gmtime
file_handler.setFormatter(file_formatter)
console_formatter = logging.Formatter("[%(module)s] %(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
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

def get_current_log_filepath():
    """
    Returns log file for today
    """
    return filename
