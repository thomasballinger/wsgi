import json
from kenya import render, render_static_file, get_post_qs, save_to_psuedo_db, \
        load_from_psuedo_db

default_header = 'This is the default header.'
default_content = 'This is the content. Currently it\'s coming from the standard input.'
template_view = 'default_view.tpl'

def render_main(environ):
    return render_static_file('index.html')

def new_post(environ):
    """Stores POST data in db"""
    d = get_post_qs(environ)
    name = d.get('name')[0]
    body = d.get('body')[0]

    #TODO:traverse "d" for parsed input and append view_attributes
    view_attributes = [name, body]
    save_to_psuedo_db(view_attributes, 'blog_entries')
    response = "Post Saved!"
    return response

def display_post(post_id):
    #select id, name, content, template_view from database
    template_view = 'blog_post_view.tpl'
    _, db_title, db_content = load_from_psuedo_db('blog_entries', row_id=int(post_id))
    if not db_title: db_title = default_header
    if not db_content: db_content = default_content
    post = render(template_view, header=db_title, content=db_content)
    return post

def display_post_links():
    #select all of the posts within database and display them
    db = 'blog_entries'
    posts = load_from_psuedo_db(db, all_rows=True)
    print posts
    if len(posts) == 0:
        return "0" #no posts available
    response = json.dumps(posts)
    print 'resonse:', response

    return response

