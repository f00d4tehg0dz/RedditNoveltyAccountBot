#!/usr/bin/python
#loosly based off https://github.com/shantnu/RedditBot/ bot.
import praw
import pdb
import re
import os
from bot_config import *

# Check that the file that contains our username exists
if not os.path.isfile("bot_config.py"):
    print "You must create a bot_config file with your username and password."
    print "Please see bot_config_template.py"
    exit(1)

# Create the Reddit instance
user_agent = ("I love pizza bot 1.0")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(R_USERNAME, R_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have seen and replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)

# Get the top 10 values from the subreddits
multi_reddits = r.get_subreddit('pics+adviceanimals+funny+aww+gaming+videos')

for submission in multi_reddits.get_hot(limit=20):
    # print comment.title
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    already_done = set()
    for comment in flat_comments:
            try:
            	#edit the "pizza" line to anything you want it to search for
                if "Pizza" in comment.body and comment.id not in already_done:
                        #edit the "yum" line to anything you want it to reply with.
                        comment.reply('Yum!')
                        already_done.add(comment.id)
            except AttributeError:
                pass
            # Store the current id into our list
            posts_replied_to.append(submission.id)
            posts_replied_to.append(comment.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
