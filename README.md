# New Agora #

I remember in the early 90's there was a service on the net called agora.  
You wrote to agora@somewhere with a request command in the subject and at maximum 3 URLs in the body and as answer you got an email back for each URL with the requested web page inside. 

* **I think it is time to use that idea again (to circumvent censorship), but today we need a bit more:**
  1. end to end encryption!
  2. send pages not only in html, but also pdf and perhaps other formats like plain text,
  3. request rss feeds that way,
  4. lots of "New Agoras" to make blocking of the service harder,
  5. a ready-to-use newagora package in different package formats (deb, rpm, ...).

## How it could work ##

Send a request to an email address. If you use that address the first time, add your public key to the request.  
Get an encrypted answer with the website you want to see (html or pdf).  
For encrypting your own requests each email address sends out its public key on request.  
Additionally it should be possible even to request rss feeds, once an address has sent its own public key.

## What actually works ##

Write as subject one of these commands:

* **help**
  - sends the README.md back
* **request**
  - write the pages you wanna recieve in the mail body, LINE BY LINE
* **register**
  - not fully functional, in the 'near' future, you can create an account with it ;)

## How to Run ##

1. You will need some sort of mail account that supports POP3.
  - **WARNING**  
    New Agora will load, check and DELETE every single e-mail it will find on this account!
2. Change the **newagora.conf** according to your needs.
3. Make shure you are in the newAgora directory, then you can run it with:  

        python newagorad.py


## License ##

GPLv3

## CREDITS ##

* fork us at GitHub: https://github.com/pythonfoo/newAgora
* idea by Atari-Frosch: http://blog.atari-frosch.de/2011/07/22/new-agora/
* pirate pad for informations and discusions: http://piratenpad.de/hU3OW9nNjl
