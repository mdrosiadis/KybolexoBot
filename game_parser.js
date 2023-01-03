HOR_LEN = 38;
VER_LEN = 39;
LETTERS_PER_LINE = 6;
greekLetters = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ";

player_divs = [
	document.querySelector("#cubeword_player1"),
	document.querySelector("#cubeword_player2")
];

game_board = document.querySelector("#cubeWordBoardContainer");


function parseLetter(domelem) {
  let letterIndex = (-parseInt(domelem.style["background-position-y"])/VER_LEN)*LETTERS_PER_LINE -
		(parseInt(domelem.style["background-position-x"])/HOR_LEN);

  return {x: parseInt(domelem.style.left) / HOR_LEN, 
		  y: parseInt(domelem.style.top) / VER_LEN,
	      letter: greekLetters[letterIndex],
	  	  bonus: domelem.childNodes[0].innerText 
	};
}

function parsePlayer(player_div) {
	return {
		name: player_div.querySelector(".gnh_name").innerText,
		elo: parseInt(player_div.querySelector(".gnh_elo").innerText),
		score: parseInt(player_div.querySelector(".gnh_score_text").innerText),	
		isActive: player_div.querySelector(".gamenickholder_content").matches("gameNickHolder2Active")
	};
}

function getGameState() {
	const all_letters = [...game_board.children];
	return {
		players : player_divs.map(parsePlayer),
		game_board: all_letters.map(parseLetter)
	};
}

console.log(JSON.stringify(getGameState()));
