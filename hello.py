import os
import bsky_api

path = './images/'
handle = "plaster.gay"

posts = bsky_api.get_liked_posts(handle)
images = bsky_api.get_image_urls(posts)

#print("should be a massive list of stuff: ",images)

os.makedirs(path, exist_ok = True) #is this okay????
bsky_api.save_images(images,path)