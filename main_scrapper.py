#SCRAPPIING THE TOP REPOSITORIES FOR TOPICS ON GITHUB
# TODO
# ---INTRODUCTION ABOUT WEBB SCRAPING
# ---INTRODUCTION ABOUT GITHUB AND THE PROBLEM STATEMENT
# ---MENTION THE TOOLS YOU'ARE USUNG (PYHTON,REQUESTS,BEAUTIFUL SOUP,PANDAS)

#HERE ARE THE STEPS WE ARE GOING TO FOLLOW
#  --we are going to scrap : https://github.com/topics
#  --we'll get a list of topics.For each topic we'll get topic title,topic page url and topic description
#  --for each topic we'll get the top 25 repos in the topic from the topic page
#  --for each repo we'll grab the repo name , username , stars , and repo url
#  --for each topic we'll create a csv filr in the following format : 
#     repo name , username, stars,repo url
#     three.js,mrdoob,69700,https://github.com/topics/3d


#STEP 1 : Scrape the list of topics from Github
# ---1--use requests to download the page
# ---2--use bs4 to parse and extract information
# ---3--convet to Pandas Dataframe

import requests
from bs4 import BeautifulSoup
import pandas as pd 
import os

def get_topics_page():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception ('failed to load page{}'.format(topics_url))
    doc = BeautifulSoup(response.text,'html.parser')
    return doc

doc = get_topics_page()

# Lets create some helper functions to parse information from the page .

def get_topic_titles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p',{'class':selection_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

titles = get_topic_titles(doc)    
#get_topic_titles is used to get the list of titles
# similarly we have written functions for descriptions and urls of topics below

#for topic Descriptions :
def get_topic_decs(doc):
    desc_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p',{'class':desc_selector})   
    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    return topic_descs

#topic Urls :
def get_topic_urls(doc):
    topic_link_tags = doc.find_all('a',{'class':'no-underline flex-grow-0'})
    topic0_url = "https://github.com"+topic_link_tags[0]['href']
    topic_urls = []
    base_url = "https://github.com"
    for tag in  topic_link_tags:
        topic_urls.append(base_url+ tag['href'])
    return topic_urls

#Lets put all together in single function
def scrape_topics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception ('failed to load page{}'.format(topics_url))
    doc = BeautifulSoup(response.text,'html.parser')
    topics_dict = {
        'title': get_topic_titles(doc),
        'description':get_topic_decs(doc),
        'url':get_topic_urls(doc)
    }
    topics_list_df = pd.DataFrame(topics_dict)
    return topics_list_df
 

# GET THE TOP REPOS FROM A TOPIC PAGE  

def get_topic_page(topic_url):
    #download the page 
    response = requests.get(topic_url)
    #check Successsful Response
    if response.status_code != 200:
        raise Exception ('failed to load page{}'.format(topic_url))
    #parse using beautifulSoup
    topic_doc = BeautifulSoup(response.text,'html.parser')
    
    return topic_doc

doc = get_topic_page('https://github.com/topics/3d')

#lets get all H3 Tags:

#Get the stars count 
def parse_star_count(stars_str):
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1])*1000)
    return int(stars_str)

def get_repo_info(h3_tag,star_tag):
    #returns all the required info about repository
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    base_url = "https://github.com"
    repo_url = base_url + a_tags[1]['href']
    stars = parse_star_count(star_tag.text.strip())
    return username,repo_name,stars,repo_url

def get_topic_repos(topic_doc):
    
    #get the h3 tags containing repo title, repo url and username  
    h3_selection_class = "f3 color-fg-muted text-normal lh-condensed"
    repo_tags = topic_doc.find_all('h3',{'class':h3_selection_class})
    # 3get the star tags
    star_tags = topic_doc.find_all('span',{'class':'Counter js-social-count'})
    #get repo info 
    topic_repo_dict ={
        'username':[],
        'repo_name':[],
        'stars':[],
        'repo_url':[]
    }
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i],star_tags[i])
        topic_repo_dict['username'].append(repo_info[0])
        topic_repo_dict['repo_name'].append(repo_info[1])
        topic_repo_dict['stars'].append(repo_info[2])
        topic_repo_dict['repo_url'].append(repo_info[3])
    
    
    topic_repos_df = pd.DataFrame(topic_repo_dict)
    # topic_repos_df.to_csv('repos_info.csv')
    # topic_repos_df.to_excel('repos_info.xlsx')
    return topic_repos_df

def scrape_topic(topic_url,path):
    
    if os.path.exists(path):
        print("The file{} already exists.Skipping...".format(path))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(path ,index=None)
    
    
#PUTTING IT ALL TOGETHER
# --We have a function to get tha list of topics
# --we have a function to create a CSV file for scrapped reposfrom a topics page
# --lets create a function to put them together


def scrape_topic_repos():
    print('Scraping list of topics')
    topics_df= scrape_topics()
    os.makedirs('data',exist_ok=True)
    for index,row in topics_df.iterrows():
        print('scraping top repositories for "{}" '.format(row['title']))
        scrape_topic(row['url'],'data/{}.csv'.format(row['title']))
        
#lets run it to scrape the top repos for all the topics on the first page of 
#   https://github.com/topics

scrape_topic_repos()