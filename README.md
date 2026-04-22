# bsky archiver

requires [Requests](https://docs.python-requests.org/en/latest/index.html)

what it currently does:
- downloads the last 10 liked posts
- saves the images (full res and thumbnail), it skips posts with videos and external embeds for now
- stores those to the folder "./images"

idea of this project is to automate archiving liked posts locally.

---

very wip, but there's some things I'd like to do too:

- have it stay up to date on newly liked posts
- create a website to look at archived posts
- implement sqlite for storing data on posts
- wrap it all up so it can be easily installed via docker

