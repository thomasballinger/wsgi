"""Utility functions for the Kenya site framework

Includes functionality for rendering templates,
serving static files, and storing data to
"psuedo databases," implemented as csv files

Template Language:
templates replace occurrences of '+word+' with the passed in
value of keyword argument word.


Rules of the Kenya framework:

* All psuedo_db csv files are stored in a folder called 'database'
* All templates are stored in a folder called 'temp'
* All static files to be served are placed in 'static'
"""

import re
import os
import csv
import urlparse

fourohfour = '<html><body>Cannot find that file<body><html>'

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

def render_static_file(name):
    """renders either a static file or an error page if file not found"""
    filename = os.path.join('static',name)
    if not os.path.exists(filename):
        return fourohfour
    with open(filename, 'r') as f:
        read_data = f.read()
    return read_data

def get_post_qs(environ):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size) #obtain form input

    d = urlparse.parse_qs(request_body)
    return d

def get_db_filename(csv_name):
    filename = os.path.join('database', csv_name)
    if not filename[-4:] == '.csv':
        filename += '.csv'
    return filename

def save_to_psuedo_db(row_data, csv_name):
    with open(get_db_filename(csv_name), 'ab') as f:
        writer = csv.writer(f)
        entry_id = get_smallest_unused_id(csv_name)
        print 'storing with id:', entry_id
        data = [entry_id] + list(row_data)
        writer.writerow(data)
    return True

def get_smallest_unused_id(csv_name):
    """TERRIBLE technique for getting a unique id"""
    rows = load_from_psuedo_db(csv_name, all_rows=True)
    if rows:
        return max([int(row[0]) for row in rows]) + 1
    else:
        return 1

def load_from_psuedo_db(csv_name, row_id=None, all_rows=False):
    if (all_rows and row_id) or (row_id is None and all_rows is False):
        raise ValueError("specify either all or an row_id")
    filename = get_db_filename(csv_name)
    if not os.path.exists(filename):
        return []

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        if row_id is not None:
            for row in reader:
                if row[0] == str(row_id): #first element/item in each row is the id
                    return row
            else:
                raise ValueError("Item '"+str(row_id)+"' not found in db")
        else:
            return list(reader)


