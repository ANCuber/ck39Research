var express = require('express');
var fs = require('fs');

var port = 3000;
var app = express();
app.set('views', './views');
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.urlencoded({
  extended: true
}))

app.get('/start', function (req, res) {  
  res.render('index',{
      latex : "x\\implies y"
  });
}); 

app.post('/send',function(req,res){ 
    var content = req.body.response;
    res.render('send',{
        yourres : content
    });
   
    
});


app.get('*',function(req,res){
    res.send('404 error!!!!!  what are you doing?');
});


app.listen(port, function(err){
    if(err){
        console.log(err);
    }else{
        console.log('http://localhost:' + port);
    }
});