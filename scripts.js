document.addEventListener('DOMContentLoaded', () => {
  const videos = document.querySelectorAll('video.lazy-video');
  if (!videos.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const v = entry.target;
        v.src = v.dataset.src;
        v.load();
        observer.unobserve(v);
      }
    });
  }, { rootMargin: '200px' });

  videos.forEach(v => observer.observe(v));
});
