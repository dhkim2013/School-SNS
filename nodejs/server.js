var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var userName = {};
var groups = {};
var getName = '';
var groupName = '';

app.get("/:id/:group",function(req, res){
    res.sendfile("client.html");
    getName = req.params.id;
    groupName = req.params.group;
});

io.on('connection', function(socket){
    var group = groupName;
    if (groups[group] == null) groups[group] = {};
    var groupObj = groups[group];
    console.log('user connected: ', socket.id);
    groupObj[socket.id] = getName;
    socket.join(group);
    var name = groupObj[socket.id];
    io.to(socket.id).emit('change name', name, groupName, socket.id);
    io.in(group).emit('connect someone', name, groupObj)

    socket.on('disconnect', function(){
        console.log('user disconnected: ', socket.id);
        name = groupObj[socket.id];
        delete groupObj[socket.id];
        io.in(group).emit('disconnect', name, groupObj)
    });

    socket.on('send message', function(name, text, id){
        io.in(group).emit('receive message', name, text, id);
    });
});

http.listen('3000', function(){
    console.log("server on!");
});
