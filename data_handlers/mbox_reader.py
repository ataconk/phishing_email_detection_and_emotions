#!/usr/bin/env python3

import email
from email.policy import default


# class for reading a mails file with a specific format (mbox) and allows for iteration over the messages in the file.
class MboxReader:
    # It opens the file in binary mode and reads the first line, which should start with "From ".   
    def __init__(self, filename):
        self.handle = open(filename, 'rb')
        assert self.handle.readline().startswith(b'From ')

    # enter and exit methods are for context management and allow the use of the "with" statement. 
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.handle.close()

    def __iter__(self):
        return iter(self.__next__())

    def __next__(self):
        lines = []
        while True:
            line = self.handle.readline()
            if line == b'' or line.startswith(b'From '):
                yield email.message_from_bytes(b''.join(lines), policy=default)
                if line == b'':
                    break
                lines = []
                continue
            lines.append(line)



import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def get_body(email):
    try:
            body = remove_tags(email.split('Content-Transfer-Encoding')[1])
            body = body.split('Content-Type')[0]
            body = body.replace('\n', ' ').replace('\t',' ').replace('&nbsp','').replace('= ', '')
            body = body.replace('=20', '').replace('=97', '').replace(';','')
            body = body.split('Mail message body')[1]
            body = body.split('--==============')[0]
            body = body.strip()
            return body
            
    except:
        pass
    
import re

TAG_RE = re.compile(r'<[^>]+>')

# following function are for cleaning the text
def remove_tags(text):
    return TAG_RE.sub('', text)
bodies = []

def not_unicode_or_backslash(x):
    try:
        x = x.encode('unicode-escape').decode()
    finally:
        return not x.startswith("\\")

def clean_body(body):
    body = re.sub(r"{.*}", "{{}}", body)
    body = body.replace('\n', ' ')
    body = ' '.join(word for word in body.split(' ') if not word.startswith('&'))
    body = ' '.join(word for word in body.split(' ') if not word.startswith('#'))
    body = ' '.join(word for word in body.split(' ') if not word.startswith('.'))
    body = ' '.join(word for word in body.split(' ') if not word.startswith('='))
    body = ' '.join(word for word in body.split(' ') if not word.startswith('|'))
     
    body = body.replace('&nbsp;', ' ')
    body = body.replace('&amp;', ' ')
    body = body.replace('=0D', ' ')
    body = body.replace('=A0', ' ')
    body = body.replace('=20', ' ')
    body = body.replace('=E9', ' ')
    body = body.replace('&copy;', ' ')
    body = body.replace('udca0', ' ')
    body = body.replace('udce2', ' ')
    body = body.replace('= ', '')
    body = re.sub(r'http\S+', '', body)
    # body = body.replace('\\', '')
    body = body.strip()
    body = " ".join(body.split()) 

    
    body = ' '.join(word for word in body.split(' ') if not_unicode_or_backslash(word))
    try: 
        body = body.split('--')[0]
    except:
        pass

    try: 
        body = body.split('**')[0]
    except:
        pass
    return body

# this part runs all functions that are defined above
with MboxReader('/Users/atacank/Downloads/phishing-2021.mbox') as mbox:
    counter = 0
    for message in mbox:

        counter = counter + 1

        try:
            body = remove_tags(' '.join(word for word in message._payload[0]._payload.split(' ') if not word.startswith('0x')))
            # print(body)
            body = clean_body(body)
            # print(body)
            bodies.append(body)
        except:
            try: 
                body = remove_tags(' '.join(word for word in message._payload.split(' ') if not word.startswith('0x')))
                body = clean_body(body)
                bodies.append(body)
            except Exception as e:
                # print(e, counter)
                pass

print(counter)