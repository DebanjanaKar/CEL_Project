
# coding: utf-8

# In[1]:

import os
from bs4 import BeautifulSoup


# In[8]:

path='/home/alapan/work_space/december_3rd/22_12/xml_folder/'
for filename  in os.listdir(path):
    fullPath = os.path.join(path, filename)
    if os.path.isfile(fullPath):
        infile= open(fullPath)
        contents=infile.read()
        soup=BeautifulSoup(contents,'xml')
        event_title=soup.TITLE.get_text()
        event_content=soup.ARTICLE.get_text()
        doc_id=soup.DOCID.get_text()
        time=soup.DATE.get_text()
    print(event_title)
    print(event_content)
    print(doc_id)
    print(time)


# In[ ]:



