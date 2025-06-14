import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("server.log"),  # Logs to a file
        logging.StreamHandler()             # print to console
    ]
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
