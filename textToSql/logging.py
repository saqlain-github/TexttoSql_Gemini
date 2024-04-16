import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self._create_log_dir()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create a file handler
        log_filename = os.path.join(self.log_dir, self._generate_log_filename())
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _create_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _generate_log_filename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"log_{timestamp}.txt"

    def log(self, message, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
            
    # Expanded log functions
    def debug(self, message):
        self.log(message, level=logging.DEBUG)

    def info(self, message):
        self.log(message, level=logging.INFO)

    def warning(self, message):
        self.log(message, level=logging.WARNING)

    def error(self, message):
        self.log(message, level=logging.ERROR)

    def critical(self, message):
        self.log(message, level=logging.CRITICAL)

logger = Logger()