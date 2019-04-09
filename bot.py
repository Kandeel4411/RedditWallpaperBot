import ctypes
import logging
import os
import sys

import praw
import prawcore

BOT_EXCEPTION = False
SPI_SETDESKWALLPAPER = 20
logger = logging.getLogger(__name__)

class BotException(Exception):
    """ A general exception class for bot """

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
        check_exception(f"{e}")
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
        check_exception(f"{e}")
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
        check_exception(f"{e}")
    except prawcore.RequestException as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't establish connection")
        print(
            "Error: Failed to establish a new connection. Please check your connection and try again."
        )
        check_exception(f"{e}")

    print(
        "Error: No Picture found in subreddit."
        " Please try again with different Subreddit.")
    logger.critical("Couldn't find picture in Subreddit")
    check_exception(f"{e}")


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
        check_exception(f"{e}")

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
        check_exception(f"{e}")
    except OSError as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't write to file")
        check_exception(f"{e}")

    logger.info(f"Saved file as {path}")


def set_image_background(image_path: str):
    """Sets given image image_path as background """

    print("Set picture as background? [Y/N] : ", end="")
    logger.debug("Starting loop")
    while True:
        logger.debug("Getting user input")
        choice = input().lower()
        if choice == "y":
            logger.info(f"User choice: {choice}")
            # Windows-only support currently
            set_windows_background(image_path=image_path)
            logger.debug("Set picture as background")
            print("Done.\n")
            break
        elif choice == "n":
            logger.info(f"User choice: {choice}")
            logger.debug("Displaying image full path")
            print(
                f"Image path is : {image_path}"
            )
            break


def set_windows_background(image_path: str):
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, 0)

def raise_bot_exception(option: bool):
    """ Takes option to throw BotException instead of sys.exit() or not. Initially False"""
    global BOT_EXCEPTION
    BOT_EXCEPTION = option

def check_exception(message):
    if BOT_EXCEPTION:
        raise BotException(message)
    else:
        sys.exit()
    
