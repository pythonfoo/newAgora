#!/usr/bin/env python

if __name__ == "__main__":
	import configLoader

	print( 'configs loaded: ' + str(len(configLoader.conf.configDic)))
	print( configLoader.conf.getValue("maxLines", 23) )
	print( configLoader.conf.getValue("nf", "nf") )

	from modules.pageLoader import pageLoader

	pg = pageLoader()
	print pg.getPlainContent('http://blog.fefe.de')
