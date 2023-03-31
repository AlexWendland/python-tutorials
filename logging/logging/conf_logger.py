import logging

# You need to import this in addition to logging. Otherwise it won't work.
import logging.config

# You need to set disable_existing_loggers to False to use the config file - otherwise
# it does exactly what you would expect if it was set to True.
logging.config.fileConfig(fname = "logger.conf", disable_existing_loggers = False)

logger = logging.getLogger(__name__)

logger.debug("This is a debug message")

# This uses the second logger in the config file.
other_logger = logging.getLogger("sampleLogger")

# Notice the console output is using the root formatter here.
other_logger.info("This is an info message")

# Notice this message gets returned to the console but not to the file.
other_logger.debug("This is a debug message")