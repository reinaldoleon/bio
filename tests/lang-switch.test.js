const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function makePage() {
  const attributes = {};
  const title = {
    getAttribute: (name) => ({
      'data-title-en': 'English title',
      'data-title-es': 'Título español',
    })[name],
  };
  const description = {
    content: '',
    getAttribute: (name) => ({
      'data-description-en': 'English summary',
      'data-description-es': 'Resumen español',
    })[name],
    setAttribute(name, value) { this[name] = value; },
  };
  const buttons = ['en', 'es'].map(lang => ({
    lang,
    classes: new Set(),
    attributes: {},
    getAttribute: () => lang,
    setAttribute(name, value) { this.attributes[name] = value; },
    addEventListener(event, callback) { this.handlers ??= {}; this.handlers[event] = callback; },
    classList: {
      add() {},
      remove() {},
    },
  }));
  const document = {
    title: 'English title',
    documentElement: { getAttribute(name) { return attributes[name] ?? null; }, setAttribute(name, value) { attributes[name] = value; } },
    querySelector(selector) {
      if (selector === 'title') return title;
      if (selector === 'meta[name="description"]') return description;
      return null;
    },
    querySelectorAll(selector) {
      if (selector === '.lang-btn') return buttons;
      return [];
    },
    getElementById(id) {
      if (id === 'theme-toggle') return { addEventListener() {} };
      return null;
    },
    addEventListener(event, callback) {
      if (event === 'DOMContentLoaded') callback();
    },
  };
  const context = {
    document,
    localStorage: {
      getItem: (key) => key === 'lang' ? 'es' : null,
      setItem() {},
    },
    window: {
      matchMedia: () => ({ matches: true }),
      addEventListener() {},
    },
  };
  return { context, attributes, description, buttons };
}

const page = makePage();
vm.runInNewContext(fs.readFileSync('assets/js/lang-init.js', 'utf8'), page.context);
assert.equal(page.attributes['data-lang'], 'es');
assert.equal(page.context.document.title, 'Título español');
assert.equal(page.description.content, 'Resumen español');

vm.runInNewContext(fs.readFileSync('assets/js/main.js', 'utf8'), page.context);
assert.equal(page.attributes.lang, 'es');
assert.equal(page.buttons[1].attributes['aria-pressed'], 'true');
assert.equal(page.buttons[0].attributes['aria-pressed'], 'false');
page.buttons[0].handlers.click();
assert.equal(page.attributes.lang, 'en');
assert.equal(page.attributes['data-lang'], 'en');
assert.equal(page.context.document.title, 'English title');
assert.equal(page.description.content, 'English summary');
assert.equal(page.buttons[0].attributes['aria-pressed'], 'true');

let savedRouteLanguage;
const routePage = {
  document: {
    documentElement: { getAttribute: (name) => name === 'data-route-lang' ? 'es' : null },
    querySelector() { throw new Error('A localized route must not rewrite its metadata'); },
  },
  localStorage: {
    getItem: () => 'en',
    setItem: (key, value) => { if (key === 'lang') savedRouteLanguage = value; },
  },
};
vm.runInNewContext(fs.readFileSync('assets/js/lang-init.js', 'utf8'), routePage);
assert.equal(savedRouteLanguage, 'es');
const englishRoute = {
  getAttribute: () => 'en',
  addEventListener(event, callback) { if (event === 'click') this.click = callback; },
};
routePage.document.querySelectorAll = selector => selector === '[data-lang-route]' ? [englishRoute] : [];
routePage.document.getElementById = id => id === 'theme-toggle' ? { addEventListener() {} } : null;
routePage.document.addEventListener = (event, callback) => { if (event === 'DOMContentLoaded') callback(); };
routePage.document.documentElement.setAttribute = () => {};
routePage.localStorage.getItem = () => 'es';
routePage.window = { matchMedia: () => ({ matches: true }), addEventListener() {} };
vm.runInNewContext(fs.readFileSync('assets/js/main.js', 'utf8'), routePage);
englishRoute.click();
assert.equal(savedRouteLanguage, 'en');
console.log('Saved language and live switching update page metadata and controls');
