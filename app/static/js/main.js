document.addEventListener('DOMContentLoaded', () => {
  initPreloader();
  initCursor();
  initParticles();
  initNoiseTexture();
  initHeaderScroll();
  initMobileNav();
  initScrollReveal();
  initParallax();
  initCardTilt();
  initCounterAnimation();
  initServiceLinks();
  initOrderForm();
  initSmoothAnchors();
  initSplitText();
  initShareMenu();
});

/* ═══ Preloader ═══ */
function initPreloader() {
  const preloader = document.getElementById('preloader');
  if (!preloader) return;

  window.addEventListener('load', () => {
    setTimeout(() => {
      preloader.classList.add('hidden');
      document.body.style.overflow = '';
    }, 600);
  });

  setTimeout(() => {
    if (!preloader.classList.contains('hidden')) {
      preloader.classList.add('hidden');
      document.body.style.overflow = '';
    }
  }, 4000);
}

/* ═══ Custom Cursor ═══ */
function initCursor() {
  if (window.matchMedia('(hover: none)').matches) return;

  const dot = document.createElement('div');
  dot.className = 'cursor-dot';
  const ring = document.createElement('div');
  ring.className = 'cursor-ring';
  document.body.appendChild(dot);
  document.body.appendChild(ring);

  let mouseX = 0, mouseY = 0;
  let dotX = 0, dotY = 0;
  let ringX = 0, ringY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  function animateCursor() {
    dotX += (mouseX - dotX) * 0.35;
    dotY += (mouseY - dotY) * 0.35;
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;

    dot.style.left = dotX + 'px';
    dot.style.top = dotY + 'px';
    ring.style.left = ringX + 'px';
    ring.style.top = ringY + 'px';
    requestAnimationFrame(animateCursor);
  }
  animateCursor();

  document.querySelectorAll('a, button, .service-card, .testimonial-card, .btn').forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('hovering'));
    el.addEventListener('mouseleave', () => ring.classList.remove('hovering'));
  });
}

/* ═══ Particle System ═══ */
function initParticles() {
  const canvas = document.getElementById('particles-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let w, h;
  const particles = [];
  const COUNT = 60;

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * w;
      this.y = Math.random() * h;
      this.size = Math.random() * 2 + 0.5;
      this.speedX = (Math.random() - 0.5) * 0.3;
      this.speedY = (Math.random() - 0.5) * 0.3;
      this.opacity = Math.random() * 0.5 + 0.1;
      this.hue = Math.random() > 0.5 ? 45 : 270;
    }
    update() {
      this.x += this.speedX;
      this.y += this.speedY;
      if (this.x < 0 || this.x > w) this.speedX *= -1;
      if (this.y < 0 || this.y > h) this.speedY *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${this.hue}, 60%, 70%, ${this.opacity})`;
      ctx.fill();
    }
  }

  for (let i = 0; i < COUNT; i++) particles.push(new Particle());

  let mouse = { x: null, y: null };
  document.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });

  function animate() {
    ctx.clearRect(0, 0, w, h);

    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw();

      if (mouse.x !== null) {
        const dx = particles[i].x - mouse.x;
        const dy = particles[i].y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 150) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `hsla(45, 60%, 70%, ${0.08 * (1 - dist / 150)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }

      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `hsla(45, 40%, 60%, ${0.06 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(animate);
  }
  animate();
}

/* ═══ Noise Texture ═══ */
function initNoiseTexture() {
  const canvas = document.getElementById('noise-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let w = canvas.width = window.innerWidth;
  let h = canvas.height = window.innerHeight;
  window.addEventListener('resize', () => {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  });

  function noise() {
    const imageData = ctx.createImageData(w, h);
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 4) {
      const v = Math.random() * 255;
      data[i] = v;
      data[i + 1] = v;
      data[i + 2] = v;
      data[i + 3] = 255;
    }
    ctx.putImageData(imageData, 0, 0);
  }

  function loop() { noise(); requestAnimationFrame(loop); }
  loop();
}

/* ═══ Header scroll ═══ */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        header.classList.toggle('scrolled', window.scrollY > 60);
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

/* ═══ Mobile Nav ═══ */
function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  const overlay = document.querySelector('.mobile-nav-overlay');
  if (!toggle || !links) return;

  function closeNav() {
    links.classList.remove('open');
    toggle.classList.remove('active');
    toggle.setAttribute('aria-expanded', 'false');
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  function openNav() {
    links.classList.add('open');
    toggle.classList.add('active');
    toggle.setAttribute('aria-expanded', 'true');
    if (overlay) overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  toggle.addEventListener('click', () => {
    links.classList.contains('open') ? closeNav() : openNav();
  });

  if (overlay) overlay.addEventListener('click', closeNav);

  links.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeNav);
  });
}

/* ═══ Scroll Reveal ═══ */
function initScrollReveal() {
  const targets = document.querySelectorAll('.reveal-fade, .reveal-scale, .reveal-skew, .reveal-stagger');

  if (!targets.length) return;

  if (!('IntersectionObserver' in window)) {
    targets.forEach(el => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  targets.forEach(el => observer.observe(el));
}

/* ═══ Parallax on scroll ═══ */
function initParallax() {
  const els = document.querySelectorAll('[data-parallax]');
  if (!els.length) return;

  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const st = window.scrollY;
        els.forEach(el => {
          const speed = parseFloat(el.dataset.parallax) || 0.1;
          const rect = el.getBoundingClientRect();
          if (rect.top < window.innerHeight && rect.bottom > 0) {
            const offset = (rect.top - window.innerHeight * 0.5) * speed;
            el.style.transform = `translateY(${offset}px)`;
          }
        });
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

/* ═══ 3D Card Tilt ═══ */
function initCardTilt() {
  const cards = document.querySelectorAll('.service-card');
  if (!cards.length || window.matchMedia('(hover: none)').matches) return;

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      const tiltX = (y - 0.5) * 12;
      const tiltY = (0.5 - x) * 12;

      card.style.setProperty('--mouse-x', (x * 100) + '%');
      card.style.setProperty('--mouse-y', (y * 100) + '%');
      card.style.transform = `perspective(800px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-6px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) translateY(0)';
    });
  });
}

/* ═══ Counter Animation ═══ */
function initCounterAnimation() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.count);
        const duration = parseInt(el.dataset.duration) || 2000;
        const start = performance.now();

        function update(now) {
          const progress = Math.min((now - start) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.floor(eased * target) + (target > 100 ? '+' : '');
          if (progress < 1) requestAnimationFrame(update);
          else el.textContent = target + (target > 100 ? '+' : '');
        }
        requestAnimationFrame(update);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

/* ═══ Service Link Click ═══ */
function initServiceLinks() {
  document.querySelectorAll('.service-link[data-service-id]').forEach(btn => {
    btn.addEventListener('click', () => {
      const serviceId = btn.getAttribute('data-service-id');
      const select = document.getElementById('order-service');
      const orderSection = document.getElementById('order');

      if (select) select.value = serviceId;
      if (orderSection) {
        orderSection.scrollIntoView({ behavior: 'smooth' });
      }

      const nameField = document.getElementById('order-name');
      if (nameField) setTimeout(() => nameField.focus(), 800);
    });
  });
}

/* ═══ Order Form (AJAX) ═══ */
function initOrderForm() {
  const form = document.getElementById('order-form');
  if (!form) return;

  const feedback = document.getElementById('order-feedback');
  const submitBtn = form.querySelector('.btn-submit');
  const submitLabel = submitBtn ? submitBtn.querySelector('.btn-label') : null;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    if (!payload.name || !payload.phone) {
      showFeedback(feedback, form.dataset.errorText || 'Por favor completa los campos obligatorios.', true);
      return;
    }

    if (submitBtn) submitBtn.setAttribute('disabled', 'true');
    if (submitLabel) submitLabel.textContent = form.dataset.sendingText || 'Enviando...';

    try {
      const res = await fetch('/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (data.ok) {
        showFeedback(feedback, form.dataset.successText || 'Solicitud recibida. Redirigiendo a WhatsApp...', false);
        form.reset();
        setTimeout(() => {
          window.open(data.whatsapp_link, '_blank');
        }, 900);
      } else {
        showFeedback(feedback, form.dataset.errorText || 'Error al enviar. Intenta de nuevo.', true);
      }
    } catch (err) {
      showFeedback(feedback, 'Ocurrió un error. Intenta nuevamente o escríbenos directo por WhatsApp.', true);
    } finally {
      if (submitBtn) submitBtn.removeAttribute('disabled');
      if (submitLabel) submitLabel.textContent = form.dataset.submitText || 'Enviar y continuar en WhatsApp';
    }
  });

  form.querySelectorAll('input, textarea, select').forEach(input => {
    input.addEventListener('focus', () => {
      const highlight = input.closest('.field')?.querySelector('.input-highlight');
      if (highlight) {
        highlight.style.width = '100%';
      }
    });
    input.addEventListener('blur', () => {
      const highlight = input.closest('.field')?.querySelector('.input-highlight');
      if (highlight) {
        const hasValue = input.value.trim().length > 0;
        highlight.style.width = hasValue ? '60%' : '0%';
      }
    });
  });
}

function showFeedback(el, message, isError) {
  if (!el) return;
  el.textContent = message;
  el.classList.remove('show', 'error');
  void el.offsetWidth;
  el.classList.add('show');
  if (isError) el.classList.add('error');
}

/* ═══ Smooth Anchor Scroll ═══ */
function initSmoothAnchors() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

/* ═══ Split Text Animation ═══ */
function initSplitText() {
  document.querySelectorAll('[data-split]').forEach(el => {
    const text = el.textContent;
    const words = text.split(' ');
    el.innerHTML = words.map(word =>
      `<span class="split-line"><span class="split-word">${word}</span></span>`
    ).join(' ');
    el.style.visibility = 'visible';
  });
}

/* ═══ Share Page Menu ═══ */
function initShareMenu() {
  const shareBtn = document.getElementById('share-btn');
  const shareModal = document.getElementById('share-modal');
  const closeBtn = document.getElementById('share-close-btn');
  const modalOverlay = shareModal ? shareModal.querySelector('.share-modal-overlay') : null;

  if (!shareModal) return;

  const currentUrl = window.location.href;

  // Set share link input value
  const linkInput = document.getElementById('share-link-input');
  if (linkInput) linkInput.value = currentUrl;

  // Generate QR Code dynamically
  const qrImg = document.getElementById('share-qr-img');
  if (qrImg) {
    qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(currentUrl)}`;
  }

  // Configure WhatsApp Share link
  const shareWa = document.getElementById('share-wa');
  if (shareWa) {
    shareWa.href = `https://wa.me/?text=${encodeURIComponent('Mira esta página: ' + currentUrl)}`;
  }

  // Configure Facebook Share link
  const shareFb = document.getElementById('share-fb');
  if (shareFb) {
    shareFb.href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(currentUrl)}`;
  }

  // Show Toast helper
  function showToast(message) {
    const toast = document.getElementById('share-toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  }

  // Copy Link action
  const copyBtn = document.getElementById('share-copy-btn');
  if (copyBtn && linkInput) {
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(currentUrl);
        copyBtn.classList.add('copied');
        showToast('Enlace copiado al portapapeles');
        setTimeout(() => {
          copyBtn.classList.remove('copied');
        }, 2000);
      } catch (err) {
        // Fallback for older browsers
        linkInput.select();
        document.execCommand('copy');
        copyBtn.classList.add('copied');
        showToast('Enlace copiado al portapapeles');
        setTimeout(() => {
          copyBtn.classList.remove('copied');
        }, 2000);
      }
    });
  }

  // Modal display toggles
  function openModal(e) {
    if (e) e.preventDefault();
    shareModal.classList.add('open');
    shareModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    shareModal.classList.remove('open');
    shareModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  if (shareBtn) shareBtn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (modalOverlay) modalOverlay.addEventListener('click', closeModal);

  // Handle ESC key to close modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && shareModal.classList.contains('open')) {
      closeModal();
    }
  });

  // Instagram and TikTok mock share behaviors (copy link and redirect to standard sites)
  const shareIg = document.getElementById('share-ig');
  if (shareIg) {
    shareIg.addEventListener('click', (e) => {
      e.preventDefault();
      navigator.clipboard.writeText(currentUrl).then(() => {
        showToast('Enlace copiado. ¡Pégalo en Instagram!');
        setTimeout(() => {
          window.open('https://www.instagram.com/', '_blank');
        }, 1200);
      });
    });
  }

  const shareTt = document.getElementById('share-tt');
  if (shareTt) {
    shareTt.addEventListener('click', (e) => {
      e.preventDefault();
      navigator.clipboard.writeText(currentUrl).then(() => {
        showToast('Enlace copiado. ¡Pégalo en TikTok!');
        setTimeout(() => {
          window.open('https://www.tiktok.com/', '_blank');
        }, 1200);
      });
    });
  }
}
