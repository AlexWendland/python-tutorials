import logging
import logging.config
from time import sleep

import yaml

# Really you are just handing this a dictionary of your configuration.
with open("logger.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    print(yaml.dump(config))
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.debug("This is a debug message")

file_logger = logging.getLogger("exampleLogger")

# Now this is pretty cool.
for count in range(100):
    file_logger.info("%s: This is an info message", count)