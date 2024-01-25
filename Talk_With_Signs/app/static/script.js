//update the content of the 'current-word' paragraph
function updateCurrentWord() {
    fetch("/current_word")
        .then(response => response.text())
        .then(word => {
            document.getElementById("current-word").innerText = word.replace("data: ", "");
        })
        .catch(error => console.error("Error fetching current word:", error));
}

// Set up SSE connection
const eventSource = new EventSource("/current_word");

// Flag to determine whether predictions should be processed
let processPredictions = false;

// Listen for the 'message' event
eventSource.addEventListener("message", () => {
    if (processPredictions) {
        updateCurrentWord();
    }
});

// Button elements
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');

// Function to start predictions
function startPredictions() {
    startBtn.disabled = true;
    pauseBtn.disabled = false;
    processPredictions = true;
    fetch("/start_predictions");
}

// Function to pause predictions
function pausePredictions() {
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    processPredictions = false;
    fetch("/pause_predictions");
}
