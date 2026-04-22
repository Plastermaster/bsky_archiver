#meow :3

#todo: figure out a way to load further posts using the "cursor" response thingie and have it stop once it comes across a post it already found archived, or something idk..

import requests
import os
import re

url_getlist = 'https://bsky.social/xrpc/com.atproto.repo.listRecords'
url_getposts = 'https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts'

def does_file_exist(path):
    return os.path.isfile(path)

def get_liked_posts(handle):

    params_getlist = dict( #prep the parameters
        repo='',
        collection='app.bsky.feed.like',
        limit=10,
        cursor=''
    )

    params_getlist["repo"] = handle #add bsky handle to parameters

    liked_posts = requests.get(url=url_getlist, params=params_getlist) #get list of liked posts
    liked_posts_response = liked_posts.json() #parse that

    uris = []

    for x in liked_posts_response["records"]:
        uris.append(str(x["value"]["subject"]["uri"]))

    return uris

def get_image_urls(urls):

    params_getposts = {'uris': []}
    
    for x in urls:
        params_getposts['uris'].append(x)

    img = requests.get(url=url_getposts, params=params_getposts)
    img_response = img.json()

    img_urls = dict(
        type=[],
        full=[],
        thumb=[],
        mimeType=[]
    )

    for x in img_response["posts"]:
        img_urls["type"] = (x["record"]["embed"]["$type"])
        if img_urls["type"]=='app.bsky.embed.images':
            img_urls["mimeType"].extend([image["image"]["mimeType"] for image in x["record"]["embed"]["images"]])
            img_urls["full"].extend([image["fullsize"] for image in x["embed"]["images"]])
            img_urls["thumb"].extend([image["thumb"] for image in x["embed"]["images"]])
            print("-- get_image_urls --\n",
                  "$type: ",img_urls["type"],"\n",
                  "$fullsize: ",img_urls["full"],"\n",
                  "$thumbnail: ",img_urls["thumb"],"\n")
        else:
            print("oh noes, no \"app.bsky.embed.images\" lol")
    return img_urls

def save_images(urls,path):
    #it checks individually if a file exists
    #idk if this is smart or not, doesn't hurt to check though

    for x in urls["full"]: #at this point this function assumes the URLs are fine, maybe a bad idea lol
        #first, check if the file exists already, gotta prep the final path first
        path_file = path + re.search("(\\w*)\\Z",x).group() + ".jpg" #wow this sucks
        if does_file_exist(path_file):
            print("Image already exists!: ",path_file)
        else:

            temp_img = requests.get(url=x) #saves full version of image first
            print("downloaded image, now to save....")
            with open (path_file, 'wb') as file:
                file.write(temp_img.content)
                print("[Full] Image saved: ",path_file)

    for x in urls["thumb"]: 
        path_file = path + re.search("(\\w*)\\Z",x).group() + "_thumb.jpg" 
        if does_file_exist(path_file):
            print("Image already exists!: ",path_file)
        else:
            temp_img = requests.get(url=x) 
            with open (path_file, 'wb') as file:
                file.write(temp_img.content)
                print("[Thumb] Image saved: ",path_file)


    
