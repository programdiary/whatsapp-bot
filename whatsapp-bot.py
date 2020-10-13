from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import emoji
import random
import datetime

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg+'..')
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if incoming_msg in ['hello','hi','hey','start','hii']:
            response = """
            *Hello!! Welcome to ProgramDiary Bot* 
        Let me help you with some reading stuff. Happy Learing!!

        Here are some option to get you started:
        > *'read'*: Get some interesting post from ProgramDiary.com.
        > *'news'*: Latest news from around the world.
        > *'quote':* Get some inspirational quote!
        > *'meme'*: Top memes for fun from r/memes."""
            msg.body(response)
            responded = True

    elif 'read' in incoming_msg:
        #Get random post from programdiary.com
        post_list = ['http://programdiary.com/post/create-twitter-bot-using-tweepy', 'http://programdiary.com/post/compilation-and-execution-process-of-java-python-c-cplusplus-csharp', 'http://programdiary.com/post/5-key-points-to-keep-in-mind-while-starting-automation-testing-for-new-project', 'http://programdiary.com/post/what-is-devsecops', 'http://programdiary.com/post/jenkins-master-slave-setup-on-aws-using-ec2-instances']
        result = random.choice(post_list)
        msg.body(result)
        responded = True
        
    elif 'news' in incoming_msg:
        # Get new around the world
        r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news,the-washington-post,cnbc,abc-news,techcrunch.com,thenextweb.com,independent&apiKey=d6a95548bdd443c2b3bbe38943f6b360')
            
        if r.status_code == 200:
            data = r.json()
            articles = data['articles'][:5]
            result = ''
                
            for article in articles:
                title = article['title']
                url = article['url']
                if 'Z' in article['publishedAt']:
                    published_at = datetime.datetime.strptime(article['publishedAt'][:19], "%Y-%m-%dT%H:%M:%S")
                else:
                   published_at = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%S%z")
                result += """
                *{}*
                Read more: {}
                _Published at {:02}/{:02}/{:02} {:02}:{:02}:{:02} UTC_
                """.format(
                    title,
                    url,
                    published_at.day,
                    published_at.month,
                    published_at.year, 
                    published_at.hour,
                    published_at.minute,
                    published_at.second
                    )
        else:
            result = ' Sorry! We cannot fetch news at this time.'

        msg.body(result)
        responded = True
    
    elif 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Sorry! We could not retrieve a quote at this time.'
        msg.body(quote)
        responded = True
    
    elif 'meme' in incoming_msg:
            r = requests.get('https://www.reddit.com/r/memes/top.json?limit=20?t=day', headers = {'User-agent': 'whatsbot 0.1'})
            
            if r.status_code == 200:
                data = r.json()
                memes = data['data']['children']
                random_meme = random.choice(memes)
                meme_data = random_meme['data']
                title = meme_data['title']
                image = meme_data['url']

                msg.body(title)
                msg.media(image)
            
            else:
                msg.body('Sorry, We cannot find memes at this time.')

            responded = True

    if not responded:
        msg.body('We can only help you with Read, News, Quotes and Memes')
    return str(resp)


if __name__ == '__main__':
    app.run()