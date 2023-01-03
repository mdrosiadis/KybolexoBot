const HOR_LEN = 38;
const VER_LEN = 39;
const LETTERS_PER_LINE = 6;
const greekLetters = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ";



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
	const player_divs = [
		document.querySelector("#cubeword_player1"),
		document.querySelector("#cubeword_player2")
	];

	const game_board = document.querySelector("#cubeWordBoardContainer");
	const all_letters = [...game_board.children];

	return {
		players : player_divs.map(parsePlayer),
		game_board: all_letters.map(parseLetter)
	};
}


const pilot_div = document.createElement('div');
pilot_div.style = `
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	align-items: center;
	position: absolute;
	background: #efefef;
	color: #111;
	border: 3px solid gold;
	border-radius: 5px;
	padding: 5px;
	width: 25vw;
	height: 40vh;
	font-size: 1.5rem;
	font-family: serif;
	top: 50%;
	right: 0;
	transform: translate(0, -50%);
	z-index: 9999;
	visibility: visible;
`;

pilot_div.innerHTML = `
<span style="font-weight: bold; font-style: italic;">Κυβόλεξο Bot</span>
<div id="bot-solution-container"></div>
<button id="get-solutions-button" type="button">Εύρεση Λύσεων</button>
`;

document.body.appendChild(pilot_div);
// add toggle button
document.addEventListener('keyup', function(event) {
  if (event.ctrlKey && event.key === ' ') {
	  pilot_div.style.visibility = pilot_div.style.visibility === 'visible' ? 'hidden' : 'visible';
  }
});

const websocket = new WebSocket("ws://localhost:5678/");
websocket.onmessage = ({data}) => {
	console.log(data);
	const parsed_data = JSON.parse(data);
	clearAllChildren(solutions_container);

	parsed_data.forEach(([word, points, path]) => {
		const sdiv = document.createElement('div');
		sdiv.style = `
			background: lightgray;
			border: 2px solid black;
			border-radius: 2px;
			font-size: 1rem;
			padding: 5px;
			margin: 5px 0;
			`;
		sdiv.innerText = `${word} (${points} πόντοι)`;
		solutions_container.appendChild(sdiv);
	});
	// solutions_container.innerText = JSON.stringify(parsed_data);
};

const btn = document.querySelector("#get-solutions-button");
btn.addEventListener("click", event => {
	const data = getGameState();


	websocket.send(JSON.stringify(data));
});

function clearAllChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.lastChild);
    }
}
const solutions_container = document.querySelector("#bot-solution-container");
// console.log(JSON.stringify(getGameState()));
