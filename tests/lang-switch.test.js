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
    documentElement: { setAttribute(name, value) { attributes[name] = value; } },
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
console.log('Saved language and live switching update page metadata and controls');
