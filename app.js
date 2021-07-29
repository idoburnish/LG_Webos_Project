const express = require('express');
const io = require('socket.io');
const app = new express();

var port = process.env.PORT || 8000;
var server = app.listen(port, () => {
    console.log("express server is ready.");
})

const socketServer = io(server);

socketServer.on("connection", function(socket) {
    console.log("connect client " + socket.id);
});