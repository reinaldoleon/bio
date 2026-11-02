const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const code = fs.readFileSync('assets/js/analytics.js', 'utf8');
const websiteId = '01234567-89ab-cdef-0123-456789abcdef';

function run(hostname, id = websiteId, withArticle = false, pathname = '/bio/en/writing/example/') {
  const appended = [];
  const listeners = {};
  const listenerOptions = {};
  class TestElement {
    constructor(tagName, attributes = {}, href = '') {
      this.tagName = tagName;
      this.attributes = attributes;
      this.href = href;
    }
    closest() { return this; }
    getAttribute(name) { return this.attributes[name] || null; }
  }
  let currentScroll = 0;
  const prose = { offsetParent: {}, getBoundingClientRect: () => ({ top: 100 - currentScroll, bottom: 1100 - currentScroll }) };
  const article = {
    getAttribute: name => ({
      'data-analytics-article': 'example',
      'data-analytics-pillar': 'AI Governance',
      'data-analytics-title-en': 'Example title',
      'data-analytics-title-es': 'Título de ejemplo',
    })[name],
    querySelectorAll: () => [prose],
  };
  const document = {
    head: { appendChild: node => appended.push(node) },
    createElement: () => ({ setAttribute(name, value) { this[name] = value; } }),
    querySelector: () => withArticle ? article : null,
    documentElement: { getAttribute: name => name === 'data-route-lang' ? 'en' : 'en' },
    addEventListener: (name, callback, options) => { listeners[name] = callback; listenerOptions[name] = options; },
  };
  const events = [];
  const window = {
    location: { hostname, origin: `https://${hostname}`, pathname, href: `https://${hostname}${pathname}` },
    siteAnalyticsConfig: { websiteId: id },
    scrollY: 0,
    innerHeight: 400,
    addEventListener: (name, callback) => { listeners[name] = callback; },
    umami: { track: (name, data) => events.push({ name, data }) },
  };
  vm.runInNewContext(code, { window, document, URL, URLSearchParams, Element: TestElement });
  return {
    window, appended, listeners, listenerOptions, events,
    setScroll(value) { currentScroll = value; window.scrollY = value; },
    click(tagName, attributes, href) { listeners.click({ target: new TestElement(tagName, attributes, href) }); },
  };
}

assert.equal(run('localhost').appended.length, 0);
assert.equal(run('example.com').appended.length, 0);
assert.equal(run('reinaldoleon.github.io', websiteId, false, '/other/').appended.length, 0);
assert.equal(run('reinaldoleon.github.io', '').appended.length, 0);
const { window, appended } = run('reinaldoleon.github.io');
assert.equal(appended.length, 1);
assert.equal(appended[0].src, 'https://cloud.umami.is/script.js');
assert.equal(appended[0].async, true);
assert.equal(appended[0]['data-do-not-track'], 'true');
const cleaned = window.siteAnalyticsBeforeSend('event', {
  url: 'https://reinaldoleon.github.io/bio/en/writing/example/?utm_source=linkedin&utm_medium=social&utm_campaign=ai-agent-traceability&utm_content=post-v1&email=visitor%40example.com#private',
  referrer: 'https://www.linkedin.com/feed/?name=Visitor',
});
assert.equal(cleaned.url, '/bio/en/writing/example/?utm_source=linkedin&utm_medium=social&utm_campaign=ai-agent-traceability&utm_content=post-v1');
assert.equal(cleaned.referrer, 'https://www.linkedin.com/');
assert.equal(window.siteAnalyticsBeforeSend('event', { url: 'https://other.example/private' }), false);
assert.equal(window.siteAnalyticsBeforeSend('event', { url: '/bio/?utm_campaign=visitor@example.com' }).url, '/bio/');
const articleRun = run('reinaldoleon.github.io', websiteId, true);
articleRun.setScroll(300);
articleRun.window.umami = undefined;
articleRun.listeners.scroll();
assert.equal(articleRun.events.length, 0);
articleRun.window.umami = { track: (name, data) => articleRun.events.push({ name, data }) };
articleRun.listeners.scroll();
articleRun.setScroll(800);
articleRun.listeners.scroll();
articleRun.listeners.scroll();
assert.deepEqual(articleRun.events.map(event => event.name), ['article_50_percent', 'article_90_percent']);
assert.equal(articleRun.events[0].data.article_slug, 'example');
assert.equal(articleRun.events[0].data.language, 'en');
assert.equal(articleRun.events[0].data.pillar, 'AI Governance');
assert.equal(articleRun.events[0].data.title, 'Example title');
articleRun.click('BUTTON', { 'data-lang-set': 'es' });
assert.equal(articleRun.listenerOptions.click, true);
articleRun.click('A', {}, 'https://reinaldoleon.github.io/bio/#project-growthmesh');
articleRun.click('A', {}, 'https://www.linkedin.com/in/reinaldoleon/');
assert.deepEqual(articleRun.events.map(event => event.name), [
  'article_50_percent', 'article_90_percent', 'language_switch', 'project_click', 'linkedin_click',
]);
assert.equal(articleRun.events[2].data.to, 'es');
assert.equal(articleRun.events[3].data.project, 'project-growthmesh');
articleRun.window.umami.track = () => { throw new Error('tracker unavailable'); };
assert.doesNotThrow(() => articleRun.click('A', {}, 'https://www.linkedin.com/in/reinaldoleon/'));
console.log('Analytics gating, events and payload sanitization passed');
