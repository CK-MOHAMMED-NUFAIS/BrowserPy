import socket
import ssl
class Url:
    def __init__(self,url):
        #spilt http scheme and url then assert and check if scheme is http
        scheme,url   = url.split("://")
        self.scheme = scheme
        assert scheme in ["http","https"], f"Not {scheme}/0 standard \n {scheme} not Supported"

        #splittting path and hostname based on "/" . and check if "/" exist in it if not ,add 
        if "/" not in url:
            url += "/"
        self.host ,self.path = url.split("/",1)
        if scheme == "http":
            self.port = 80
        elif scheme == "https":
            # https connects use port 443
            self.port = 443
        
        #custom port support
        if ":" in self.host:
            self.host,port = self.host.split(":",1)
            self.port = int(port)
            
        print(self.host,self.path,self.port)

        
    def request(self,raw = False):
        soc = socket.socket(family = socket.AF_INET,type=socket.SOCK_STREAM,proto=socket.IPPROTO_TCP,)
        print("Trying to connect to hostname:\n")
        soc.connect((self.host,self.port))
   
    # check if the scheme is https . if it then connection will encrypted
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            soc = ctx.wrap_socket(soc,server_hostname=self.host)

        #simple to add headers using dict
        header = {
            "Host":self.host,
            "Connection":"close",
            "User-Agent":'firefox',
        }

        request_line = "GET /{} HTTP/1.1\r\n".format(self.path)
        req = f"{request_line}"
        for header , value in  header.items():
            req+="{}:{}\r\n".format(header,value)
        req +="\r\n\r\n"
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
        # check if raw parameter is true then call simple terminal printing function
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


if __name__ == "__main__":
    import sys
    system = sys.argv
    if len(system) > 1:
        url = Url(system[1])
        # url = Url()
        headers , body = url.request(True)
    else:
        print("\nplease input the url carefully and try again\n")
