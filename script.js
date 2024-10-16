let pepetasBalance = 0.00;
let tapValue = 0.01;
let farmingProgress = 0;
let userLevel = 5;

document.getElementById('tap-to-earn').addEventListener('click', function() {
    pepetasBalance += tapValue;
    document.getElementById('balance-amount').textContent = pepetasBalance.toFixed(2) + ' PEPETAS';
    showTapAnimation();
    updateMissionProgress('earn', tapValue);
});

function showTapAnimation() {
    const animation = document.getElementById('tap-animation');
    animation.textContent = '+' + tapValue.toFixed(2);
    animation.style.opacity = '1';
    animation.style.transform = 'translate(-50%, -100%)';
    
    setTimeout(() => {
        animation.style.opacity = '0';
        animation.style.transform = 'translate(-50%, -50%)';
    }, 500);
}

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
        updateMissionProgress('earn', 50);
    }
});
fetch('api.php')
  .then(response => response.json())
  .then(data => {
    document.getElementById('balance-amount').textContent = data.balance + ' PEPETAS';
  });
document.getElementById('checkin-btn').addEventListener('click', function() {
    alert('Daily check-in successful! Reward added.');
    updateMissionProgress('checkin', 1);
});

function updateMissionProgress(missionType, value) {
    // Logique pour mettre à jour la progression des missions
    // Cette fonction devrait être étendue pour gérer différents types de missions
}

function levelUp() {
    userLevel++;
    document.getElementById('user-level').textContent = userLevel;
    alert('Félicitations ! Vous êtes passé au niveau ' + userLevel + ' !');
}
let pepetasBalance = localStorage.getItem('pepetasBalance') || 0.00;

function updateBalance(amount) {
    pepetasBalance = parseFloat(pepetasBalance) + amount;
    localStorage.setItem('pepetasBalance', pepetasBalance);
    document.getElementById('balance-amount').textContent = pepetasBalance.toFixed(2) + ' PEPETAS';
}

document.getElementById('tap-to-earn').addEventListener('click', function() {
    updateBalance(0.01);
    showTapAnimation();
});

// Chargement initial
document.getElementById('balance-amount').textContent = pepetasBalance + ' PEPETAS';
// Ajoutez ici d'autres fonctions pour gérer les missions, les mini-jeux, etc.