const cells = document.querySelectorAll('.cell');
const resetButton = document.querySelector('.reset');
const currentTurn = document.querySelector('.current-turn');
const player1Score = document.querySelector('.score1');
const player2Score = document.querySelector('.score2');
const draw = document.querySelector('.draw');
const message = document.querySelector('.content');
const overlay = document.getElementById('overlay');
const close = document.getElementById('close');

const winCombinaisons = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6],
];

let turn = true;
let usedCells = [];
let winner = false;
let drawscore = 0;


let player1 = {
    symbol : '<i class = "fa fa-close"></i>',
    played : [],
    score : 0
}

let player2 = {
    symbol : '<i class = "fa fa-circle"></i>',
    played : [],
    score : 0
}

checkturn();

for (let i = 0; i < 9; i++) {
    cells[i].addEventListener('click', () => {
        if (isEmpty(i)) {
            if (turn) {
                addSymbol(player1, i);
                turn = false;
                checkWin(player1);
                checkturn();
            } else {
                addSymbol(player2, i);
                turn = true;
                checkWin(player2);
                checkturn();
            }
        }else{
            alert('Utilisez une autre case !');
        }
    });
}


function addSymbol(player, i){
    cells[i].innerHTML = player.symbol;
    player.played.push(i);
    usedCells.push(i);
}

function checkWin(player){
    if(!winner){
        winCombinaisons.forEach(combinaison => {
            if (combinaison.every(cell => player.played.includes(cell))) {
                player.score++;
                showScore();
                winner = true;
                overlay.style.display = 'flex';
                message.innerHTML = player.symbol + '<h2>WIN !</h2>';
            }
        });
    }
    checkDraw();
}

function isEmpty(i){
    if (usedCells.includes(i)) {
        return false;
    }
    return true;
}   

function resetGame(){
    cells.forEach(cell => {
        cell.innerHTML = '';
    });
    player1.played = [];
    player2.played = [];
    usedCells = [];
    turn = true;
    checkturn();
}

resetButton.addEventListener('click', resetGame);

function checkturn(){
    if (turn) {
        currentTurn.innerHTML = player1.symbol;
    }else{
        currentTurn.innerHTML = player2.symbol;
    }
}


function showScore(){
    player1Score.innerHTML = player1.score;
    player2Score.innerHTML = player2.score;
    draw.innerHTML = drawscore;
} 

function checkDraw(){
    if (!winner && usedCells.length === 9) {
        drawscore++;
        showScore();
        draw.innerHTML = drawscore;
        overlay.style.display = 'flex';
        message.innerHTML = '<h2> Egalité!</h2>';
    }
}

function showMessage(){
    if (winner) {
        message.innerHTML = player1.symbol + '<h2>WIN !</h2>';
    }
}

close.addEventListener('click', () => {
    overlay.style.display = 'none';
    resetGame();
    showMessage();
    winner = false;
});