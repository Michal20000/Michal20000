const clearContainer = "<div class = \"clear\"></div>";
const generateChessCardContainer = (source) => {
  return "<div class = \"chess-card-container\"><img class = \"chess-card\" source = \"" + source + "\" src = \"./chess-main.png\" alt = \"\"></div>";

};

const databaseCards = [
  "./chess-cards/0.png",
  "./chess-cards/1.png",
  "./chess-cards/2.png",
  "./chess-cards/3.png",
  "./chess-cards/4.png",
  "./chess-cards/5.png",
  "./chess-cards/6.png",
  "./chess-cards/7.png",
  "./chess-cards/8.png",
  "./chess-cards/9.png",
  "./chess-cards/10.png",
  "./chess-cards/11.png",
  "./chess-cards/12.png",
  "./chess-cards/13.png",
  "./chess-cards/14.png",
  "./chess-cards/15.png"

];
const gameCards = [

];

const randomValue = (min, max) => {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;

};

console.log(databaseCards.length);
for (let i = 0; i < 8; ++i) {
  let index = randomValue(0, databaseCards.length);
  gameCards.push(databaseCards[index]);
  gameCards.push(databaseCards[index]);
  databaseCards.splice(index, 1);

};

gameCards.sort(() => {
  return Math.random() > 0.5 ? 1 : -1;

});

console.log(gameCards);
for (let gameCard of gameCards) {
  $(".chess-cards-container").append(generateChessCardContainer(gameCard));

};
$(".chess-cards-container").append(clearContainer);



var x = 0;
var objects = [
  null,
  null
  
];
var score = 0;
var matched = 0;
var time = (new Date()).getTime();

const checkObjects = () => {
  score = score + 1;
  if ($(objects[0]).attr("source") == $(objects[1]).attr("source")) {
    matched = matched + 1;
    $(objects[0]).hide();
    $(objects[1]).hide();

  }
  else {
    $(objects[0]).attr("src", "./chess-main.png");
    $(objects[1]).attr("src", "./chess-main.png");

  }

  if (matched == 8) {
    time = (new Date()).getTime() - time;
    alert("Wynik: " + score * time / 1000);

  }
  x = 0;

};

$(".chess-card").click(function() {
  if (x == 0) {
    objects[0] = this;
    $(this).attr("src", $(this).attr("source"));
    x = 1;
    return;

  }
  if (x == 1) {
    objects[1] = this;
    $(this).attr("src", $(this).attr("source"));

    if (objects[0] !== objects[1]) {
      x = 2;
      setTimeout(checkObjects, 1000);

    }
    return;

  }

});
