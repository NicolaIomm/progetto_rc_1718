# progetto_rc_1718

Avviare il server tramite:
	~ python3 startServer.py

TicketHandler gestisce la vendita dei biglietti. 
Ogni volta che un utenta acquista un biglietto, tickethandler riceve un messaggio tramite coda su su rabbitmq. 
Rabbitmq gira in locale su docker. 
Una volta creato il contenitore: $docker start name-container (rabbitmq)
	
Spiegazione dei file:
	
	# startServer.py : - Si occupa di avviare il server su localhost, 
							porta 3000, e gestire le richieste HTTP.
					   - Gestisce il collegamento con spotify (OAuth2
							e Web API) per ottenere gli artisti seguiti.
					   - Si occupa di riportare i risultati ottenuti 
							nella pagina di risposta
	# functions.py :   - Contiene le funzioni che utilizza startServer.py
	# error_url.html:  - Pagina mostrata nel caso in cui si richiede
							una risorsa che il webserver non gestisce
	# page_pattern.txt: - File di testo letto dal webserver, sulla base
							della quale crea la pagina da mostrare all'utente
						- Contiene lo script per la chiamata ai concerti
							e il titolo della pagina
	# result.html: - Pagina da mostrare all'utente finale, completa di
							script e risultati della Web API a spotify
							
						

API REST:

	Title: Login
	URL: /callback?code=code
	Method: GET
	Parameters:
		code: string
	Success response:
		Code: 200

	Title: Cerca Concerti
	URL: /cercaConcerti/artist=artist?
	Method: GET
	Parameters:
		artist: string
	Success response:
		Code: 200

	Title: Compra biglietti
	URL: /compraBiglietti/target=target?
	Parameters:
		target: string
	Method: GET
	Success response: 
		Code: 200

Spiegazione Spotify OAuth2.0 : 
 - https://developer.spotify.com/web-api/authorization-guide/
