import praw
from time import sleep
from collections import deque

r = praw.Reddit("LonghornMod by /u/thirdegree")

streamUrl = "https://www.youtube.com/watch?v=fB4wW6NB2-Y"
streamPass = "none"
SUBREDDIT = "LonghornNation"
MIN_KARMA = 50

has_enough = []
done_subs = deque(maxlen=200)

def _login():
	USERNAME = raw_input("Username? longhornmod\n")
	PASSWORD = raw_input("Password hookemhorns\n")
	print "logging in............"
	r.login(USERNAME, PASSWORD)
	print "welcome longhornmod"
	return USERNAME

def check_inbox():
	comments = r.get_unread()
	for post in comments:
		print "processing " + post.author.name
		if post.author.name.lower() in has_enough or enough_karma(post.author.name):
			print "accepted"
			r.send_message(post.author.name, "Stream Invite", "URL: %s\n\nPassword: %s"%(streamUrl, streamPass))
			print "stream sent out\n\n"
		else:
			print "rejected"
			r.send_message(post.author.name,"Stream Invite", "I'm sorry, but you do not have enough karma in this subreddit. If you would like to know why please visit the wiki for /r/LonghornNation and find the FAQs. Hook 'em!")
			print "rejection sent out\n\n"
		post.mark_as_read()

def check_subs():
	subs = r.get_subreddit(SUBREDDIT).get_new(limit=25)
	for sub in subs:
		if "[Game Day Thread]" in sub.title and sub.id not in done_subs:
			print "found new GDT"
			done_subs.appead(sub.id)
			sub.add_comment("Comment here if you would like the password for the stream. A reminder, you must have >=300 karma (link+comment) in /r/LonghornNation to receive the password.")
			print "commented in GDT"
			sleep(2)

def enough_karma(username):
	user = r.get_redditor(username)
	print "1"
	overview = user.get_overview(limit=None)
	print "2"
	acc=0
	for post in overview:
		if post.subreddit.display_name.lower() == SUBREDDIT.lower():
			acc += post.score
			if acc >= MIN_KARMA:
				has_enough.append(username.lower())
				return True
	return False

def to_from_file(has_enough):
	with open("users", "r") as w:
		w = w.read()
		w = filter(lambda x: x!= '', w.split("\n"))
	with open("users", "w") as u:
		u.write("\n".join(has_enough))
	return has_enough

if __name__ == '__main__':
	_login()
	running = True
	try:
		has_enough = [i.strip() for i in file('users').read().split('\n')]
	except IOError:
		f = open("users", "w")
		f.close()
	while running:
		try:
			check_inbox()
			check_subs()
			has_enough = to_from_file(has_enough)
			sleep(5)
		except Exception as e:
			print e
			sleep(60)
