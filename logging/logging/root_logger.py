import logging

# Logging is one of a few singleton classes in python.

if __name__ == "__main__":


    # Least severe
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    # Most severe

    # Default level is warning and default logger is root.

    logging.basicConfig(
        level = logging.DEBUG, # Set the custom level of the logger like this.
                                #Defaults to Warning.
        filename = "somefile.log", # Set the filename of the logger like this.
                                #Defaults to stdout.
        filemode = "w", # Set the filemode of the logger like this.
                            #Defaults to append.
        format = "%(asctime)s - %(levelname)s - %(message)s", # Set the format of the
                                    #logger like this. Defaults to quite a nice format
        datefmt = "%d-%b-%y %H:%M:%S" # Set the date format of the logger like this.
    )

    # basicConfig should be called before any logging is done. As you can see it
    # has no effect here.

    logging.info("This won't be logged")

    # You can print errors using the exc_info parameter.

    try:
        1/0
    except:
        logging.error("Error", exc_info = True)

    # If you do this with no exception, you get Nonetype: None in the return.

    logging.error("Error", exc_info = True)

    # There is short hand for logging.error(exc_info=True)

    try:
        1/0
    except:
        logging.exception("Error")

    # You can create your own logger using getLogger.

    logger = logging.getLogger("mylogger")

    logger.warning("This is a warning message.")

    # The levels are actually given by integers:

    print("Debug", logging.DEBUG)
    print("Info", logging.INFO)
    print("Warning", logging.WARNING)
    print("Error", logging.ERROR)
    print("Critical", logging.CRITICAL)