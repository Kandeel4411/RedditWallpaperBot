import configparser
from pathlib import Path

import praw
import pytest

import bot

# Getting bot credentials
config = configparser.RawConfigParser()
config.read("etc/config.ini")
login_config = config["Login"]

# Turning on bot exception
bot.raise_bot_exception(option=True)

# Dummy reddit object to test
reddit = bot.get_reddit(login=login_config)


def test_bot_exception():
    """ Tests that bot exception was turned on """

    assert bot.BOT_EXCEPTION, "Failed to turn on bot exception"


def test_get_reddit():
    """ Tests get_reddit() to return reddit object"""

    assert isinstance(bot.get_reddit(login=login_config),
                      praw.Reddit), "Didn't return reddit object"


def test_get_subredit_empty_name():
    """ Tests get_subreddit() with empty name given """

    with pytest.raises(bot.BotException, match="Couldn't create Subreddit Object") as exp:
        bot.get_subreddit(reddit=reddit, name="")


def test_get_subreddit():
    """ Tests get_subreddit() to return subreddit object """

    assert bot.get_subreddit(
        reddit=reddit, name="Test") == reddit.subreddit("Test"), "Didn't return subreddit object"


def test_get_picture_post_invalid_subreddit():
    """ Tests get_picture_post() with invalid subreddit """

    subreddit = bot.get_subreddit(reddit=reddit, name="1231ijdjabshdn")
    with pytest.raises(bot.BotException, match="Couldn't access subreddit"):
        bot.get_picture_post(subreddit_sort=subreddit.hot())


def test_get_picture_post_invalid_login():
    """ Tests get_picture_post() with invalid login reddit """

    false_login = {
        "client_id": "1",
        "client_secret": "2",
        "user_agent": "3",
    }
    reddit = bot.get_reddit(login=false_login)
    # :D
    subreddit = bot.get_subreddit(reddit=reddit, name="anime")
    with pytest.raises(bot.BotException, match="Invalid client_ID or client_secret"):
        bot.get_picture_post(subreddit_sort=subreddit.hot())


def test_get_picture_post_no_pic_found():
    """ Tests get_picture_post() with no picture found in subreddit"""

    subreddit = bot.get_subreddit(reddit=reddit, name="Python")
    with pytest.raises(bot.BotException, match="No picture posts in the defined limit"):
        bot.get_picture_post(subreddit_sort=subreddit.hot(limit=0))


def test_get_picture_post():
    """ Tests get_picture_post() to return picture submission """

    subreddit = bot.get_subreddit(reddit=reddit, name="wallpapers")
    picture = bot.get_picture_post(subreddit_sort=subreddit.hot())

    assert picture in subreddit.hot()


def test_create_image_folder():
    """ Tests create_image_folder() to create directory """

    fake_path = "fake_images/"
    bot.create_image_folder(path=fake_path)
    assert Path.exists(Path(fake_path)), "Couldn't find image directory"

    # Removing test path
    Path.rmdir(Path(fake_path))


def test_save_image():
    """ Tests save_image to create image"""

    fake_path = "fake_images/Fakeimage.jpg"
    fake_image = b"FakeFakeFake"

    bot.save_image(path=fake_path, image=fake_image)
    assert Path.exists(Path(fake_path)), "Fake image wasn't created"

    # Removing test path & image
    Path.unlink(Path(fake_path))
    Path.rmdir(Path(fake_path).parent)
