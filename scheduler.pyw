#!/usr/bin/env python

import pathlib as pl
import subprocess
import random

BASE_DIR = pl.Path(__file__).parent
SUBREDDITS_PATH = BASE_DIR / pl.Path("subreddits.txt")
BOT_PATH = BASE_DIR / pl.Path("main.py")

with open(SUBREDDITS_PATH) as subs:
    subreddits = subs.read().split()

subreddit = random.choice(subreddits)
subprocess.Popen(
    f"python {BOT_PATH} {subreddit} -y", shell=True, cwd=BASE_DIR
)
