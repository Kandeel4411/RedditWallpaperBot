import ctypes
import logging
import os
import sys

import praw

SPI_SETDESKWALLPAPER = 20
logger = logging.getLogger(__name__)

def getReddit(login):
    """Input: Dict with client_id and client_secret """
    try:
        reddit = praw.Reddit(
            client_id=login["client_id"],
            client_secret=login["client_secret"],
            user_agent=login["user_agent"]
        )
    except Exception as e:
        logging.exception(f"{e}")
        logging.critical("Couldn't create Reddit object")
        sys.exit()
    return reddit


def getSubreddit(reddit, name):
    """Returns subreddit based on given reddit object and subreddit name"""
    try:
        subreddit = reddit.subreddit(name)
    except Exception as e:
        logging.exception(f"Error: {e}")
        logging.critical(f"Couldn't create {subreddit} Subreddit Object")
        sys.exit()
    else:
        logger.info(f"Successfully created Subreddit Object : {subreddit}")
        return subreddit


def getPicturePost(subreddit_sort):
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
            if hasattr(submission, "post_hint")\
                    and submission.post_hint == "image"\
                    and os.path.splitext(submission.url)[1] != ".gif":
                logger.info(f"{submission} Has Picture ")
                logger.debug("Finished Iteration")
                return submission
            logger.debug(f"submission: {submission} No Picture")
    except Exception as e:
        logging.exception(f"{e}")
        logging.critical("Couldn't access submissions")
        print(
            "Error: Invalid Subreddit. Please try again with valid Subreddit."
        )
        sys.exit()
    else:
        print(
            "Error: No Picture found in subreddit."
            " Please try again with different Subreddit.")
        logger.critical("Couldn't find picture in Subreddit")
        sys.exit()


def saveImage(path, image):
    """Saves image with given name and contents in bytes to image folder """
    # Creating directory if it doesn't exist
    try:
        logger.debug("Creating image directory")
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        logger.error("Directory already exists")
    except Exception as e:
        print(f"Error : {e}")
        logger.exception(f"{e}")
        logger.critical("Couldn't create directory")
        sys.exit()

    # Creating Image
    try:
        logger.debug(f"Opening {path}")
        img = open(path, "wb")
    except Exception as e:
        print(f"Error: {e}")
        logger.exception(f"{e}")
        logger.critical("Couldn't open file")
        sys.exit()
    else:
        with img:
            try:
                logger.debug("Writing to file")
                img.write(image)
            except Exception as e:
                print(f"Error: {e}")
                logger.exception(f"{e}")
                logger.critical("Couldn't write to file")
                sys.exit()
            else:
                logger.info(f"Saved file as {path}")


def setImageBackground(path):
    """Sets given image path as background """
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, path, 0)
