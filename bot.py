import ctypes
import logging
import os
import sys

import praw
import prawcore

SPI_SETDESKWALLPAPER = 20
logger = logging.getLogger(__name__)


def get_reddit(login):
    try:
        reddit = praw.Reddit(
            client_id=login["client_id"],
            client_secret=login["client_secret"],
            user_agent=login["user_agent"]
        )
        
    except praw.exceptions.ClientException as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't create Reddit object")
        sys.exit()
    return reddit


def get_subreddit(reddit, name):
    """Returns subreddit based on given reddit object and subreddit name"""
    try:
        subreddit = reddit.subreddit(name)
    except TypeError as e:
        print( 
        "Error: Invalid Subreddit. Please try again with valid Subreddit.\n"
        )
        logger.exception(f"{e}")
        logger.critical(f"Couldn't create Subreddit Object")
        sys.exit()
    return subreddit


def get_picture_post(subreddit_sort):
    """Returns picture submission based on the given subreddit
and how it's sorted"""

    logger.debug(
        f"Iterating over {subreddit_sort} submissions in subreddit,\
        limit={subreddit_sort.limit}")

    # Searching Posts until a picture is found
    print("Searching...\n")
    try:
        for submission in subreddit_sort:
            # Is an image tagged post which isn't a gif
            if (
                hasattr(submission, "post_hint")
                and submission.post_hint == "image"
                and os.path.splitext(submission.url)[1] != ".gif"
                ):
                logger.info(f"{submission} Has Picture ")
                logger.debug("Finished Iteration")
                return submission
            logger.debug(f"submission: {submission} No Picture")
    except prawcore.exceptions.Redirect as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't access subreddit")
        print(
            "Error: Invalid Subreddit. Please try again with valid Subreddit."
        )
        sys.exit()
    except prawcore.RequestException as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't establish connection")
        print(
            "Error: Failed to establish a new connection. Please check your connection and try again."
        )
        sys.exit()
    
    print(
        "Error: No Picture found in subreddit."
        " Please try again with different Subreddit.")
    logger.critical("Couldn't find picture in Subreddit")
    sys.exit()


def save_image(path, image):
    """Saves image with given name and contents in bytes to image folder """
    # Creating directory if it doesn't exist
    try:
        logger.debug("Creating image directory")
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        logger.error("Directory already exists")
    except OSError:
        print(f"Error : {e}")
        logger.exception(f"{e}")
        logger.critical("Couldn't create directory")
        sys.exit()

    # Creating Image
    try:
        logger.debug(f"Opening {path}")
        with open(path, "wb") as img_file:
            logger.debug("Writing to file")
            img_file.write(image)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        logger.exception(f"{e}")
        logger.critical("Couldn't open file")
        sys.exit()
    except OSError as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't write to file")
        sys.exit()

    logger.info(f"Saved file as {path}")



def set_image_background(path):
    """Sets given image path as background """
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, path, 0)
