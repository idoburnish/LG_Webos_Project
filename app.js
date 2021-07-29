const express = require('express');
const io = require('socket.io');
const app = new express();

var port = process.env.PORT || 8000;
var server = app.listen(port, () => {
    console.log("express server is ready.");
})

const socketServer = io(server);

let finger = 0;

socketServer.on("connection", function(socket) {
    console.log("connect client " + socket.id);
    
    socket.on("finger_number", function(data){
        finger = data.finger_number;
        socket.emit("finger_number",{
            finger : data.finger_number
        });
    })


    socket.on("disconnection",function(reason){
        console.log(`disconnect id : ${socket.id}`);
        
    })
});


