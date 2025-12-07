document.addEventListener('DOMContentLoaded', function() {

  // Hover Effects
  const statsCard = document.querySelector('.stats-card');
  const imageSecondary = document.querySelector('.image-secondary');

  if (statsCard) {
    statsCard.addEventListener('mouseenter', function() {
      statsCard.style.transition = 'transform 0.3s ease';
      statsCard.style.transform = 'translateY(-5px)';
    });
    statsCard.addEventListener('mouseleave', function() {
      statsCard.style.transform = 'translateY(0)';
    });
  }

  if (imageSecondary) {
    imageSecondary.addEventListener('mouseenter', function() {
      imageSecondary.style.transform = 'translateX(-3%) translateY(-3%) scale(1.03)';
      imageSecondary.style.boxShadow = '0 25px 60px rgba(0, 0, 0, 0.8)';
      imageSecondary.style.zIndex = '40';
    });
    imageSecondary.addEventListener('mouseleave', function() {
      imageSecondary.style.transform = 'translateX(0) translateY(0) scale(1)';
      imageSecondary.style.boxShadow = '0 15px 50px rgba(0, 0, 0, 0.5)';
      imageSecondary.style.zIndex = '20';
    });
  }

  // Count-up Animation
  const statsItems = document.querySelectorAll('.stats-item h3');

  function countUp(el, endValue) {
    let current = 0;
    const duration = 2000;
    const step = endValue / (duration / 10);

    const timer = setInterval(() => {
      current += step;
      if (current >= endValue) {
        clearInterval(timer);
        current = endValue;
      }
      el.textContent = Math.floor(current) + '+';
    }, 10);
  }

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        statsItems.forEach(item => {
          if (!item.hasAttribute('data-counted')) {
            const valueText = item.textContent.replace('+', '');
            const endValue = parseInt(valueText);
            countUp(item, endValue);
            item.setAttribute('data-counted', 'true');
          }
        });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  const aboutSection = document.querySelector('.about-section');
  if (aboutSection) {
    observer.observe(aboutSection);
  }
});