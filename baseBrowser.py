import socket
class Url:
    def __init__(self,url):
        #spilt http scheme and url then assert and check if scheme is http
        scheme,url   = url.split("://")
        assert scheme == "http", f"Not http/0 standard \n {scheme} not Supported"

        #splittting path and hostname based on "/" . and check if "/" exist in it if not ,add 
        if "/" not in url:
            url += "/"
        self.host ,self.path = url.split("/",1)
        print(self.host,self.path)


        
    def request(self,raw = False):
        soc = socket.socket(family = socket.AF_INET,type=socket.SOCK_STREAM,proto=socket.IPPROTO_TCP,)
        print("Trying to connect to hostname:\n")
        soc.connect((self.host,80))
   
        request_line = "GET /{} HTTP/1.0\r\n".format(self.path)
        hostH= "Host:{}\r\n".format(self.host)

        req = "{}{}\r\n\r\n".format(request_line,hostH)
        soc.send(req.encode("utf8"))
#       this creates request like below
        # GET /index.html HTTP/1.0
        # Host:example.org

        #makefile hides the loop
        response = soc.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()

        version, status, explanation = statusline.split(" ", 2)

        assert status == "200", "{}: {}".format(status, explanation)

        headers = {}
        while True:
            line = response.readline()
            if line =="\r\n":break
            header ,value  = line.split(":",1)
            headers[header.lower()] = value.strip()

        assert "transfer-encoding" not in headers
        assert "content-encoding" not in headers

        self.body = response.read()
        soc.close()
        if raw == True:
            self.show()
        return headers, self.body
        
    def show(self):
        flag = False
        for i in self.body:
            if i == "<":
                flag = True
            elif i == ">":
                flag = False
            elif not flag:
                print(i,end="")

# url = Url("http://example.org/index.html")
if __name__ == "__main__":
    import sys
    system = sys.argv
    if len(system) > 1:
        url = Url(system[1])
        # url = Url()
        headers , body = url.request(True)
    else:
        print("\nplease input the url carefully and try again\n")