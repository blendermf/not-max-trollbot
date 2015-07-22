import praw
import OAuth2Util

r = praw.Reddit("DiamondClub subreddit moderation script by /u/blendermf v 0.1.")

o = OAuth2Util.OAuth2Util(r)

print(r.get_me())