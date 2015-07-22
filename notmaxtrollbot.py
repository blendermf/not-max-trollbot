import praw
import time
from praw.handlers import MultiprocessHandler
import OAuth2Util
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import *

import config

handler = MultiprocessHandler()

r = praw.Reddit(user_agent="DiamondClub subreddit moderation script by /u/blendermf v 0.1.", handler=handler)

o = OAuth2Util.OAuth2Util(r)

scheduler = BackgroundScheduler()
scheduler.add_jobstore('sqlalchemy', url='mysql+pymysql://{}:{}@{}/{}'.format(config.db_user, config.db_pass, config.db_host, config.db_name))

def post_diamondtime():
	now = datetime.now(timezone('US/Eastern'))
	episode_date = now + relativedelta(weekday=TU, hour=22, minute=0, second=0, microsecond=0)
	title = u'Weekly Diamond Time Submissions - For Episode on {0:%b %d, %Y}'.format(episode_date)

	f = open('diamondtime-text.md', 'r')
	text = f.read()

	sub = r.submit('diamondclub',title,text,save=False)
	sub.set_contest_mode(True)
	sub.set_flair(flair_text=u'Diamond Time',flair_css_class=u'diamondtime')
	sub.sticky(bottom=False)
	sub.distinguish(as_made_by=u'mod')

	print('Diamond time posted.')

scheduler.add_job(post_diamondtime, 'cron', day_of_week='wed', hour=3, minute=10, timezone=timezone('US/Eastern'), replace_existing=True, id="post_diamondtime")
scheduler.start()
scheduler.print_jobs()

while True:
	time.sleep(3)
scheduler.shutdown()

