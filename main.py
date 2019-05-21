#! python wrapper/wrap.py


"""
A Reddit Bot that gets top Hot sorted picture from a given
Subreddit and sets it as background.

"""
import configparser
import logging
import pathlib
import sys

import requests

import bot

config = configparser.RawConfigParser()
config.read("etc/config.ini")

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
    reddit = bot.get_reddit(login=login_config)

    subreddit_name = input("Enter the subreddit you want to access: ")

    subreddit = bot.get_subreddit(reddit=reddit, name=subreddit_name)

    # Get picture submission based on 'Hot' sort
    picture = bot.get_picture_post(subreddit_sort=subreddit.hot())

    print(f"Title: {picture.title}")
    print(f"Author: {picture.author.name}\n")

    print("Downloading...")
    try:
        r = requests.get(url=picture.url)
        r.raise_for_status()
        logger.info("Downloading Picture")
        logger.debug(f"Getting request from picture {r}")
    except requests.RequestException as e:
        print(
            "Error: Connection broken; couldn't download image.",
            "Please try again."
        )
        logger.exception(f"{e}")
        logger.critical("Couldn't download image")
        sys.exit()
    print("Done.\n")

    # Getting image extension from url
    image_ext = pathlib.Path(picture.url).suffix

    # Getting picture path
    image_filename = picture.author.name + image_ext
    image_path = pathlib.Path(".").resolve() / "images" / image_filename

    bot.save_image(path=image_path, image=r.content)
    bot.set_image_background(image_path=str(image_path))

    print("Exiting..\n")
    logger.debug("End of program")


if __name__ == "__main__":
    main()
