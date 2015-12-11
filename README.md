# pycast

Welcome to pyCast, a simple Python script to generate XML files for serving podcasts.

To generate files:

./pyCast.py -d ~/Public/Podcast -w http://172.31.2.250/Podcast

This will search all sub-directories under ~/Public/Podcast, and generate an XMl file named after each directory found.

The base URL for the files will be http://172.31.2.250/Podcast.  In this instance, the directory ~/Public was being served by Python ( sudo python -m SimpleHTTPServer 80 )

Testing has done on 10.10 / 10.11 using the pre-installed Python