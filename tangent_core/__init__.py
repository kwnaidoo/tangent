import logging

# Create our API logger to keep track of failures in API queries
api_logger = logging.getLogger(__name__)
api_logger.setLevel(logging.WARNING)

# Create the Handler for logging data to a file
log_handler = logging.FileHandler('api_exceptions.log')
log_handler.setLevel(logging.WARNING)

# Format how our log messages will appear
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Add the Formatter to the Handler
log_handler.setFormatter(formatter)

# Attach log handler to api_logger
api_logger.addHandler(log_handler)