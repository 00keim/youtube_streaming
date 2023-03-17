import os
import subprocess
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
	path = '/home/username/youtube_streaming/'
	l = os.listdir(path + 'streamer/')

	for streamer in l:
		with open(path + 'streamer/' + streamer, 'r') as f:
			content = f.read().splitlines()
			key = content[0]
			channelId = content[1]
			if len(content) >=  3:
				last_videoId = content[2]
			else:
				last_videoId = None

		cmd = ['curl', 'https://www.googleapis.com/youtube/v3/search?key={0}&part=snippet&channelId={1}&eventType=live&type=video'.format(key, channelId)]
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		d = json.loads(result.stdout.decode())

		if d.get('items') == None:
			# error
			subject = 'error'
			body = 'an error has occurred while {} is open.'.format(streamer)
			sendmail(subject, body)
	
		elif d.get('items') == []:
			# not streaming
			continue

		else:
			# streaming
			channelTitle = d['items'][0]['snippet']['channelTitle']
			title = d['items'][0]['snippet']['title']
			videoId = d['items'][0]['id']['videoId']

			if videoId != last_videoId:
				subject = '{} is streaming now'.format(channelTitle)
				body = '{}\n'.format(title) + 'youtube.com/watch?v={}'.format(videoId)
				sendmail(subject, body)
				with open(path + 'streamer/' + streamer, 'w') as f:
					f.write(key + '\n' + channelId + '\n' +  videoId)

def sendmail(subject, body):
	
	smtp_server = 'smtp.gmail.com'
	port = 587
	server = smtplib.SMTP(smtp_server, port)

	server.starttls()

	from_address = 'from.example@gmail.com'
	password = 'password'
	to_address = 'to.example@gmail.com'

	server.login(from_address, password)

	message = MIMEMultipart()
	message['Subject'] = subject
	message['From'] = from_address
	message['To'] = to_address

	message.attach(MIMEText(body))

	server.send_message(message)

	server.quit()

if __name__ == '__main__':
	main()
