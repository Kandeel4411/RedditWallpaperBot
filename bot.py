import ctypes
import logging
import os
import subprocess
import sys

import distro
import praw
import prawcore
from platform import system

BOT_EXCEPTION = False
SPI_SETDESKWALLPAPER = 20


logger = logging.getLogger(__name__)


class BotException(Exception):
    """ A general exception class for bot """


def get_reddit(login):
    """ Returns logged-in reddit object based on given login information"""
    reddit = praw.Reddit(
        client_id=login["client_id"],
        client_secret=login["client_secret"],
        user_agent=login["user_agent"]
    )
    return reddit


def get_subreddit(reddit, name):
    """Returns subreddit based on given reddit object and subreddit name"""
    try:
        subreddit = reddit.subreddit(name)

    # Exception thrown when name is empty string
    except TypeError as e:
        print(
            "Error: Invalid Subreddit."
            " Please try again with valid Subreddit.\n"
        )
        logger.exception(f"{e}")
        logger.critical(f"Couldn't create Subreddit Object")
        check_bot_exception("Couldn't create Subreddit Object")
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
                hasattr(submission, "post_hint") and
                submission.post_hint == "image"and
                os.path.splitext(submission.url)[1] != ".gif"
            ):
                logger.info(f"{submission} Has Picture ")
                logger.debug("Finished Iteration")
                return submission
            logger.debug(f"submission: {submission} No Picture")

    # Exception thrown when subreddit is not found
    except prawcore.exceptions.Redirect as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't access subreddit")
        print(
            "Error: Invalid Subreddit. Please try again with valid Subreddit."
        )
        check_bot_exception("Couldn't access subreddit")

    # Exception thrown on network/time out failure
    except prawcore.RequestException as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't establish connection")
        print(
            "Error: Failed to establish a new connection."
            " Please check your connection and try again."
        )
        check_bot_exception("Couldn't establish connection")

    # Exception thrown when the reddit object couldn't login
    except prawcore.exceptions.ResponseException as e:
        logger.exception(f"{e}")
        logger.critical("Invalid client_ID or client_secret")
        print(
            "Error: Invalid client_Id or client_secret."
            " Please check your credentials and try again."
        )
        check_bot_exception("Invalid client_ID or client_secret")

    print(
        "Error: No Picture found in subreddit."
        " Please try again with different Subreddit."
    )
    logger.critical("Couldn't find picture in Subreddit")
    check_bot_exception("No picture posts in the defined limit")


def save_image(path, image):
    """Saves image with given name and contents in bytes to image folder """

    create_image_folder(path=path)

    try:
        logger.debug(f"Opening {path}")
        with open(path, "wb") as img_file:
            logger.debug("Writing to file")
            img_file.write(image)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        logger.exception(f"{e}")
        logger.critical("Couldn't open file")
        check_bot_exception("Couldn't open file")
    except OSError as e:
        logger.exception(f"{e}")
        logger.critical("Couldn't write to file")
        check_bot_exception("Couldn't write to file")
    logger.info(f"Saved file as {path}")


def create_image_folder(path):
    try:
        logger.debug("Creating image directory")
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        logger.error("Directory already exists")
    except PermissionError as e:
        print(f"Error : {e}")
        logger.exception(f"{e}")
        logger.critical("Couldn't create directory")
        check_bot_exception("Couldn't create directory")


def set_image_background(image_path: str, prompt=None):
    """Prompts given image path to be set as background.
 if prompt exists, uses that as prompt instead. """

    choice = user_prompt(
        "Set picture as background? [Y/N] : "
    ) if prompt is None else prompt

    if choice:
        os_name = system()
        os_support = {
            "Windows": set_windows_background,
            "Darwin": set_mac_background,
            "Linux": set_linux_background
        }

        # Calls background function based on current OS
        if os_name in os_support:
            os_support[os_name](image_path=image_path)
        else:
            print("Error: Unsupported OS.")
            logger.critical(f"Unsupported OS: {os_name}")
            check_bot_exception("Unsupported OS")

        logger.debug("Set picture as background")
        print("Done.\n")
    else:
        logger.debug("Displaying image full path")
        print(f"Image path is : {image_path}")


def user_prompt(message: str):
    """ Prompts user continously until he enters [Y/N] and returns choice as boolean """
    logger.debug("Starting loop")
    while True:
        choice = input(message).lower()
        if choice == "n":
            logger.info(f"User choice: {choice}")
            return False
        elif choice == "y":
            logger.info(f"User choice: {choice}")
            return True


def set_windows_background(image_path: str):
    """ Sets given image path as background for Windows 64-bit"""
    try:
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, image_path, 0)
    except WindowsError as e:
        print("Failed to set Windows wallpaper. Please try again.")
        logger.exception(e)
        logger.critical("Couldn't set background")
        check_bot_exception(e)


def set_mac_background(image_path: str):
    """ Sets given image path as background for Mac using osascript """
    try:
        mac_script = (
            f"""osascript -e 'tell application "Finder" """
            f""" to set desktop picture to "{image_path}" as POSIX file'"""
        )
        subprocess.run(mac_script, shell=True)
    except subprocess.CalledProcessError as e:
        print("Failed to set Mac wallpaper. Please try again.")
        logger.exception(e)
        logger.critical("Couldn't set background")
        check_bot_exception(e)


def set_linux_background(image_path: str):
    """Sets given image path as background for supported Linux distributions"""
    distro_script = get_dist_script(image_path=image_path)
    if distro_script is not None:
        try:
            subprocess.run(distro_script, shell=True)
        except subprocess.CalledProcessError as e:
            print("Failed to set Linux wallpaper. Please try again.")
            logger.exception(e)
            logger.critical("Couldn't set background")
            check_bot_exception(e)
    else:
        print("Error: Unsupported Linux environment.")
        logger.critical("Unsupported Linux Distro")
        check_bot_exception("Unsupported Linux Distro")


def get_dist_script(image_path: set_image_background):
    """ Returns:
            None   # if Linux distro is not supported.
            string # script to change background for the current distro.
 """

    dist = distro.id()
    if dist == "ubuntu":
        distro_script = (
            f"gsettings set org.gnome.desktop.background "
            f"picture-uri file://{image_path}"
        )
    elif dist == "linuxmint":
        distro_script = (
            f"gsettings set org.cinnamon.desktop.background "
            f"picture-uri file://{image_path}"
        )
    else:
        distro_script = None
    return distro_script


def raise_bot_exception(option: bool):
    """ Takes option to throw BotException instead of sys.exit() or not.
    Initially False"""
    global BOT_EXCEPTION
    BOT_EXCEPTION = option


def check_bot_exception(message):
    """Based on global BOT_EXCEPTION variable, raises error or exits script"""
    if BOT_EXCEPTION:
        raise BotException(message)
    else:
        sys.exit()
