function getTargetDate() {
  const date = new Date();
  date.setDate(date.getDate() + 20);
  date.setHours(10, 0, 0, 0);
  return date.getTime();
}

const targetTime = getTargetDate();
const countdownElement = document.getElementById('countdown');

function updateCountdown() {
  if (!countdownElement) return;

  const now = new Date().getTime();
  const distance = targetTime - now;

  const days = Math.floor(distance / (1000 * 60 * 60 * 24));
  const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((distance % (1000 * 60)) / 1000);

  let countdownHTML = '';

  if (distance < 0) {
    clearInterval(interval);
    countdownHTML = '<div class="text-center text-danger fw-bold fs-5">EXPIRED!</div>';
  } else {
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

const interval = setInterval(updateCountdown, 1000);
window.onload = updateCountdown;