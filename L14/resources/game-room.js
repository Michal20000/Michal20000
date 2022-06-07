var socketIO = io("/game-room");
console.log(io);
console.log(socketIO);



const onGame = function() {
	console.log("");

};
const onFrame = function() {
	console.log("");

};
const onEnd = function() {
	console.log("");

};



socketIO.on("Game", onGame);
socketIO.on("Frame", onFrame);
socketIO.on("End", onEnd);
