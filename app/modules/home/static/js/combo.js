function getTargetDate() {
    const date = new Date();
    // Set target 20 days later
    date.setDate(date.getDate() + 20);
    // Set target time (e.g., 10:00:00 AM)
    date.setHours(10, 0, 0, 0);
    return date.getTime();
}

const targetTime = getTargetDate();

const countdownElement = document.getElementById('countdown');

function updateCountdown() {
    const now = new Date().getTime();
    const distance = targetTime - now;

    // Calculate time for Days, Hours, Minutes, Seconds
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    let countdownHTML = '';

    if (distance < 0) {
        // Time's up
        clearInterval(interval);
        countdownHTML = '<div class="text-center text-danger fw-bold fs-5">EXPIRED!</div>';
    } else {
        // Display remaining time
        const timerItems = [
            {value: days, label: 'Days'},
            {value: hours, label: 'Hours'},
            {value: minutes, label: 'Minutes'},
            {value: seconds, label: 'Seconds'}
        ];

        timerItems.forEach(item => {
            countdownHTML += `
                        <div class="timer-item text-center mx-1">
                            <span class="count-value text-spa-accent">${String(item.value).padStart(2, '0')}</span>
                            <label class="d-block">${item.label}</label>
                        </div>
                    `;
        });
    }

    countdownElement.innerHTML = countdownHTML;
}

// Update the countdown every 1 second
const interval = setInterval(updateCountdown, 1000);

// Run immediately on load
window.onload = updateCountdown;