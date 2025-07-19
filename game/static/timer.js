let startTime, interval;

function startTimer() {
  startTime = Date.now();
  interval = setInterval(updateTimer, 1000);
}

function updateTimer() {
  const currentTime = Date.now();
  const elapsedTime = currentTime - startTime;
  const minutes = Math.floor(elapsedTime / 60000);
  const seconds = Math.floor((elapsedTime % 60000) / 1000);
  const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  document.getElementById('timer').innerText = formattedTime;
}

function stopTimer() {
  clearInterval(interval);
}

// The startTimer function should be called when the typing test starts
startTimer();
