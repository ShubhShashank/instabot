#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
  import Tkinter as tk
except:
  import tkinter as tk

import threading, time, random
import instafunctions as insta

from splinter import Browser

class InstagramApp(tk.Tk):

  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.wm_title('InstaBot')

    container = tk.Frame(self)
    container.pack(side='top', fill='both', expand=True, padx=10)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    frame = MainPage(container, self)
    frame.grid(row=0, column=0, sticky='nsew')

class MainPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)

    tk.Label(self, text='Username:').pack(anchor='w')
    self.username = tk.StringVar()
    self.ent_username = tk.Entry(self, width=44, textvariable=self.username)
    self.ent_username.pack(anchor='w')

    tk.Label(self, text='Password:').pack(anchor='w')
    self.ent_password = tk.Entry(self, width=44)
    self.ent_password.pack(anchor='w')
    
    tk.Label(self, text='Minutes between executions').pack(anchor='w')
    self.ent_min_executions = tk.Entry(self, width=44)
    self.ent_min_executions.pack(anchor='w')

    tk.Label(self, text='Tags seperated by ","').pack(anchor='w')
    self.ent_tag = tk.Text(self, height=3, width=50)
    self.ent_tag.pack(anchor='w')

    tk.Label(self, text='Max number of likes per tag').pack(anchor='w')
    self.ent_max_likes_per_tag = tk.Entry(self, width=44)
    self.ent_max_likes_per_tag.pack(anchor='w')

    self.comment_photos = tk.IntVar()
    self.ent_comment_photos = tk.Checkbutton(self, text='Comment photos', variable=self.comment_photos)
    self.ent_comment_photos.pack(anchor='w')

    tk.Label(self, text='Comments separated by ","').pack(anchor='w')
    self.ent_comments = tk.Text(self, height=3, width=50)
    self.ent_comments.pack(anchor='w')

    tk.Button(self, text='Run', command=self.run).pack(side='left', anchor='w', pady=10)
    tk.Button(self, text='Stop', command=self.stop).pack(side='left', anchor='w', pady=10)

  def do_task(self):
    if self.active:
      username = self.username.get()
      password = self.ent_password.get()
      tags = [tag.strip() for tag in self.ent_tag.get("1.0",'end-1c').split(',')]
      max_likes_per_tag = self.ent_max_likes_per_tag.get()
      comment_photos = self.comment_photos.get()
      comments = [comment.strip() for comment in self.ent_comments.get("1.0",'end-1c').split(',')]
      
      min_executions = int(self.ent_min_executions.get()) * 60

      b = Browser('chrome')
      insta.go_to_page(b, 'http://instagram.com')

      if not insta.load_cookies(b, username):
        insta.login_at_instagram(b, username, password)

      for tag in tags:
        myTagSearch = insta.TagSearch(b, tag)
        
        for i in range( int(max_likes_per_tag) ):
          if not myTagSearch.is_liked():
            myTagSearch.like()
            
            if comment_photos == 1:
              comment = comments[ random.randrange( len(comments) ) ]
              myTagSearch.comment( comment )

          if not myTagSearch.next():
            break

      insta.save_cookies(b, username)
      b.quit()

      threading.Timer(min_executions, self.do_task).start()

  def run(self):
    self.active = True
    threading.Thread(target=self.do_task).start()

  def stop(self):
    self.active = False

app = InstagramApp()
app.mainloop()
