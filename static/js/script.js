// Smooth button click animation
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.style.transform = "scale(0.95)";
    setTimeout(() => {
      btn.style.transform = "scale(1)";
    }, 150);
  });
});

// Simple alert for actions (you can customize)
function showMessage(msg) {
  alert(msg);
}

// Dark mode toggle (optional)
function toggleTheme() {
  document.body.classList.toggle('light-mode');
}