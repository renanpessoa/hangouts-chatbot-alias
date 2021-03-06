from flask import Flask, request, json
from oauth2client import client
import redis
import os 

application = Flask(__name__)

host_redis = os.environ.get('HOST_REDIS', 'redis')
redis = redis.Redis(host=host_redis, decode_responses=True)

def _help():
  """Send help text to Hangouts Chat."""
  text = """
```
Usage: @bot  [command] (message)

*Commands*:
  
  add      Adds specified users to notify list | To add yourself use key 'myself'
  list     Lists users on notify list
  remove   Removes specified users from notify list | To remove yourself use key 'myself'
  help     This help

 > Obs: All commands are optional

*Examples*:

  @bot add myself @Fulano     <= Will add yourself and @Fulano in list.
  @bot this a messge test     <= Send 'this a messge test' to all list.
  @bot remove myself @Fulano  <= Remove yourself and @fulano from list.

```
"""
  return text

def validate_token():

  # Bearer Tokens received by bots will always specify this issuer.
  CHAT_ISSUER = 'chat@system.gserviceaccount.com'

  # Url to obtain the public certificate for the issuer.
  PUBLIC_CERT_URL_PREFIX = 'https://www.googleapis.com/service_accounts/v1/metadata/x509/'

  # Intended audience of the token, which will be the project number of the bot.
  #Go to -> https://console.developers.google.com/iam-admin/settings?authuser=1&organizationId=$ORGANIZATIONID&project=$PROJECT_NAME
  PROJECT_NUMBER = ['']

  # Authorization HTTP header.
  BEARER_TOKEN = request.headers['Authorization'].split()[1]

  for project_number in PROJECT_NUMBER:
    try:
      # Verify valid token, signed by CHAT_ISSUER, intended for a third party.
      token = client.verify_id_token(
          BEARER_TOKEN, project_number, cert_uri=PUBLIC_CERT_URL_PREFIX + CHAT_ISSUER)
      break
    except Exception as err: 
      print(f'->> {err}')
      pass

  try: 
    if token['iss'] != CHAT_ISSUER:
      return 1, 'Invalid issuee, please contact administrator.'
    else:
      return 0, 'Ok'
  except:
      return 1, 'Invalid token, please contact administrator.'

def send_msg(texto, room_name):
  """Send message to Hangouts Chat."""
  members = redis.smembers(room_name)

  if str(members) == 'set()':

    text = '```There are no users in the list, please add with add command. For help type help.```'
    return text

  else:

    user = texto['message']['sender']['displayName']
    
    remove_botname = texto['message']['text'].split()[0]

    message = texto['message']['text'].replace(remove_botname,'')

    text = '%s: \n%s\n\n\n/cc %s ' % (user, message, ','.join(members))

    return text

def _list(room_name):
  """Send list of members to Hangouts Chat."""
  members = redis.smembers(room_name)
  
  if str(members) == 'set()':
    text = '```Users in list: none```'
    return text

  text = 'Users in list: %s ' % ','.join(members)
  
  return text

def _add(users, room_name): 
  """Add members in list and send to Hangouts Chat."""
  global users_added
  users_added = []

  try:

    for word in users['message']['text'].split():

      if word == 'myself':
        user = users['message']['sender']['name']
        check_result = redis.sadd(room_name, "<" + user + ">")
      
        if check_result == 1:
          users_added.append("<" + user + ">")
        else:
          users_added.append('Already added ->> ' + "<" + user + ">")

        check_continue = 1
        text = '```User added: %s ```' %  (','.join(users_added))

    for _item in range(len(users['message']['text'].split())):

      _item = _item + 1

      try:
        _type = users['message']['annotations'][_item]['userMention']['user']['type']
        user = users['message']['annotations'][_item]['userMention']['user']['name']
    
        if _type == 'BOT':

          if check_continue == 1:
            continue
          else:
            text = 'Please add user with @'
            continue
    
        user = users['message']['annotations'][_item]['userMention']['user']['name']
        check_result = redis.sadd(room_name, "<" + user + ">")

      except:
        pass

      if check_result == 1:
        users_added.append("<" + user + ">")
      else:
        users_added.append("Already added ->> " + "<" + user + ">")

    text = "```Added users: %s ```" % (','.join(list(set(users_added))))
    return text

  except:

    text = 'Please add user with @'
    return text


def _remove(users, room_name): 
  """Remove users from list and send to Hangouts Chat."""
  global users_removed
  users_removed = []

  try:

    for word in users['message']['text'].split():

      if word == 'myself':
        user = users['message']['sender']['name']
        check_result = redis.srem(room_name, "<" + user + ">")
      
        if check_result == 1:
          users_removed.append("<" + user + ">")
        else:
          users_removed.append('Not found ->> ' + "<" + user + ">")

        check_continue = 1
        text = '```User removed: %s ```' %  (','.join(users_removed))

    for _item in range(len(users['message']['text'].split())):

      _item = _item + 1

      try:
        _type = users['message']['annotations'][_item]['userMention']['user']['type']
        user = users['message']['annotations'][_item]['userMention']['user']['name']
    
        if _type == 'BOT':

          if check_continue == 1:
            continue
          else:
            text = 'Please add user with @'
            continue
    
        user = users['message']['annotations'][_item]['userMention']['user']['name']
        check_result = redis.srem(room_name, "<" + user + ">")

      except:
        pass

      if check_result == 1:
        users_removed.append("<" + user + ">")
      else:
        users_removed.append("Not found ->> " + "<" + user + ">")
    text = "```Removed users: %s ```" % (','.join(list(set(users_removed))))
    return text
  except:

    text = 'Please add user with @'
    return text

@application.route('/', methods=['POST'])
def on_event():
  """Handler for events from Hangouts Chat."""

  event = request.get_json()
 
  token_status, token_text = validate_token()

  if token_status != 0:
    return json.jsonify({'text': token_text})

  if event['type'] == 'ADDED_TO_SPACE' and event['space']['type'] == 'ROOM':
    text = 'Thanks for adding me to "%s"! For help type @bot help' % event['space']['displayName']
 
  elif event['type'] == 'MESSAGE':

    room_name = event['space']['name'].split('/')[1]
    commands = ['list', 'add', 'remove', 'help']

    try:
      param = event['message']['text'].split()[1:][0]
    except:
      text = _help()
      return json.jsonify({'text': text})

    if param in commands:

      if param == 'list':
       text = _list(room_name)

      elif param == 'add':
       text = _add(event, room_name)

      elif param == 'remove':
       text = _remove(event, room_name)

      elif param == 'help':
        text = _help()
        return json.jsonify({'text': text})
    
    else:
      text = send_msg(event, room_name)

  else:
    return
    
  return json.jsonify({'text': text})

if __name__ == '__main__':
  application.run(host='0.0.0.0')
