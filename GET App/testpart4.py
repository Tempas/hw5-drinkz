
import sys
import socket

def main(args):

    address = args[1]
    port = args[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((address, int(port)))

    s.send("GET / HTTP/1.0\r\n\r\n")
    text = ""
    while 1:
        buf = s.recv(1000)
        if not buf:
            break
        text+=buf

    s.close()

    assert text.find("<a href='somethingelse'>something else</a>, or") != -1, text
    print "GET request success"

def form(args):

    address = args[1]
    port = args[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((address, int(port)))

    s.send("GET /recv?add=4&to=6 HTTP/1.0\r\n\r\n")
    text = ""
    while 1:
        buf = s.recv(1000)
        if not buf:
            break
        text+=buf

    s.close()

    assert text.find("10") != -1, text
    print "GET form submit success"

def image(args):

    address = args[1]
    port = args[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((address, int(port)))

    s.send("GET /helmet HTTP/1.0\r\n\r\n")
    fp = s.makefile("request_image")
    for line in fp:
        if "Content-Length: " in line:
           length = int(line.strip("Content-Length: "))
           break
        
    fp2 = open("Spartan-helmet-Black-150-pxls.gif","r")
    text2 = ""
    for line in fp2:
        text2+=line
    
    s.close()
    assert length == len(text2),length
    print "GET image success"
   
if __name__ == '__main__':
    form(sys.argv)
    image(sys.argv)
    main(sys.argv)
        
        
    
       
   
