var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var userName = {};
var getName = '';
var groupName = '';

app.get("/:id/:group",function(req, res){
    res.sendfile("client.html");
    getName = req.params.id;
    groupName = req.params.group;
});

io.on('connection', function(socket){
    console.log('user connected: ', socket.id);
    userName[socket.id] = getName;
    var name = userName[socket.id]
    io.to(socket.id).emit('change name', name, groupName, socket.id);
    io.emit('connect someone', name, userName)

    socket.on('disconnect', function(){
        console.log('user disconnected: ', socket.id);
        name = userName[socket.id];
        delete userName[socket.id];
        io.emit('disconnect', name, userName)
    });

    socket.on('send message', function(name, text, id){
        io.emit('receive message', name, text, id);
    });
});

http.listen('3000', function(){
    console.log("server on!");
});
