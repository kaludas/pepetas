let pepetasBalance = 21749.85;
let tapValue = 0.01;
let farmingProgress = 0;

document.getElementById('tap-to-earn').addEventListener('click', function() {
    pepetasBalance += tapValue;
    document.getElementById('balance-amount').textContent = pepetasBalance.toFixed(2) + ' PEPETAS';
});

function updateFarmingTimer() {
    let timer = document.getElementById('farming-timer');
    let [hours, minutes, seconds] = timer.textContent.split(':').map(Number);
    
    if (seconds > 0) {
        seconds--;
    } else if (minutes > 0) {
        minutes--;
        seconds = 59;
    } else if (hours > 0) {
        hours--;
        minutes = 59;
        seconds = 59;
    }

    timer.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

    if (hours === 0 && minutes === 0 && seconds === 0) {
        document.getElementById('claim-btn').disabled = false;
    }
}

setInterval(updateFarmingTimer, 1000);

document.getElementById('claim-btn').addEventListener('click', function() {
    if (!this.disabled) {
        pepetasBalance += 50;
        document.getElementById('balance-amount').textContent = pepetasBalance.toFixed(2) + ' PEPETAS';
        this.disabled = true;
        document.getElementById('farming-timer').textContent = '06:00:00';
    }
});

document.getElementById('checkin-btn').addEventListener('click', function() {
    // Logique pour le check-in quotidien
    alert('Daily check-in successful! Reward added.');
});