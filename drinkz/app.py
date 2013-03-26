#! /usr/bin/env python
from wsgiref.simple_server import make_server
from db import save_db, load_db
import sys
import urlparse
import simplejson
import db
import recipes
import os.path
import fileinput,sys

dispatch = {
    '/' : 'index',
    '/recipesList' : 'recipesList',
    '/inventoryList' : 'inventoryList',
    '/liqourTypes' : 'liqourTypes',
    '/convertToML' : 'formConvertToML',
    '/recv' : 'recv',
    '/recvAmount' : 'recvAmount',
    '/rpc' : 'dispatch_rpc'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):
        
        path = environ['PATH_INFO']
        
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = """\
Visit:
<a href='recipesList'>Recipes</a>,
<a href='inventoryList'>Inventory</a>,
<a href='liqourTypes'>Liqour Types</a>,
<a href='convertToML'>Convert to ml</a>, or
<a href='form'>a form...</a>
<p>
<img src='/helmet'>
"""
        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipesList(self, environ, start_response):
        data = recipesList()
        start_response('200 OK', list(html_headers))
        return [data]
    
    def inventoryList(self, environ, start_response):
        data = inventoryList()
        start_response('200 OK', list(html_headers))
        return [data]

    def liqourTypes(self, environ, start_response):
        data = liqourTypesList()
        start_response('200 OK', list(html_headers))
        return [data]
    
    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
    
    def formConvertToML(self, environ, start_response):
        data = convertToML()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s. <p><a href='./'>return to index</a>" % (firstname, lastname)

        start_response('200 OK', list(html_headers))
        return [data]
    
    def recvAmount(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['amount'][0]
        print amount
        amount = str(db.convert_to_ml(amount))
        

        content_type = 'text/html'
        data = "Converted Amount %s ml<p><a href='./'>return to index</a>" % (amount)

        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):

        return int(a) + int(b)

    
def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
<p><a href='/'>Home</a>
"""

def convertToML():
    return """
<form action='recvAmount'>
Enter amount(i.e. 11 gallon or 120 oz)<input type='text' name='amount' size'20'>
<input type='submit'>
</form>
<p><a href='/'>Home</a>
"""


def recipesList():
    recipeList = db.get_all_recipes()
    recipeStringHTML = "<ul>"
    for recipe in recipeList:
        if recipe.need_ingredients():
            val = "no"
        else:
           val = "yes"
        recipeStringHTML += ("<li>"+recipe._recipeName + " " + val +"<p>")
    recipeStringHTML += ("</ul>"+"<p><a href='/'>Home</a>")

    return recipeStringHTML

def inventoryList():
    inventoryStringHTML = "<ul>"
    for (m,l) in db.get_liquor_inventory():
        inventoryStringHTML+= ("<li>" + str(m)+ " " + str(l)+ " "  + str(db.get_liquor_amount(m,l))+" ml"+ "<p>")
    inventoryStringHTML += ("</ul>"+"<p><a href='/'>Home</a>")

    return inventoryStringHTML
    
def liqourTypesList():
    liqourTypeStringHTML = "<ul>"
    for (m,l) in db.get_liquor_inventory():
        liqourTypeStringHTML += ("<li>" + str(m)+ " " + str(l) + "<p>")
    liqourTypeStringHTML += ("</ul>"+"<p><a href='/'>Home</a>")

    return liqourTypeStringHTML

def setUpWebServer():
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
    
if __name__ == '__main__':
    args = sys.argv
    try:
        filename = args[1]
    except:
        filename = 'myTest'

    for line in fileinput.input(['../bin/'+filename], inplace=True):
        line = line.replace("drinkz.", "")
        sys.stdout.write(line)

    load_db('../bin/'+filename)
    setUpWebServer()



