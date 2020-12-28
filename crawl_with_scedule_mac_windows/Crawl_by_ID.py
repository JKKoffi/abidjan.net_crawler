#!/usr/bin/env python
# coding: utf-8

# # Crawl Abidjan.net annonce by ID
# 
# We'll use an ID to crawl and preprocess all of these annonce.

# ## Imports  libraries

# In[21]:


import time
import os
import numpy as np  
from datetime import datetime
import pandas as pd

import io
import requests
from string import punctuation
import locale
from datetime import datetime
import re
from bs4 import BeautifulSoup, SoupStrainer
import requests
import sys
import time
from datetime import datetime


# ## Utility functions

# In[22]:


def create_dir(dir_path):
  if not os.path.exists(dir_path):
    os.makedirs(dir_path)
  print("Done")

#mesure elapsed time
from contextlib import contextmanager
from timeit import default_timer
@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

# def save_history(df):
      
#       if not os.path.exists(path_to_history):
#         df.to_csv(path_to_history, header=True, encoding='utf-16le', index =False,mode='a')
#       else:
#         df1 = pd.read_csv(path_to_history, encoding='utf-16le')
#         df_full = pd.concat([df1, df],axis=0)
#         df_full = df_full.reset_index()
#         df_full = df_full.drop_duplicates()
#         df.to_csv(path_to_history, header=True, encoding='utf-16le', index =False,mode='a')


            
def search_links_id(start_id):

  pages = []
  j=start_id
  stop = False
  i = 0
  while stop ==False:

      url = f'https://business.abidjan.net/AL/a/{j}.asp'
      response = requests.get(url)
      if response.ok:
        pages.append(url)
        i = 0
      else:
        i +=1
        if i>2000: #stop if more than 50 pages are failled
          stop=True
      j +=1
      # save_history(pd.DataFrame({'pages':url},index=[0]))
  df = pd.DataFrame({'pages':pages})
  return df


def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start



""" Crawle page data"""

import re
from bs4 import BeautifulSoup, SoupStrainer
import requests

def crawl_data(df_links):

  session = requests.Session()

  data = []
  mesure_complexity = {} # jsut to measure the execution time
  pages_fail = []

  N=df_links.shape[0]
  i = 0


  # with elapsed_timer() as elapsed:    
  # if i>4:
  #     time.sleep(20)
  for link in df_links.iloc[:,0].tolist():
    data1 = []
    download_url = link
    data1.append(download_url)
    try:
      response = session.get(download_url)
      try:
        soup = BeautifulSoup(response.text, 'html.parser')
        # elem = soup.find("div", {"id": "module"})
        # data1 = [
        #           download_url,
        #           elem.next_sibling.next_sibling.next_sibling.next_sibling.text,
        #           elem.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
        #         ]
        elem = soup.findAll("div", {"id": "module"})
        data1 = [
                  download_url,
                  elem[0].text,elem[1].text,elem[2].text
                ]
        print(len(data1[2]))    
        data.append(data1)
        print(f'{download_url} done!')
      except:
        try:
          soup = BeautifulSoup(response.text, 'html.parser')
          # elem = soup.find("div", {"id": "shadow"})
          elem = soup.find("div", {"id": "page_content"})
          data1 = [download_url,elem.text]
          print(len(data1[1]))
          data.append(data1)
        except:
          print(f'failed on {download_url}')
          pages_fail.append(download_url)
    except:
        pages_fail.append(download_url)
    # time.sleep(5)
    i +=1
    prog = ((i+1)/N) * 100
    print('\rCompleted: {:.2f}%'.format(prog),end=' ')



  df_2 = pd.DataFrame({'link':[x[0] for x in data if len(x)==2], "content":[x[1] for x in data if len(x)==2]})
  df_3 = pd.DataFrame({'link':[x[0] for x in data if len(x)==4], "header":[x[2] for x in data if len(x)==4],"content":[x[3] for x in data if len(x)==4]})  
  df_fail = pd.DataFrame({'pages':pages_fail}) 
  df_fail.to_csv(os.path.join(dir_result,'pages_failed.csv'), header=True, encoding='utf-16le', index =False , sep=';',mode="a")

  df_3['page-content'] = df_3['header']+''+df_3['content']
  df_2['page-content'] = df_2['content']
  df_merged = pd.DataFrame()
  columns=['link', 'page-content']
  df_merged = pd.concat([df_2.loc[:,columns], df_3.loc[:,columns]], axis=0)
  df_merged = df_merged.reset_index()
  df_merged = df_merged.drop(['index'], axis = 1)

  return df_merged


import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')
# src:https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

from string import punctuation
def remove_punctuations(string):
	for pct in punctuation:
		string = string.replace(pct,' ')
		string = re.sub('\s\s+',' ',string)
	return string


def decode_encode(string):
  bytestring = string.encode('ascii', 'ignore').decode('ascii')#.encode('utf-8')
  return bytestring#.decode('utf-8')

#find email
def find_email(string):
  try:
    email_found = re.findall(r'[\w]*@[\w]*.[\w]*', string)
    if len(email_found)==1:
      return email_found[0]
    else:
      chr = ''
      for x in email_found:
        chr += '/'+ x
      return chr
  except:
    pass

#find capital
def find_capital(string):

  string = remove_punctuations(string)
  string = string.replace('FRANCS CFA','FCFA')
  # string = string.replace('F CFA', 'FCFA')
  string0 = string.replace(' ','')
  string0 = string0.replace('DE','')
  try:
    return float(re.findall(r'[0-9]{7,12}FCFA', string0)[0].replace('FCFA', ''))
  except:
    try:
      start = string.lower().find('capital')
      string1 = string1[start,start+15]
      return float(re.findall(r'[0-9]{7,12}', string0)[0].replace('FCFA', ''))
    except:
      pass

def find_tel(string):
  string = remove_accents(string).lower()
  start = string.find('tel')
  if start!=-1:
    string = string[start:]
    string = remove_punctuations(string)
    # string = string.replace('225','')
    stop = string.find('capital') 
    string = string[:stop]
    chr = ''
    string = string.replace(' ','')
    string = re.findall(r'[0-9]{8,8}', string)
    for x in string:
      chr += x+'|'
    return chr


  string = string
  string = remove_punctuations(string)
  # string = string.replace('225','')
  stop = string.find('fax') 
  string = string[:stop]
  chr = ''
  string = string.replace(' ','')
  string = re.findall(r'[0-9]{8,8}', string)
  for x in string:
    chr += x+'|'
  return chr


def find_fax(string):
  string = remove_accents(string).lower()
  start = string.find('fax')
  if start!=-1:
    string = string[start:]
    string = remove_punctuations(string)
    string = string.replace('225','')
    string = string[:20]
    chr = ''
    string = string.replace(' ','')
    string = re.findall(r'[0-9]{8,8}', string)
    for x in string:
      chr +=' '+x
    return chr

def find_notaire(string):
  start = string.lower().find('notaire')
  string = string[start:start+50]
  string0 =  re.findall(r'[A-Z]{2,20}',string)
  if len(string0)!=0:
    chr = ''
    for x in string0:
      chr += ' '+x
    return chr
  else:
    stop = string.find('date')
    string1 = string[:stop]
    start = string1.find(':')
    try:
      int(string1[start:])
    except:
      return string1[start:]


def find_cat(string):
  start = string.lower().find('catégorie')
  string = string[start:start+100]
  stop=string.lower().find('avocat')
  string = string[:stop-1]
  string0 =  re.findall(r'[A-Z]{2,20}',string)
  if len(string0)!=0:
    chr = ''
    for x in string0:
      chr += ' '+x
    return chr

def find_cat(string):
  start = remove_accents(string).lower().find('catégorie')
  if start!=-1:
    
    string = string[start:start+100]
    stop=string.lower().find('avocat')
    string = string[:stop-1]
    string0 =  re.findall(r'[A-Z]{2,20}',string)
    if len(string0)!=0:
      chr = ''
      for x in string0:
        chr += ' '+x
      return chr

  start = remove_accents(string).lower().find('catgorie')
  string = string[start:start+100]
  stop=string.lower().find('avocat')
  string = string[:stop-1]
  string0 =  re.findall(r'[A-Z]{2,20}',string)
  if len(string0)!=0:
    chr = ''
    for x in string0:
      chr += ' '+x
    return chr


def find_date(string):
  string = string.lower()
  start = string.lower().find('date de')
  if start!=-1:
    try:
      string = string[start:start+50]
      string = re.findall(r'[a-z]+ [0-9]{1,2} [a-z]+ [0-9]{4,4}',string)[0]
      return string
    except:
      pass






def find_rccm(string):
  string = string.lower()

  start = string.find('rccm')
  if start!=-1:
    try:
      string = string[start:start+100].replace(' ','') 
      string = re.findall(r'[a-z]*[a-z]*[0-9]{1,4}[a-z]{1,1}[0-9]{1,4}', remove_punctuations(string))
      string0 =  string[0].replace('rccm','') 
      stop = string0.find('ci')
      return string0[stop:]
    except:
      pass
  try:
    return re.findall(r'[a-z]*[a-z]*[0-9]{1,4}[a-z]{1,1}[0-9]{1,4}', remove_punctuations(string))
  except:
    pass


def remove_punctuations2(string):
  for pct in punctuation:
    string = string.replace(pct,' ')
    string = re.sub('\s\s+',' ',string)
  return string

def find_miss_rccm(string):
  string = string.encode('ascii', 'ignore').decode('ascii')
  string =  string.lower()
  string0 = re.findall(r'[a-z]* [a-z]* [a-z]*[0-9]{1,4} [a-z]{1,1} [0-9]{1,4}', remove_punctuations2(string))
  if len(string0)>0:
      return string0[0]
  string1 = re.findall(r'[a-z]*[a-z]*[0-9]{1,4}[a-z]{1,1} [0-9]{1,6}', remove_punctuations2(string))
  if len(string1)>0:
        return string1[0]

def find_missing_rccm(string):
  fields_list = [x for x in re.split('\n[^\w]*', string.split('\n\n\n')[-1]) if x not in [' ',''] and len(x)>2]
  for field in fields_list:
    field = remove_accents(field.lower())
    start = (remove_accents(field.lower())).find(remove_accents('rccm'.lower()))
    if start!=-1:
      return field[start+4:]

#BP
def find_bp(string):
  string = string.lower()
  start = remove_accents(string).find('siege')
  if start!=-1:
    matches = ['[0-9]{1,4} bp [0-9]{1,4} [a-z]* [0-9]{1,2}',r'[0-9]{1,4} bp [0-9]{1,4}',r'[0-9]{1,2} bp [0-9]{1,4} [a-z]* [0-9]{1,4}',r'bp [0-9]{1,4} [a-z]* [0-9]{1,4}',r'bp [0-9]{1,4} [a-z]* [0-9]{1,4}',r'[a-z]* bp [0-9]{1,4}',r'[a-z]* bp [0-9]{1,4}']

    for match in matches:
      # string = string[start:]#start+100]
      string0 = re.findall(match, string)
      if len(string0)!=0:
        chrt = ''
        for x in string0:
          chrt += x + "/"
        return chrt
  else:
    matches = [r'bp [a-z]+ [0-9]+',r'\[a-z]{2,15}',r'[0-9]{1,4} bp [0-9]{1,4} [a-z]* [0-9]{1,2}',r'[0-9]{1,4} bp [0-9]{1,4}',r'[0-9]{1,2} bp [0-9]{1,4} [a-z]* [0-9]{1,4}',r'bp [0-9]{1,4} [a-z]* [0-9]{1,4}',r'bp [0-9]{1,4} [a-z]* [0-9]{1,4}',r'[a-z]* bp [0-9]{1,4}',r'[a-z]* bp [0-9]{1,4}']

    for match in matches:
      # string = string[start:]#start+100]
      string0 = re.findall(match, string)
      if len(string0)!=0:
        chrt = ''
        for x in string0:
          chrt += x + "|"
        return chrt

# string = df_merged.loc[84084,'page-content']
def find_miss_bp(string):
  string = string.lower()
  start = string.find('bp')
  if start!=-1:
    string = string[start:]
    stop = string.find('\n')
    if stop!=-1:
      string = string[:stop]
      return re.sub('\s\s+','',remove_punctuations(string).replace('bp',''))#.find('\n')
        
def find_duree(string):
  start = (remove_accents(string).lower()).find('duree')
  if start!=-1:
      string0 = string[start+8:start+12]
      string0 = re.findall(r'[0-9]{2,2}',string0)
      if len(string0)==1:
        return string0[0]
      string1 = string[start:start+12]
      string1 = re.findall(r'[0-9]{2,2}',string1)
      return string1
      
    

      
def find_name(string):
  start = remove_accents(string).lower().find('societe')
  string = string[start+8:start+100]
  stop=remove_accents(string).lower().find('categorie')
  string = string[:stop-1]
  string0 =  re.findall(r'[A-Z]{2,20}',string)
  if len(string0)!=0:
    chr = ''
    for x in string0:
      chr += ' '+x
    return chr
  else:
    string0 =  re.findall(r'[A-Z]{1,20}',string)
    chr = ''
    for x in string0:
      chr += ' '+x
    return chr

def find_siege(string):
  string = remove_accents(string).lower() 
  start = string.find('siege')
  string = string[start:]
  stop = string.find('\n')
  string = string[:stop]
  string = string.replace('siege','')
  string = string.replace('social','')
  string = string.replace(':','')
  string = re.sub('\s\s+','',string)
  return string  



def search_fileds(df_merged):

  df_merged['content'] = df_merged['page-content'].apply(lambda x: ' '.join(x.split('\n')))

  df_merged['content'] = df_merged.content.apply(lambda string: decode_encode(string) )

  #replace multiple space by one
  df_merged['content'] = df_merged['content'].apply( lambda string: re.sub("\s\s+" , " ", string) )

  # df_merged['email'] = 
  df_merged['email'] = df_merged['content'].apply( lambda string: find_email( string) )

  # df_merged['email'] = 
  df_merged['capital'] = df_merged['content'].apply( lambda string: find_capital(string) )

  df_merged['tel'] = df_merged['content'].apply(lambda string: find_tel(string))

  df_merged['fax'] = df_merged['content'].apply(lambda string: find_fax(string))

  df_merged['notaire'] = df_merged['content'].apply(lambda string: find_notaire(string))

  df_merged['notaire'] = df_merged['content'].apply(lambda string: find_notaire(string))

  df_merged['categorie'] = df_merged['content'].apply(lambda string: find_cat(string))

  df_merged['nom'] = df_merged['content'].apply(lambda string: find_name(string))

  df_merged['date'] = df_merged['content'].apply(lambda string: find_date(string))

  df_merged['rccm'] = df_merged['content'].apply(lambda string: find_rccm(string))

  df_merged.loc[df_merged['rccm'].isna(),'rccm'] = df_merged.loc[df_merged['rccm'].isna(),'content'].apply(lambda x:find_miss_rccm(x))

  df_merged.loc[df_merged['rccm'].isna(),'rccm'] = df_merged.loc[df_merged['rccm'].isna(),'page-content'].apply(lambda x:find_missing_rccm(x))

  df_merged['bp'] = df_merged['content'].apply(lambda string: find_bp(string))

  df_merged.loc[df_merged['bp'].isna(),'bp'] = df_merged.loc[df_merged['bp'].isna(),'page-content'].apply(lambda x:find_miss_bp(x))

  df_merged['duree'] = df_merged['content'].apply(lambda string: find_duree(string))

  df_merged.loc[[i for i,x in enumerate(df_merged['content']) if x.lower().find('abidjan')!=-1],'ville']='Abidjan'

  df_merged['siege'] = df_merged['page-content'].apply(lambda x: find_siege(x))



  return df_merged


# ## Set up  dirs and csts, and local language

# In[23]:


# id = 94400
if not os.path.exists('history.txt'):
    with open('history.txt','w') as f:
        f.write(str(id))
        f.close()
else:
        id = int(open('history.txt','r').read())
# id


# In[24]:


dir_result = os.path.abspath('./{}'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
#'results'
path_to_history = os.path.join(dir_result, 'history.csv')
create_dir(dir_result)
#set for french date
locale.setlocale(locale.LC_ALL)


# ## Start search lin by ID
# 
# * Search lins and save into a variable called `df_link`
# 
# * Start Id set 94100.

# In[25]:


df_links = search_links_id(id)#(94100)
df_links.head()


# In[26]:


print('Number of links avalaible is:',df_links.shape[0])


# ## Start the crawler to grab content for each links found

# In[27]:


df_merged = crawl_data(df_links)
df_merged.head()#will return the 5 rows of the df


# ### Search fileds and return df

# In[28]:



df_merged = search_fileds(df_merged)
df_merged.head()


# ## Display missing fields in df
# 

# In[29]:


df_merged.isna().sum()


# #Update  your dataframe or save

# In[35]:


#we load the data into df_merged1 and update it
path_to_df_1 = '/content/annonceDetail1.csv'#path_to_df_1 = 'Enter the path of your existing df'
if os.path.exists(path_to_df_1):
    df_merged1 = pd.read_csv(path_to_df_1, encoding='utf-16le' )
    df_merged_complete = pd.concat([df_merged1, df_merged],axis = 0)
    df_merged_complete = df_merged_complete.reset_index()
else:
    df_merged_complete = df_merged.copy()


# In[ ]:


# type(stringlist)==list


# * Transform list into values

# In[36]:


def transform_list(stringlist):

  if type(stringlist)==list:
    chr = ''
    for x in stringlist:
      chr += x +'|'
    return chr
  return stringlist

for col in df_merged_complete.columns.tolist():
  df_merged_complete[col] = df_merged_complete[col].apply(lambda x:transform_list(x))


# _*Pay attention to the path where you'll save the updated file*_

# In[40]:


df_merged_complete = df_merged_complete.drop_duplicates()
path_to_save_df = 'annonceDetail_udate.csv'#path_to_save_df = 'write gere the absolute path of your new df'
df_merged_complete.to_csv(path_to_save_df, header=True, encoding='utf-16le', index =False ,mode='a')
df_merged_complete.to_csv(os.path.join(dir_result,path_to_save_df), header=True, encoding='utf-16le', index =False ,mode='a')

# In[ ]:
with open('history.txt','w') as f:
    f.write(str(int(df_links.max()[0].split('/')[-1].split('.')[0])))
    f.close()

