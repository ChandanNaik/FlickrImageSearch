#////////////////////////////////////////////////
#Gets images from Flickr and dumps to S3 bucket//
#Author: thanika
#////////////////////////////////////////////////

import boto3
import flickrapi
import urllib.request

#Create S3 Bucket
s3_resource = boto3.resource('s3')
our_bucket = s3_resource.Bucket(name='flickrbigdatacu')

#Create Flickr object
key='72867a4388924cd9840ae813f23a70cf'
secret='49021d0404efb5c3'
flickr = flickrapi.FlickrAPI(key,secret, format='parsed-json')

#Get 20 most interesting photos for the day 
apiResult = flickr.interestingness.getList(per_page = '20')
photos = apiResult["photos"]["photo"]

#Dump one by one in S3 bucket
for photo in photos:

	imageURL = 'https://farm'+str(photo["farm"])+'.staticflickr.com/'+photo["server"]+'/'+photo["id"]+'_'+photo["secret"]+'.jpg'
	
	try:
		urllib.request.urlretrieve(imageURL, 'temporary.jpg')
		our_bucket.upload_file(Filename='temporary.jpg', Key=photo["id"]+'.jpg')
		print("SUCCESSfully dumped photo with ID: "+photo["id"])

	except:
		print("FAILED to dump photo with ID: "+photo["id"])

#our_bucket.download_file('testing.jpg','testing_download.jpg')