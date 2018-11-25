import os
import sys
import sqlite3
from sqlite3 import Error
import pickle
import requests
from bs4 import BeautifulSoup


# NOTE : This code works if you are logged in to codeforces in firefox
# Codeforces cookies expire once in a month on a browser with remember me option selected


'''
Change following values according to your browser:
1. Go to Firefox browser
2. Login/Relogin to codeforces and check option for Remember me for a month
3. Go to http://codeforces.com and Inspect Element
4. search all these parameters separately : bfaa, _tta, csrf_token
5. substitute values below
'''

language_id = '50'                              # value changed automatically based on file extension java, py3 or cpp14
source_file = '/home/aditya/.config/sublime-text-3/Packages/User/sublime.cpp' # Enter default location here, argument may be given to override default
ftaa = ''                                       # obtained automatically from cookie
csrf_token = '2413aa211b9a066f8df27be1677dca82' # values changed automatically from webpage
_tta = '993'                                    # cannot change this automatically due to hidden input, working on it
bfaa = '51650df53d9d5ca38b72ec50f2ac4219'       # change this according to your browser


def create_connection(db_file): # create sqlite connection for cookie file
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
  return None


def set_cookie(): # store latest cookies in pickle file
  ck1 = ''
  ck2 = ''
  ck3 = ''
  ck_dict = {}
  
  ''' Firefox / Chrome cookies are stored in sqlite db
      However they have lock acquired in their original location (browser process is expected to be running)
      Hence the need to copy to another location
      Chrome cookies are encrypted and is difficult to decrypt them on Linux
      So I have decided to make only for Firefox for now '''
  
  os.system('cp /home/aditya/.mozilla/firefox/x7yfuu12.default/cookies.sqlite /home/aditya')
  # change line to location of firefox cookies on your system, ideally only 'x7yfuu12' and usernames should be different

  conn = create_connection('/home/aditya/cookies.sqlite')
  # change line, ideally only username should be different
  
  if (conn is None):
    print ('Could not connect to Cookies DB')
  else:
    try:
      cur = conn.cursor()
      cur.execute('SELECT name, value FROM moz_cookies WHERE baseDomain LIKE "%codeforces%";')
      rows = cur.fetchall()
      for row in rows:
        ck_name = str(row[0])
        ck_value = str(row[1])
        ck_dict[ck_name] = ck_value
      
      '' 'Store cookie data in pickle file '''
      
      with open('cookie_file.dat', 'wb') as cookie_file:
        cookie_file.truncate(0)
        pickle.dump(ck_dict, cookie_file, protocol=pickle.HIGHEST_PROTOCOL)
    except Error as e:
      print (e)
  os.system('rm /home/aditya/cookies.sqlite')
  # change line, ideally only username should be different


def get_cookie(): # retrieve latest cookies from pickle file
  ck = ''
  with open('cookie_file.dat', 'rb') as cookie_file:
    ck = pickle.load(cookie_file)
  return ck


def set_contest(contest_link): # set contest link before start of contest (automatically sets cookies also)
  set_cookie()
  if (contest_link.find('problem') != -1):
    contest_link = contest_link.split('/problem')[0]
  contest_link = contest_link.replace('contests', 'contest')
  with open('contest_file', 'w') as contest_file:
    contest_file.truncate(0)
    contest_file.write(contest_link)


def get_contest(): # gets contest link from file
  contest_link = ''
  with open('contest_file', 'r') as contest_file:
    for line in contest_file:
      contest_link = line
      break
  return contest_link


def get_source(): # source code extraction from specified file
  global source_file
  sf = source_file
  try:
    sf = sys.argv[2]
  except:
    troll = 1
  source_file = sf
  global language_id                    # language selection based on extension of file (default: cpp14)
  if (source_file[-3:] == '.py'):
    language_id = '31'
  elif (source_file[-4:] == 'java'):
    language_id = '36'
  else:
    language_id = '50'
  try:
    with open(source_file, 'r') as f:
      source = f.read()
    return source
  except:
    return None
  return None


def submit(problem_code):       # code to submit problem
  contest_link = get_contest()
  verdict_link = contest_link + '/my'
  submit_link = contest_link + '/submit'
  cookies = get_cookie()
  s = requests.Session()      # start session

  for ck_name, ck_value in cookies.items():
    s.cookies[ck_name] = ck_value

  headers = {
            'Host':'codeforces.com',
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'en-US,en;q=0.5',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':contest_link,
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1'
            }  
  
  submit_page = s.post(submit_link, headers=headers, cookies=cookies) # try to find details from submit page
  global csrf_token
  global _tta
  global bfaa
  global ftaa
  global language_id
  soup = BeautifulSoup(submit_page.content, 'html.parser')
  print (str(soup.body.find('div', id='body').find('form')))
  try:
    csrf_token = str(soup.body.find('div', id='body').find('form').find('input', type='hidden')['value']) # usually available in response
  except:
    print ('no csrf_token found, falling back to hardcoded values')
    None
  try:
    _tta = str(soup.find('input', name='_tta').attrs['content']) # usually unavailable in response, falls back to hardcoded value
    print (__tta)
  except:
    print ('no _tta found, falling back to hardcoded value')
    None
  token_submit_link = submit_link + '?csrf_token=' + csrf_token
  headers = {
            'Host':'codeforces.com',
            'User-Agent':'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'en-US,en;q=0.5',
            'Referer' : submit_link,
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Connection' : 'keep-alive',
            'Upgrade-Insecure-Requests' : '1'
            }

  params = (('csrf_token', csrf_token),)

  source = get_source()
  
  data = {
        'csrf_token': csrf_token,
        'ftaa': cookies['70a7c28f3de'],
        'bfaa': bfaa,
        'action': 'submitSolutionFormSubmitted',
        'submittedProblemIndex': problem_code,
        'programTypeId': language_id,
        'source': source,
        'tabSize': '4',
        'sourceFile': '',
        '_tta': _tta
        }
  if source is None:
    print ('Wrong file')
  else:
    response = s.post(token_submit_link, headers = headers, params=params, cookies=cookies, data=data)
    if (response.text.find('You have submitted exactly the same code before') != -1):
      print ('Same Code uploaded Twice -> not submitted')
    else:
      print ('Submitted')
      print ('Check verdict at ' + verdict_link)
        

try:
  inp = sys.argv[1]
  #inp = "https://codeforces.com/contest/911"
  #inp = 'A'
  ''' usage python3 cf_submitter.py contest_link ----> sets the contest link
            python3 cf_submitter.py problem_ID file_path(optional) ----> submits the problem !!!
            '''
  if (inp.find('codeforces.com') != -1):
    set_contest(inp)
  else:
    submit(inp)
except:
  print (''' usage python3 cf_submitter.py contest_link ----> sets the contest link and cookies
            python3 cf_submitter.py problem_ID file_path(optional) ----> submits the problem !!!
            ''')
          

