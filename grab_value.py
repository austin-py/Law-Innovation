import cgi
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')

with open ('data.txt', 'w') as f:
    f.write(searchterm)
