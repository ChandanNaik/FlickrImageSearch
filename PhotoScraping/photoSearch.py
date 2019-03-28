import urllib.parse
import requests
import webbrowser

#Keywords input
searchKeywords = input('Enter search keywords: ')

#Construct URL
searchApi = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=<KEY GOES HERE>&format=json&nojsoncallback=1&'
searchUrl = searchApi+urllib.parse.urlencode({'text':searchKeywords})

#Get response , convert to JSON
searchResultJson = requests.get(searchUrl).json()
photosData = searchResultJson["photos"]["photo"]

#Print image IDs
count = 0
for photoData in photosData:
	print(photoData["id"])
	count+=1
	#Open every 20th image in webbrowser
	if count%20 == 0:
		imageUrl = 'https://farm'+str(photoData["farm"])+'.staticflickr.com/'+photoData["server"]+'/'+photoData["id"]+'_'+photoData["secret"]+'.jpg'
		webbrowser.open(imageUrl)
