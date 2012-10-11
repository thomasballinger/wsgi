import csv
import string
import json
import urlparse

#TODO: create function for wrting and reading to a file

class View:
    header = 'This is the default header.'
    content = 'This is the content. Currently it\'s coming from the standard input.'
    template_view = 'default_view.tpl'
    db_counter = 1


    def render_main(self, environ):
        with open('index.html', 'r') as f:
            read_data = f.read()

        return read_data

    def new_post(self, environ):
        #TODO: this doesn't actually need the self keyword anymore since it's been removed from the class attribute list, right?
        print View.db_counter
        self.view_attributes = []

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size) #obtain form input

        d = urlparse.parse_qs(request_body)

        name = d.get('name')[0]
        body = d.get('body')[0]

        #grab counter value...essentially the poor man's version of a primary key in a database.
        #with open('database/db_counter.txt', 'r') as f:
         #   read_data = f.read()

            #db_counter = int(read_data)

        #TODO:traverse "d" for parsed input and append view_attributes
        self.view_attributes.append(View.db_counter)
        self.view_attributes.append(name)
        self.view_attributes.append(body)

        #write information to psuedo database
        with open('database/pseudo_database.csv', 'ab') as f:
            writer = csv.writer(f)
            writer.writerow(self.view_attributes)
        
        View.db_counter+=1
        print View.db_counter
        #with open('database/db_counter.txt', 'w') as f:
         #   f.write(str(db_counter))

        response = "Post Saved!"
        return response

    def render(self, template):

        template = 'tmp/' + template
        with open(template, 'r') as f:
            read_data = f.read()

        read_data = read_data.replace("'+header+'", self.header)
        read_data = read_data.replace("'+content+'", self.content)
        
        return read_data

    def display_post(self, post_id):
        #select id, name, content, template_view from database
        template = 'database/pseudo_database.csv'
       
        with open(template, 'rb') as f:
            reader = csv.reader(f)

            for row in reader:
                if row[0] == post_id: #first element/item in each row is the id
                    self.header = row[1]#retrieved header, basically name of post
                    self.content = row[2] #retrieved content


        self.template_view = 'blog_post_view.tpl' #retrieved template view #TODO: there should be some function to lookup what type of template should be used
        post = self.render(self.template_view) #this should pass in a default argument of 'default_view.tpl'

        return post

    def display_post_links(self):
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




        """def parse_user_input(self):

        with open('database/db_counter.txt', 'r') as f:
            read_data = f.read()
            f.closed
            db_counter = int(read_data)

        self.view_attributes.append(db_counter)
        self.view_attributes.append(raw_input("Enter post name:"))
        self.view_attributes.append(raw_input("Enter blog body:"))

        with open('database/pseudo_database.csv', 'ab') as f:
            writer = csv.writer(f)

            writer.writerow(self.view_attributes)
            f.closed
        
        db_counter+=1
        with open('database/db_counter.txt', 'w') as f:
            f.write(str(db_counter))
            f.closed"""

        
