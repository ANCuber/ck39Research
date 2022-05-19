var express = require('express');
var fs = require('fs');

var port = 3000;
var app = express();


app.get('/', function (req, res) {  
  res.sendFile('index.html', { root: __dirname });
}); 





app.listen(port, function(err){
    if(err){
        console.log(err);
    }else{
        console.log('http://localhost:' + port);
    }
});