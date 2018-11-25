import os
import sys
import sqlite3
from sqlite3 import Error
import pickle
import getpass
from requests import Session

cookie = ''

def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
  return None

def set_cookie():
  ck = ""
  sz = ""
  os.system('cp /home/aditya/.mozilla/firefox/x7yfuu12.default/cookies.sqlite /home/aditya')
  conn = create_connection('/home/aditya/cookies.sqlite')
  if (conn is None):
    print ('Could not connect to Cookies DB')
  else:
    try:
      cur = conn.cursor()
      cur.execute('SELECT value FROM moz_cookies WHERE baseDomain LIKE "%codeforces%" AND name = "X-User";')
      rows = cur.fetchall()
      for row in rows:
        ck = str(row[0])
        break
      cur = conn.cursor()
      cur.execute('SELECT value FROM moz_cookies WHERE baseDomain LIKE "%codeforces%" AND name = "70a7c28f3de";')
      rows = cur.fetchall()
      for row in rows:
        sz = str(row[0])
        break
      ck_dict = {'cookie' : ck, 'ftaa' : sz}
      with open('cookie_file.dat', 'wb') as cookie_file:
        cookie_file.truncate(0)
        pickle.dump(ck_dict, cookie_file, protocol=pickle.HIGHEST_PROTOCOL)
    except Error as e:
      print (e)
  os.system('rm /home/aditya/cookies.sqlite')
      

def get_cookie():
  ck = ''
  with open('cookie_file.dat', 'rb') as cookie_file:
    ck = pickle.load(cookie_file)
  return ck

def set_contest(contest_link):
  set_cookie()
  if (contest_link.find('problem') != -1):
    contest_link = contest_link.split('/problem')[0]
  contest_link = contest_link.replace('contests', 'contest')
  print (contest_link)
  with open('contest_file', 'w') as contest_file:
    contest_file.truncate(0)
    contest_file.write(contest_link)

def get_contest():
  contest_link = ''
  with open('contest_file', 'r') as contest_file:
    for line in contest_file:
      contest_link = line
      break
  return contest_link


def submit(problem_code):
  #Common headers for all requests
  contest_link = get_contest()
  #print (contest_link)
  submit_link = contest_link + '/submit'
  #print (submit_link)
  ck = get_cookie()
  cookie = ck['cookie']
  ftaa = ck['ftaa']
  #print (cookie)
  s = Session()
  s.cookies['X-User'] = cookie
  header = {
            'Host':'codeforces.com',
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'en-US,en;q=0.5',
            'Accept-Encoding':'gzip, deflate, br'
            }
  #End common headers
  submit_page = s.get(submit_link, headers = header)
  print (submit_page.text)
  '''csrf_token = (submit_page.text.split('name="X-Csrf-Token" content="')[1]).split('"')[0]
  bfaa = (submit_page.text.split('window._bfaa = "')[1]).split('"')[0]
  _tta = submit_page.text.split('name="_tta" value="')#[1]).split('"')[0]
  token_submit_link = submit_link + '?csrf_token=' + csrf_token
  print (csrf_token)
  print (bfaa)
  print (len(_tta))'''
  
  


#inp = sys.argv[1]
#inp = "https://codeforces.com/contest/911"
inp = 'A'
if (inp.find('codeforces.com') != -1):
  set_contest(inp)
else:
  submit(inp)

