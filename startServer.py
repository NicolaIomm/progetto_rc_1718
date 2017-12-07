from functions import *

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

            current_token_time = time.time()

                # do HTTP POST to get token
            json_response_token = do_token_request(self, code)
            (access_token, token_type, expires_in, scope) = parse_json_response_token(json_response_token)
            #self.wfile.write(access_token.encode())
            
                # Gestisco il refresh del token, nel caso in cui sia scaduto
            if (time.time() - current_token_time > expires_in):
                json_response_token = do_refresh_token_request(self,code)
                (access_token, token_type, expires_in, scope) = parse_json_response_token(json_response_token) 
            
                # request for followed artists
            query_response = do_followed_artists_query(access_token)
            self.send_response(query_response.status, query_response.reason)
            body = query_response.read().decode()
            #self.wfile.write(("token expires in "+str(expires_in)).encode())
            #self.wfile.write(body.encode())
            json_data = json.loads(body)
            followed_artists = parse_json_response_artists(json_data)

                # Ottengo la stringa da mostrare con tutti i risultati, e la carico come risposta
            page = load_page_to_show(followed_artists)
            self.wfile.write(page.encode())
            
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

    # Catturo CTRL+C e in caso interrompo il server
try:
    webserver.serve_forever()
except KeyboardInterrupt:
    print("\nServer in chiusura.. Arrivederci !")
    webserver.shutdown()
