(() => {
  'use strict';

  const hostname = window.location.hostname;
  const websiteId = window.siteAnalyticsConfig && window.siteAnalyticsConfig.websiteId;
  const production = hostname === 'reinaldoleon.github.io' && window.location.pathname.startsWith('/bio/');
  const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (!production || !uuid.test(websiteId || '')) return;

  const allowedCampaigns = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'];
  const campaignValue = /^[a-z0-9._~-]{1,80}$/i;

  // Umami's before-send hook is the final boundary: only campaign fields survive.
  window.siteAnalyticsBeforeSend = (_type, payload) => {
    if (!payload || typeof payload.url !== 'string') return false;
    try {
      const url = new URL(payload.url, window.location.origin);
      if (url.origin !== window.location.origin || !url.pathname.startsWith('/bio/')) return false;
      const safe = new URLSearchParams();
      for (const key of allowedCampaigns) {
        const value = url.searchParams.get(key);
        if (value && campaignValue.test(value)) safe.set(key, value);
      }
      payload.url = url.pathname + (safe.toString() ? `?${safe}` : '');
      if (payload.referrer) {
        const referrer = new URL(payload.referrer, window.location.origin);
        payload.referrer = /^https?:$/.test(referrer.protocol) ? referrer.origin + '/' : '';
      }
      return payload;
    } catch (_) {
      return false;
    }
  };

  const tracker = document.createElement('script');
  tracker.src = 'https://cloud.umami.is/script.js';
  tracker.async = true;
  tracker.setAttribute('data-website-id', websiteId);
  tracker.setAttribute('data-domains', 'reinaldoleon.github.io');
  tracker.setAttribute('data-exclude-hash', 'true');
  tracker.setAttribute('data-do-not-track', 'true');
  tracker.setAttribute('data-before-send', 'siteAnalyticsBeforeSend');
  document.head.appendChild(tracker);

  const article = document.querySelector('[data-analytics-article]');
  const language = () => {
    const route = document.documentElement.getAttribute('data-route-lang');
    return route === 'es' || route === 'en' ? route : document.documentElement.getAttribute('data-lang') === 'es' ? 'es' : 'en';
  };
  const articleData = () => article ? {
    language: language(),
    article_slug: article.getAttribute('data-analytics-article'),
    pillar: article.getAttribute('data-analytics-pillar'),
    title: article.getAttribute(`data-analytics-title-${language()}`) || article.getAttribute('data-analytics-title-en'),
  } : null;
  const track = (name, data) => {
    try {
      if (window.umami && typeof window.umami.track === 'function') {
        window.umami.track(name, data);
        return true;
      }
    } catch (_) {
      // Analytics must never interrupt navigation or rendering.
    }
    return false;
  };

  document.addEventListener('click', event => {
    const control = event.target instanceof Element ? event.target.closest('[data-lang-set], [data-lang-route], a[href]') : null;
    if (!control) return;
    const next = control.getAttribute('data-lang-set') || control.getAttribute('data-lang-route');
    if (next === 'es' || next === 'en') {
      if (next !== language()) track('language_switch', { from: language(), to: next, ...(articleData() || {}) });
      return;
    }
    if (control.tagName !== 'A') return;
    let destination;
    try { destination = new URL(control.href, window.location.href); } catch (_) { return; }
    if (destination.hostname === 'www.linkedin.com') {
      track('linkedin_click', { language: language(), ...(articleData() || {}) });
    } else if (destination.origin === window.location.origin &&
               (destination.hash === '#projects' || destination.hash.startsWith('#project-'))) {
      track('project_click', { language: language(), project: destination.hash.slice(1) });
    }
  }, true);

  if (!article) return;
  const milestones = [50, 90];
  const sent = new Set();
  const checkProgress = () => {
    const prose = [...article.querySelectorAll('.writing-prose')].find(element => element.offsetParent !== null);
    if (!prose) return;
    const top = prose.getBoundingClientRect().top + window.scrollY;
    const bottom = prose.getBoundingClientRect().bottom + window.scrollY;
    const viewport = window.scrollY + window.innerHeight;
    const progress = Math.min(100, Math.round((viewport - top) / (bottom - top) * 100));
    for (const milestone of milestones) {
      if (progress >= milestone && !sent.has(milestone) && track(`article_${milestone}_percent`, articleData())) {
        sent.add(milestone);
      }
    }
  };
  window.addEventListener('scroll', checkProgress, { passive: true });
  window.addEventListener('resize', checkProgress, { passive: true });
})();
