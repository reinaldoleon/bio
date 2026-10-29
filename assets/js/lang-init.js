// Apply the saved language before the page's styles and content are painted.
(() => {
  try {
    const routeLang = document.documentElement.getAttribute('data-route-lang');
    if (routeLang === 'en' || routeLang === 'es') {
      localStorage.setItem('lang', routeLang);
      return;
    }
    const lang = localStorage.getItem('lang');
    if (lang !== 'en' && lang !== 'es') return;
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.setAttribute('lang', lang);

    const title = document.querySelector('title');
    if (title && title.getAttribute('data-title-' + lang)) {
      document.title = title.getAttribute('data-title-' + lang);
    }
    const description = document.querySelector('meta[name="description"]');
    if (description && description.getAttribute('data-description-' + lang)) {
      description.setAttribute('content', description.getAttribute('data-description-' + lang));
    }
  } catch (_) {
    // The static page still renders in English if storage is unavailable.
  }
})();
