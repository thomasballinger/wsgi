import posts
import kenya

route_dict = {
    '^/create$' : posts.new_post,
    '^/display_post_links$' : posts.display_post_links,
    '^/$' : lambda env: kenya.render_static_file('index.html'),
    '^.*/id/(.*)$' : posts.display_post,
    }

def fourohfour(env):
    return '404 error'

kenya_wsgi_app = kenya.Router(route_dict, fourohfour_function=fourohfour)

from wsgiref.simple_server import make_server
httpd = make_server('', 8080, kenya_wsgi_app)
print "Serving on port 8080..."

# Serve until process is killed
httpd.serve_forever()
