import json
#import simplejson as json


 #def application(environ, start_response):
   # the environment variable CONTENT_LENGTH may be empty or missing
   try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
   except (ValueError):
      request_body_size = 0

   # When the method is POST the query string will be sent
   # in the HTTP request body which is passed by the WSGI server
   # in the file like wsgi.input environment variable.
   request_body = environ['wsgi.input'].read(request_body_size)
   #print request_body
   #return request_body

   result = {"name":"John"}#{'success':'true','message':'The Command Completed Successfully'};
   #result = {'key':'value'}#{"value": "New", "onclick": "CreateNewDoc()"}
   #myjson = json.load(sys.stdin)
   
   #print result
   #result = simplejson.JSONEncoderForHTML.encode({"foo": ["bar", "baz"]})
   #result = JSONEncoder().encode({"foo": ["bar", "baz"]})
   #print 'Content-Type: application/json\n\n'
   print json.dumps(result)

   #sys.exit("some msg")



   #d = parse_qs(request_body)
   #print d

   #name = d.get('name', [''])[0] # Returns the first age value.
   #body = d.get('hobbies', []) # Returns a list of hobbies.
   #grab all of the user input and then store in database. if all goes well with storing, alert(success)