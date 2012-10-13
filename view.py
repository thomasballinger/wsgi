import csv
import json
import urlparse
import re

header = 'This is the default header.'
content = 'This is the content. Currently it\'s coming from the standard input.'
template_view = 'default_view.tpl'
db_counter = 1

def render_main(environ):
    with open('index.html', 'r') as f:
        read_data = f.read()

    return read_data

def new_post(environ):
    """Stores POST data in db"""
    global db_counter

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size) #obtain form input

    d = urlparse.parse_qs(request_body)

    name = d.get('name')[0]
    body = d.get('body')[0]


    #TODO:traverse "d" for parsed input and append view_attributes
    view_attributes = [db_counter, name, body]

    #write information to psuedo database
    with open('database/pseudo_database.csv', 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(view_attributes)

    db_counter+=1

    response = "Post Saved!"
    return response

def render(template, **kwargs):

    template = 'tmp/' + template
    with open(template, 'r') as f:
        read_data = f.read()

    # an attempt at preventing recursive replacement (still possible if one is creative)
    for textglob in kwargs.values():
        if re.search(r"'[+].*[+]'", textglob):
            raise ValueError("Template text cannot have '+anything+' in it")

    for key, replacement in kwargs.iteritems():
        read_data = re.sub("'[+]"+key+"[+]'", replacement, read_data)

    return read_data

def display_post(post_id):
    #select id, name, content, template_view from database
    template = 'database/pseudo_database.csv'

    with open(template, 'rb') as f:
        reader = csv.reader(f)

        for row in reader:
            if row[0] == post_id: #first element/item in each row is the id
                header = row[1]#retrieved header, basically name of post
                content = row[2] #retrieved content

    template_view = 'blog_post_view.tpl' #retrieved template view #TODO: there should be some function to lookup what type of template should be used
    post = render(template_view, header=header, content=content) #this should pass in a default argument of 'default_view.tpl'

    return post

def display_post_links():
    posts = []
    #select all of the posts within database and display them
    template = 'database/pseudo_database.csv'

    try:

        with open(template, 'rb') as f:
            reader = csv.reader(f)

            for row in reader:
                posts.append(row)

            response = json.dumps(posts)

    except(IOError):
        response = "0"#no posts available

    return response

