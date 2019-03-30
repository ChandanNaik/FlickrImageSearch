# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 21:49:28 2019

@author: divya
"""

import flickrapi
import pandas as pd
import sys
################################################
## https://towardsdatascience.com/how-to-use-flickr-api-to-collect-data-for-deep-learning-experiments-209b55a09628
## Get flickr Hot list tags for a given duration
## Write code for incremental updates

###################################################


def get_urls(image_tag,MAX_COUNT):
    key='72867a4388924cd9840ae813f23a70cf'
    secret='49021d0404efb5c3'
    flickr = flickrapi.FlickrAPI(key,secret)
    photos = flickr.walk(text=image_tag,
                            tag_mode='all',
                            tags=image_tag,
                            extras='url_o',
                            per_page=50,
                            sort='relevance')
    count=0
    urls=[]
    for photo in photos:
        if count< MAX_COUNT:
            count=count+1
            print("Fetching url for image number {}".format(count))
            try:
                url=photo.get('url_o')
                urls.append(url)
            except:
                print("Url for image number {} could not be fetched".format(count))
        else:
            print("Done fetching urls, fetched {} urls out of {}".format(len(urls),MAX_COUNT))
            break
    urls=pd.Series(urls)
    print("Writing out the urls in the current directory")
    urls.to_csv(image_tag+"_urls.csv")
    print("Done!!!")
    
    
    
def main():
    tag=sys.argv[1]
    MAX_COUNT=int(sys.argv[2])
    get_urls(tag,MAX_COUNT)
if __name__=='__main__':
main()




## run
## > python get_images.py file_containing_url_csv
import csv
import requests
import os
import sys
import time
def put_images(FILE_NAME):
    urls=[]
    with open(FILE_NAME,newline="") as csvfile:
        doc=csv.reader(csvfile,delimiter=",")
        for row in doc:
            if row[1].startswith("https"):
                urls.append(row[1])
    if not os.path.isdir(os.path.join(os.getcwd(),FILE_NAME.split("_")[0])):
        os.mkdir(FILE_NAME.split("_")[0])
    t0=time.time()
    for url in enumerate(urls):
        print("Starting download {} of ".format(url[0]+1),len(urls))
        try:
            resp=requests.get(url[1],stream=True)
            path_to_write=os.path.join(os.getcwd(),FILE_NAME.split("_")[0],url[1].split("/")[-1])
            outfile=open(path_to_write,'wb')
            outfile.write(resp.content)
            outfile.close()
            print("Done downloading {} of {}".format(url[0]+1,len(urls)))
        except:
            print("Failed to download url number {}".format(url[0]))
    t1=time.time()
    print("Done with download, job took {} seconds".format(t1-t0))
def main():
    FILE_NAME=sys.argv[1]
    put_images(FILE_NAME)

if __name__=='__main__':
    main()
