// for development
// const socketUrl = `ws://${window.location.host}/ws${window.location.pathname}`;

// for production
const socketUrl = `wss://${window.location.host}/ws${window.location.pathname}`;
const socket = new WebSocket(socketUrl);

const collections = document.getElementsByTagName('td');

var nextMove = 'X';

var boardDetails = [];
Array.from(collections).forEach((element) => {
    boardDetails.push(element.children[0].innerHTML);
});

socket.onmessage = function (e) {
    const message = JSON.parse(e.data);
    if (message.message == 'join game') {
        if (message.previous == 'X') {
            nextMove = 'O';
        } else {
            nextMove = 'X';
        }
    } else if (message.message === 'play message') {
        const buttonId = message.buttonId;
        collections[buttonId].children[0].disabled = true;
        collections[buttonId].children[0].removeAttribute('onclick');
        collections[buttonId].children[0].innerHTML = nextMove;
        boardDetails[buttonId] = nextMove;
        if (nextMove == 'X') {
            nextMove = 'O';
            collections[buttonId].children[0].style.backgroundColor = '#7FFFD4';
        } else {
            nextMove = 'X';
            collections[buttonId].children[0].style.backgroundColor = '#FF7FAA';
        }
    } else if (message.message == 'save game') {
        const status = message.status;
        if (status == 'success') {
            const temp = document.getElementsByTagName('template')[0];
            document
                .getElementById('game_header')
                .appendChild(temp.content.cloneNode(true));
        } else {
            const temp = document.getElementsByTagName('template')[1];
            document
                .getElementById('game_header')
                .appendChild(temp.content.cloneNode(true));
        }
    } else if (message.message == 'end game') {
        const boardId = message.board_id;
        const endUrl = `${window.location.origin}/tic_tac_toe/game/${boardId}/end/`;
        window.location.href = endUrl;
    }
};

socket.onopen = function (e) {
    socket.send(
        JSON.stringify({
            message: 'join game',
        })
    );
};

const updateBoard = function (board_id, row, col) {
    socket.send(
        JSON.stringify({
            message: 'update board',
            board_id: board_id,
            row: row,
            col: col,
            details: boardDetails,
            next_move: nextMove,
        })
    );
};

const saveGame = function () {
    socket.send(
        JSON.stringify({
            message: 'save game',
            details: boardDetails.toString(),
            next_move: nextMove,
        })
    );
};
