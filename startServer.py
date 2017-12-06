import http.server
import http.client
import urllib.parse
import ssl
import base64
import json

    # Crea contesto ssl
ssl._create_default_https_context = ssl._create_unverified_context

    # Global variables used for OAuth 2.0 Spotify
client_id = "0b0257f3ab104ffc89c6f4529161b19c"
client_secret_key = "85644beebd884fadb72fd7f766ee9814"
scope = urllib.parse.quote("user-follow-read", safe='')
redirect_uri = "http://127.0.0.1:3000/callback"
authorization_code = ""

       # Ottengo url per accesso al proprio account spotify
def get_authorize_url():
    response_type = "code"
    url = ("https://accounts.spotify.com/authorize/?client_id="+client_id+
            "&response_type="+response_type+
            "&redirect_uri="+urllib.parse.quote(redirect_uri, safe = '')+
            "&scope="+scope)
    return url

    # Effettuo la richiesta per ottenere un token
def do_token_request(request_handler, code):
        # Ottengo header per effettuare la richiesta del token
    def getheaders_tokenrequest():
        def getauthorizationcode_tokenrequest():
            info = client_id+":"+client_secret_key
            base64code = base64.b64encode(info.encode())
            authorization_code = "Basic " + base64code.decode()
            return str(authorization_code)
        authorization_code = getauthorizationcode_tokenrequest()
        headers = { "Authorization":authorization_code,
                    "Content-type":"application/x-www-form-urlencoded" }
        return headers #urllib.parse.urlencode(headers)
    
        # Ottengo body per effettuare la richiesta del token
    def getbody_tokenrequest(code,grant_type):
        body = {"grant_type":grant_type,
                "code":code,
                "redirect_uri":redirect_uri}
        return urllib.parse.urlencode(body)    

        # retriving parameters for token_request
    body_parameters = getbody_tokenrequest(code, "authorization_code")
    headers = getheaders_tokenrequest()

        # token_request
    token_request = http.client.HTTPSConnection("accounts.spotify.com") 
    token_request.request("POST",
                          "/api/token",
                          body_parameters.encode(),
                          headers )
    response = token_request.getresponse()
    
    request_handler.send_response(response.status, response.reason)
    request_handler.end_headers()

    json_response = json.loads(response.read().decode())
    return json_response

    # Parse della risposta per ottenere il token
def parse_json_response_token(json_response):
    access_token = json_response["access_token"]
    token_type = json_response["token_type"]
    expires_in = json_response["expires_in"]
    scope = json_response["scope"]
    return (access_token, token_type, expires_in, scope)

    # Effettuo la richiesta per ottenere gli artisti seguiti
def do_followed_artists_query(access_token):
    path = "/v1/me/following?type=artist"
    followed_request = http.client.HTTPSConnection("api.spotify.com") 
    followed_request.request("GET",
                              path,
                              None,
                              {"Authorization":"Bearer "+access_token,
                               #"Content-type":"application/x-www-form-urlencoded",
                               "Connection":"keep-alive"})
    return followed_request.getresponse() 

def parse_json_response_artists(json_data):
    names = []
    for item in json_data["artists"]["items"]:
        names.append(item["name"])
    return names

    # Gestore richieste alle risorse del server localhost
class myHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == "/login"):
            url = get_authorize_url()

            self.send_response(301, 'Redirecting')
            self.send_header('Location', url)
            self.end_headers();

            # Pagina di redirezione dopo aver acconsentito l'utilizzo dei dati su spotify.com
        elif (self.path[0:9] == "/callback"):
            query = self.path[9:]
            code = query[6:]
            
            #self.send_response(200, 'OK')
            #self.end_headers()
            
            #file = open("callback.html", 'r')
            #message = "Accesso effettuato con successo\n"+"Codice ricevuto:"+code+"\n"
            #message = file.read()
            #self.wfile.write(message.encode())

                # do HTTP POST to get token
            json_response_token = do_token_request(self, code)
            (access_token, token_type, expires_in, scope) = parse_json_response_token(json_response_token)
            #self.wfile.write(access_token.encode())

            '''
                # GESTIRE IL REFRESH DEL TOKEN QUANDO SCADE IL TIMEOUT (SUCCESSIVAMENTE)
            '''
            
                # request for followed artists
            query_response = do_followed_artists_query(access_token)
            self.send_response(query_response.status, query_response.reason)
            body = query_response.read().decode()
            #self.wfile.write(("token expires in "+str(expires_in)).encode())
            #self.wfile.write(body.encode())
            json_data = json.loads(body)
            followed_artists = parse_json_response_artists(json_data)

            title = "<div align=center><h1>Lista degli artisti seguiti su spotify:</h1></div>"
            self.wfile.write(title.encode())
            for artist in followed_artists:
                format = "<div align=center><h4>"+artist+"</h4></div>"
                self.wfile.write(format.encode())
            
# Gestisco l'accesso alle risorse non menzionate precedentemente
        else:
            self.send_response(200,"OK")
            self.send_header('Content-type','text/html;charset=utf-8')
            self.end_headers()

            file = open("error_url.html",'r')
            message = file.read()
            self.wfile.write(message.encode())

    # Imposto e avvio il server
server_address = ("127.0.0.1", 3000)
webserver = http.server.HTTPServer(server_address, myHttpRequestHandler)
print("Server avviato su "+str(server_address)+". \nPer terminare l'esecuzione premere CTRL+C.")

    # Catturo CTRL+C
try:
    webserver.serve_forever()
except KeyboardInterrupt:
    print("\nServer in chiusura.. Arrivederci !")
    webserver.shutdown()
