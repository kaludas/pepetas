let pepetasBalance = parseFloat(localStorage.getItem('pepetasBalance')) || 0.00;
let tapValue = 0.01;
let farmingProgress = 0;
let userLevel = parseInt(localStorage.getItem('userLevel')) || 1;
let canClaim = true;
let claimTimer = parseInt(localStorage.getItem('claimTimer')) || 0;
let lastCheckIn = parseInt(localStorage.getItem('lastCheckIn')) || 0;

function updateBalance(amount) {
    pepetasBalance = parseFloat(pepetasBalance) + amount;
    localStorage.setItem('pepetasBalance', pepetasBalance);
    document.getElementById('balance-amount').textContent = pepetasBalance.toFixed(2) + ' PEPETAS';
}

document.getElementById('tap-to-earn').addEventListener('click', function() {
    updateBalance(tapValue);
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
    if (!canClaim) {
        claimTimer--;
        if (claimTimer <= 0) {
            canClaim = true;
            document.getElementById('claim-btn').disabled = false;
            document.getElementById('claim-btn').textContent = 'Claim 50 PEPETAS';
        } else {
            let hours = Math.floor(claimTimer / 3600);
            let minutes = Math.floor((claimTimer % 3600) / 60);
            let seconds = claimTimer % 60;
            document.getElementById('claim-btn').textContent = `${hours}h ${minutes}m ${seconds}s`;
        }
        localStorage.setItem('claimTimer', claimTimer);
    }
}

setInterval(updateFarmingTimer, 1000);

document.getElementById('claim-btn').addEventListener('click', function() {
    if (canClaim) {
        updateBalance(50);
        canClaim = false;
        claimTimer = 21600; // 6 heures
        this.disabled = true;
        updateMissionProgress('earn', 50);
    }
});

document.getElementById('checkin-btn').addEventListener('click', function() {
    const now = Date.now();
    if (now - lastCheckIn > 86400000) { // 24 heures en millisecondes
        updateBalance(10);
        lastCheckIn = now;
        localStorage.setItem('lastCheckIn', lastCheckIn);
        alert('Daily check-in successful! You received 10 PEPETAS.');
        updateMissionProgress('checkin', 1);
    } else {
        alert('You can only check in once per day.');
    }
});

function updateMissionProgress(missionType, value) {
    // Implémentez ici la logique pour mettre à jour les missions
    console.log(`Mission progress: ${missionType}, value: ${value}`);
}

function levelUp() {
    userLevel++;
    localStorage.setItem('userLevel', userLevel);
    document.getElementById('user-level').textContent = userLevel;
    alert('Félicitations ! Vous êtes passé au niveau ' + userLevel + ' !');
}

// Initialisation
document.getElementById('balance-amount').textContent = pepetasBalance.toFixed(2) + ' PEPETAS';
document.getElementById('user-level').textContent = userLevel;

// Ajoutez ici le code pour les tâches et l'invitation d'amis
const tasks = JSON.parse(localStorage.getItem('tasks')) || [
    { name: 'Collect 100 PEPETAS', reward: 50, progress: 0, goal: 100 },
    { name: 'Invite 2 friends', reward: 100, progress: 0, goal: 2 }
];

function updateTasks() {
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = '';
    tasks.forEach((task, index) => {
        const li = document.createElement('li');
        li.textContent = `${task.name} - Progress: ${task.progress}/${task.goal}`;
        const completeBtn = document.createElement('button');
        completeBtn.textContent = 'Complete';
        completeBtn.onclick = () => completeTask(index);
        li.appendChild(completeBtn);
        taskList.appendChild(li);
    });
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function completeTask(index) {
    if (tasks[index].progress < tasks[index].goal) {
        tasks[index].progress++;
        if (tasks[index].progress === tasks[index].goal) {
            updateBalance(tasks[index].reward);
            alert(`Task completed! You earned ${tasks[index].reward} PEPETAS.`);
        }
        updateTasks();
    }
}

document.getElementById('invite-btn').addEventListener('click', function() {
    alert('Invitation link: https://t.me/your_bot_link');
    // Simuler l'invitation d'un ami
    tasks[1].progress = Math.min(tasks[1].progress + 1, tasks[1].goal);
    updateTasks();
});

updateTasks();
