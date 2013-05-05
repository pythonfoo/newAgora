import urllib2

class pageLoader(object):
	def __init__(self):
		#TODO:
		# configs for cache folder, reloat-duration, more foo
		pass
		
	def isLinkOutdated(self, link):
		#TODO: check if the given url is already loaded or outdated
		return True
		
	def getHashFromLink(self, link):
		pass
	
	def getContent(self, link):
		content = ''
		
		try:
			request = urllib2.Request(link)
			request.add_header('User-agent',  'newagora')
			response = urllib2.urlopen(request)
			content = response.read()
		except Exception, ex:
			print("Error 4 getContent: " + link + '|' + str(ex))
			
		return content
	
	def getContentCached(self, link):
		#TODO: caching should work over the link-hash (somehow)
		#hashLink = self.getHashFromLink(link)
		pass
	
	def putContentToCache(self, link, content):
		#hashLink = self.getHashFromLink(link)
		pass
	
	def getPlainContent(self, link):
		content = ''
		
		if self.isLinkOutdated(link):
			content = self.getContent(link)
		else:
			content = getContentCached(link)
			
		return content
