import http.server
import http.client
import urllib.parse
import ssl
import base64
import json
import time

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

def do_refresh_token_request(request_handler, old_token):

    body_parameters = {"grant_type":grant_type,
                       "refresh_token":old_token}
    
    token_refresh_request = http.client.HTTPSConnection("account.spotify.com")
    token_refresh_request.request("POST",
                                  "/api/token",
                                  body_parameters.encode(),
                                  get_headers_token_request())
    response = token_refresh_request.getresponse()
                       
    request_handler.send_response(response.status, response.reason)
    request_handler.end_headers()

    json_response = json.loads(response.read().decode())
    return json_response                      

    # Parse della risposta per ottenere il token
def parse_json_response_token(json_response):
    access_token = json_response["access_token"]
    token_type = json_response["token_type"]
    expires_in = int(json_response["expires_in"])
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

def load_page_to_show(followed_artists):
    pattern = open("page_pattern.txt","r")
    rows = pattern.readlines()
    pattern.close()

    insert_here = rows.index("</div>\n")+1
    for artist in followed_artists:
        format = "<div align=center><form method=\"get\">   \
                  <h4>"+artist+"</h4><button type=\"submit\" formaction=\"cercaConcerti/artist="+urllib.parse.quote(artist)+"\">cercaBiglietti</button>                                \
                  </form></div>"
        rows.insert(insert_here,format)
        insert_here += 1

    page_to_write = open("result.html","w")
    for line in rows:
        page_to_write.write(line+"\n")
    page_to_write.close()

    page_to_load = open("result.html","r")
    page = page_to_load.read()
    page_to_load.close()
    return page

def getConcertBodyToShow(artist, listConcert):
    i = 1;

    data = ""
    for dict in listConcert:
        titolo = str(dict["title"])
        sede = str(dict["venue"])
        citta = str(dict["city"])
        prezzo = str(dict["price"])
        giorno = str(dict["start_time"])
        data += "<p>"+str(i)+" --------------------------------------------------------------------"+"</p>\n"
        data += "<p>Titolo: "+titolo+"</p>\n"
        data += "<p>Sede: "+sede+"</p>\n"
        data += "<p>Citta: "+citta+"</p>\n"
        data += "<p>Prezzo: "+prezzo+"</p>\n"
        data += "<p>Ora di inizio: "+giorno+"</p>\n"
        data += "<button onclick=\"compraBiglietti('"+artist+","+titolo+","+giorno+"')\">Compra il biglietto</button>\n"
        i += 1
    
    body = "<html>                                                              \n\
            <head>                                                              \n\
            <script>                                                            \n\
            function compraBiglietti(concert){                                  \n\
            var request = new XMLHttpRequest();                                 \n\
            request.open(\"GET\", \"/compraBiglietti/?target=\"+concert, false );\n\
            request.send(null);                                                 \n\
            }                                                                   \n\
            </script>                                                           \n\
            </head>                                                             \n\
            <body>                                                              \n\
            <div align=center>                                                  \n\
            <h1>Lista dei concerti di "+artist+":</h1><br>" +                   \
            data +                                                              \
            "</div>                                                             \n\
            </body>                                                             \n\
            </html>"    
    return body
