import http.server
import urllib.parse
import urllib.request
import ssl

    # Crea contesto https
ssl._create_default_https_context = ssl._create_unverified_context

       # Richiesta di accesso alle credenziali di spotify.com
def get_authorize_url():
    client_id = "0b0257f3ab104ffc89c6f4529161b19c"
    response_type = "code"
    redirect_uri = urllib.parse.quote("http://127.0.0.1:3000/callback", safe='')
    scope = urllib.parse.quote("user-follow-read", safe='')
    url = ("https://accounts.spotify.com/authorize/?client_id="+client_id+
            "&response_type="+response_type+
            "&redirect_uri="+redirect_uri+
            "&scope="+scope)
    return url

class myHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/login"):
            url = get_authorize_url()

            self.send_response(301, 'Redirecting')
            self.send_header('Location', url)
            self.end_headers();
        elif (self.path[0:9] == "/callback"):
            query = self.path[9:]
            code = query[6:]
            print(code)
            
            self.send_response(200, 'OK')
            self.end_headers()
            message = "Accesso effettuato con successo\n"+"Codice ricevuto:"+code+"\n"
            self.wfile.write(message.encode())
        else:
            self.send_response(200,"OK")
            self.send_header('Content-type','text/html;charset=utf-8')
            self.end_headers()

            file = open("error_url.html",'r')
            message = file.read()
            self.wfile.write(message.encode())

server_address = ("127.0.0.1", 3000)
webserver = http.server.HTTPServer(server_address, myHttpRequestHandler)
print("Server avviato su "+str(server_address)+". \nPer terminare l'esecuzione premere CTRL+C.")

try:
    webserver.serve_forever()
except KeyboardInterrupt:
    print("\nServer in chiusura.. Arrivederci !")
    webserver.shutdown()
