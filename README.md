Kenya web framework
-------------------

Includes functionality for rendering templates,
serving static files, and storing data to
"psuedo databases," implemented as csv files

Template Language:
templates replace occurrences of '+word+' with the passed in
value of keyword argument word.

* All psuedo_db csv files are stored in a folder called 'database'
* All templates are stored in a folder called 'temp'
* All static files to be served are placed in 'static'
