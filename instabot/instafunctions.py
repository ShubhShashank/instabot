#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, json, os.path

def go_to_page(b, url):
  b.visit(url)
  time.sleep(5)

def go_to_longin_form(b):
  time.sleep(3)
  b.find_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a').click()

def make_login(b, username, password):
  b.find_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[1]/input').type( username )
  b.find_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/input').type( password )
  b.find_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button').click()
  time.sleep(5)

def login_at_instagram(b, username, password):
  go_to_longin_form(b)
  make_login(b, username, password)

def make_search(b, searchquery):
  # empty input box
  b.find_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[2]/input').type(searchquery)
  # selects the first box
  b.find_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[2]/div[2]/div[2]/div/a[1]/div/div[1]/span').click()

def make_tag_search(b, tag):
  url = 'https://www.instagram.com/explore/tags/' + tag + '/'
  go_to_page(b, url)


def save_cookies(b, username):
  file_name = username + '.json'
  myCookies = b.cookies.all()
  f = open(file_name, 'w')
  f.write( json.dumps(myCookies) )
  f.close()

def is_logged(b):
  return b.is_element_not_present_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[3]/div/div[3]/a')

def load_cookies(b, username):
  file_name = username + '.json'

  if not os.path.isfile(file_name):
    return False

  f = open(file_name)
  data = json.load(f)

  go_to_page(b, 'http://instagram.com')
  b.cookies.add( data )
  b.reload()

  #return is_logged(b)
  return True


def like_photos(b, counter):
  try:
    b.find_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/a[1]').first.click()
    while True:
      time.sleep(5)

      counter = counter - 1

      hearthElement = b.find_by_xpath('/html/body/div[2]/div/div[2]/div/article/div[2]/section[2]/a/span').first
      if not hearthElement.has_class('_soakw coreSpriteHeartFull'):
        hearthElement.click()

      if counter == 0:
        break

      b.find_by_css('.coreSpriteRightPaginationArrow').click()

    b.find_by_xpath('/html/body/div[2]/div/button').click()
  except:
    print('Error doing tag search')


def goToProfile(b):
  b.find_by_xpath('//*[@id="react-root"]/section/nav/div/div/div/div[3]/div/div[3]/a').click()



def scrollToBottomOfList(b):
  prev = 0
  while True:
    time.sleep(7)
    scrollTop = b.evaluate_script("document.getElementsByClassName('_4gt3b')[0].scrollTop")
    scrollHeight = b.evaluate_script("document.getElementsByClassName('_4gt3b')[0].scrollHeight")

    if scrollHeight == prev:
      break

    prev = scrollHeight
    b.execute_script("document.getElementsByClassName('_4gt3b')[0].scrollTop = document.getElementsByClassName('_4gt3b')[0].scrollHeight")


def list_following(b):
  goToProfile(b)
  b.find_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a').click()
  scrollToBottomOfList(b)

def list_followers(b):
  goToProfile(b)
  b.find_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a').click()
  scrollToBottomOfList(b)

# Tag Search Iterator
class TagSearch(object):
  def __init__(self, b, tag):
    self.b = b
    self.tag = tag
    
    self.prev_url = None

    make_tag_search(self.b, self.tag)
    self.b.find_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div[1]/a[1]').first.click()
    
  def is_liked(self):
    return self.b.find_by_xpath('/html/body/div[2]/div/div[2]/div/article/div[2]/section[2]/a/span').first.has_class('_soakw coreSpriteHeartFull')

  def like(self):      
    self.b.find_by_xpath('/html/body/div[2]/div/div[2]/div/article/div[2]/section[2]/a/span').first.click()
    time.sleep(2)


  def comment(self, comment):
    my_comment = comment + '\n\r\r'
    self.b.find_by_xpath('/html/body/div[2]/div/div[2]/div/article/div[2]/section[2]/form/input').fill(my_comment)
    time.sleep(5)

  def next(self):
    if self.prev_url == self.b.url:
      return False
      
    self.prev_url = self.b.url
    self.b.find_by_css('.coreSpriteRightPaginationArrow').click()
    time.sleep(5)
    return True
