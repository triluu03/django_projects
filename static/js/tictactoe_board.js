// for development
// const socketUrl = `ws://${window.location.host}/ws${window.location.pathname}`;

// for production
const socketUrl = `wss://${window.location.host}/ws${window.location.pathname}`;
console.log('creating socket connection to ', socketUrl);
const socket = new WebSocket(socketUrl);

socket.onmessage = function (e) {
    const message = JSON.parse(e.data);
    if (message.message === 'update board') {
        window.location.reload();
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
        })
    );
};
