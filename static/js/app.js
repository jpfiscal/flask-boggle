const BASE_URL = "127.0.0.1:5000";

const $submitGuess = $("#submit_guess");
const $guessInput = $("#guess_input");
const $guessResultHeader = $("#guess_result");
const $currentScore = $("#current_score");
const $timerDisplay = $("#timer_display");

let timeLimit = 60;
let timer = setInterval(function(){
    $timerDisplay.text(timeLimit);
    if (timeLimit <= 0){
        clearInterval(timer);
        finalizeGame();
        $guessInput.prop('disabled', true);
        $timerDisplay.text("Time's Up!")
    }
    timeLimit --;
},1000)

$submitGuess.on("click", async function(e){
    e.preventDefault();
    const guess = $guessInput.val();
    const response = await axios({
        url: `/check`,
        method: "POST",
        data: {guess: guess}
    })
    displayResult(guess, response.data["result"]);
    updateScore(response.data["score"]);
    $guessInput.val("");
})

function displayResult(guess, response){
    if (response === 'not-word'){
        $guessResultHeader.text(`${guess} is not a recognized word!`);
    }else if (response === 'not-on-board'){
        $guessResultHeader.text(`${guess} is not on the game board!`);
    }else if (response === 'ok'){
        $guessResultHeader.text(`Valid word: "${guess}" found!`);
    }else{
        $guessResultHeader.text(`"${guess}" has already been found.`);
    }
}

function updateScore(score){
    $currentScore.text(`Score: ${score}`)
}

async function finalizeGame(){
    const response = await axios({
        url: `/finalize_game`,
        method: "POST"
    })
}
