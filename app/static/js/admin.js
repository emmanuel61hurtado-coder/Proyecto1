document.addEventListener('DOMContentLoaded', () => {
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const sidebar = document.querySelector('.admin-sidebar');

  if (menuBtn && sidebar) {
    menuBtn.addEventListener('click', () => sidebar.classList.toggle('open'));
  }

  // Confirmación antes de eliminar
  document.querySelectorAll('[data-confirm]').forEach(form => {
    form.addEventListener('submit', (e) => {
      const msg = form.getAttribute('data-confirm');
      if (!confirm(msg)) e.preventDefault();
    });
  });

  // Auto-scroll al final del feed de notas (lo más reciente visible)
  const notesFeed = document.querySelector('.notes-feed');
  if (notesFeed) {
    notesFeed.scrollTop = notesFeed.scrollHeight;
  }

  // Auto-cerrar flash messages
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.5s';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 500);
    }, 5000);
  });
});
