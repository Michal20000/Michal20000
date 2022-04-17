/* 
/// <reference path = "./angular.min.js"/>
/// <reference path = "./snake.js"/>
*/

var application = angular.module("Main", []);
var mainController = ($scope) => {
  const ChessGame = function(white, black, result, date, url) {
    this.white = white;
    this.black = black;
    this.result = result;
    this.date = date;
    this.url = url;

  };
  let games = [
    new ChessGame("Teonasemo", "ashrocks007", "White wins!", "YYYY-MM-DD", "./abc.gif"),
    new ChessGame("Teonasemo", "ashrocks007", "White wins!", "YYYY-MM-DD", "./abc.gif"),
    new ChessGame("Teonasemo", "ashrocks007", "White wins!", "YYYY-MM-DD", "./abc.gif")

  ];
  $scope.message = "Hello World!";
  $scope.chessGame = new ChessGame("Teonasemo", "ashrocks007", "White wins!", "YYYY-MM-DD", "./abc.gif");
  console.log("Hello!");

};
application.controller("MainController", mainController);
