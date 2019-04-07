#! python wrapper/wrap.py


"""
A Reddit Bot that gets top Hot sorted picture from a given
Subreddit and sets it as background.

"""
import configparser
import logging
import os
import sys

import requests

import botFunctions as bot

config = configparser.RawConfigParser()
config.read("etc/config.ini")

# Setting up Logging configuration
log_config = config["Logging"]
logging.basicConfig(
    filename=log_config["filename"],
    filemode=log_config["filemode"],
    level=int(log_config["level"]),
    format=log_config["format"]
)
logger = logging.getLogger(__name__)


def main():
    logger.debug("Start of Program.")
    print("""
+---------------------------+
| W A L L P A P E R   B.O.T |
+---------------------------+
    """)

    # Create reddit object
    login_config = config["Login"]
    reddit = bot.getReddit(login=login_config)

    # Getting user-specified subreddit
    subreddit_name = input("Enter the subreddit you want to access: ")
    if not subreddit_name:
        print("Error: Empty subreddit entered. Please try again.\n")
        logger.critical("Empty subreddit entered")
        sys.exit()

    # Create subreddit object
    subreddit = bot.getSubreddit(reddit=reddit, name=subreddit_name)

    # Get picture submission based on 'Hot' sort
    picture = bot.getPicturePost(subreddit_sort=subreddit.hot())

    # Printing title of picture
    print(f"Title: {picture.title}")
    print(f"Author: {picture.author.name}\n")

    # Downloading Picture
    print("Downloading...")
    try:
        r = requests.get(url=picture.url)
        r.raise_for_status()
        logger.info("Downloading Picture")
        logger.debug(f"Getting request from picture {r}")
    except Exception as e:
        print(f"Error: {e}. Please try again.")
        logger.exception(f"{e}")
        logger.critical("Couldn't download image")
        sys.exit()
    print("Done.\n")

    # Getting image extension from url
    image_ext = os.path.splitext(picture.url)[1]

    # Opening and saving picture
    image_filename = picture.author.name + image_ext
    image_path = os.path.join(os.path.abspath("images/"), image_filename)
    bot.saveImage(path=image_path, image=r.content)

    # Setting picture as background[Y/N] User choice
    print("Set picture as background? [Y/N] : ", end="")
    logger.debug("Starting loop")
    while True:
        logger.debug("Getting user input")
        choice = input()
        if choice == "Y" or choice == "y":
            logger.info(f"User choice: {choice}")
            bot.setImageBackground(path=image_path)
            logger.debug("Set picture as background")
            print("Done.\n")
            break
        elif choice == "n" or choice == "N":
            logger.info(f"User choice: {choice}")
            logger.debug("Displaying image full path")
            print(
                f"Image path is : {image_path}"
            )
            break

    print("Exiting..\n")
    logger.debug("End of program")


if __name__ == "__main__":
    main()
