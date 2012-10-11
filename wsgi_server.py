import view
#execfile('configuration.py')

def blog_wsgi_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/html')] # HTTP Headers
    start_response(status, headers)

    blog_post = view.View()

    path = environ['PATH_INFO']
    #output = getOutput(URL_routing[path])
    
    if path == '/create':
    	output = blog_post.new_post(environ)
    elif path == '/display_post_links':
        #method = URL_routing[path]
        #output = blog_post.method
    	output = blog_post.display_post_links()
    elif path.find('/id/')!=-1:
        parsed_path = path.split("/")

        try:
            post_id = int(parsed_path[2]) #obtain ID for clicked post, should be second item of path. if no error is thrown then it can be converted to an int and is therefore a string.
            output = blog_post.display_post(str(post_id))
        except(ValueError):
            output = '404 Error'
    elif path == '/':
    	output = blog_post.render_main(environ)
    else:
    	output = '404 Error'

    return output


from wsgiref.simple_server import make_server
httpd = make_server('', 8080, blog_wsgi_app)
print "Serving on port 8080..."

# Serve until process is killed
httpd.serve_forever()
