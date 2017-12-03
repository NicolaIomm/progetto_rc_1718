//var https = require('https');
//var request = require('request')


var express = require('express')
var app = express()


var PORT = 3000

app.get('/login', function(req, res) {
	var client_id = '0b0257f3ab104ffc89c6f4529161b19c'
	var scopes = 'user-follow-read';
	var redirect_uri = 'https://www.spotify.com/it/'
	res.redirect('https://accounts.spotify.com/authorize' +
	  '?response_type=code' +
	  '&client_id=' + client_id +
	  '&scope=' + encodeURIComponent(scopes) +
	  '&redirect_uri=' + encodeURIComponent(redirect_uri));
});


app.listen(PORT, function(){
	console.log("Server avviato con successo sulla porta "+PORT)
})