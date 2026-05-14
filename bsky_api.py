#meow :3    #miaumiaumiau

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

    print(img_response["posts"])

    for x in img_response["posts"]:

        img_response_keys = list(x.keys()) #first gotta figure out if it contains the [record][embed][$type] keys, otherwise it will shatter itself

        if 'record'  in img_response_keys and 'embed' in img_response_keys: #this solves the issue of any post not conaining any embeds

            img_response_type = x["record"]["embed"].get("$type")

            if 'app.bsky.embed.images' in img_response_type or 'app.bsky.embed.recordWithMedia' in img_response_type: #too long aaaaaa

                img_response_keys_embed=list(x["record"]["embed"].keys())
                img_urls["type"] = (x["record"]["embed"]["$type"])

                #not the most optimal code but it works
                if 'images' in img_response_keys_embed:

                    img_urls["mimeType"].extend([image["image"]["mimeType"] for image in x["record"]["embed"]["images"]])
                    img_urls["full"].extend([image["fullsize"] for image in x["embed"]["images"]])
                    img_urls["thumb"].extend([image["thumb"] for image in x["embed"]["images"]])

                else:
                    img_response_keys_media=list(x["record"]["embed"]["media"].keys())

                    if 'images' in img_response_keys_media:

                        img_urls["mimeType"].extend([image["image"]["mimeType"] for image in x["record"]["embed"]["media"]["images"]])
                        img_urls["full"].extend([image["fullsize"] for image in x["embed"]["media"]["images"]])
                        img_urls["thumb"].extend([image["thumb"] for image in x["embed"]["media"]["images"]])

                    else:
                        print("oh noes, no \"app.bsky.embed.images\" or \"app.bsky.embed.recordWithMedia\" lol")
                        continue

            else:
                print("oh noes, no \"app.bsky.embed.images\" or \"app.bsky.embed.recordWithMedia\" lol")
                continue

            print("-- get_image_urls --\n",
                  "$type: ",img_urls["type"],"\n",
                  "$fullsize: ",img_urls["full"],"\n",
                  "$thumbnail: ",img_urls["thumb"],"\n")

        else:
            print("oh noes, no \"app.bsky.embed.images\" or \"app.bsky.embed.recordWithMedia\" lol")

    return img_urls

def save_images(urls,path,thumbnails):
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

    if thumbnails:

        for x in urls["thumb"]:
            path_file = path + re.search("(\\w*)\\Z",x).group() + "_thumb.jpg"
            if does_file_exist(path_file):
                print("Image already exists!: ",path_file)
            else:
                temp_img = requests.get(url=x)
                with open (path_file, 'wb') as file:
                    file.write(temp_img.content)
                    print("[Thumb] Image saved: ",path_file)


