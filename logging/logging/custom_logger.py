import logging

# It is standard practice to use __name__ as the name of the logger, so when importing
# this module, the logger will be named custom_logger and it is easy to find out where
# it has come from.

logger = logging.getLogger(__name__)

# The Handler class is used to send the log records to the appropriate destination.

stream_handler = logging.StreamHandler() # This is standard output.
file_handler = logging.FileHandler("file.log") # This is to a file.

# You set the warning levels using the setLevel method.

stream_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)

# The Formatter class is used to format the log records.

stream_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# You need to attach these to the handlers.

stream_handler.setFormatter(stream_formatter)
file_handler.setFormatter(file_formatter)

# You need to attach these to the logger.

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.warning("This is a warning")
logger.error("This is an error")