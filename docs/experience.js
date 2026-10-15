'use strict';
(() => {
  const one = selector => document.querySelector(selector);
  const all = selector => [...document.querySelectorAll(selector)];
  const body = document.body;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const motionButton = one('#motion-toggle');
  const signals = {
    all: ['One human. A constellation of things to explore.', '#work'],
    research: ['Follow the question. Inspect the evidence.', '#work', 'Research'],
    learning: ['Make difficult thinking a little more addictive.', '#project-maith', 'Learning'],
    music: ['Before the agents, there was the remix.', '#music'],
    writing: ['Some ideas need a whole book.', '#project-shelf', 'Writing'],
    commerce: ['Turn a useful idea into a concrete proposal.', '#connect']
  };
  one('.signal-dock').hidden = false;
  one('.scene-toolbar').hidden = false;
  all('[data-scene]').forEach(button => button.addEventListener('click', () => {
    body.dataset.scene = button.dataset.scene;
    all('[data-scene]').filter(item => item.tagName === 'BUTTON').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  }));
  function setMotion(paused) {
    body.classList.toggle('motion-paused', paused);
    motionButton.setAttribute('aria-pressed', String(paused));
    motionButton.disabled = reducedMotion.matches;
    motionButton.textContent = reducedMotion.matches ? 'Reduced motion enabled' : paused ? 'Resume ambient motion ▷' : 'Pause ambient motion Ⅱ';
  }
  setMotion(reducedMotion.matches);
  motionButton.addEventListener('click', () => setMotion(motionButton.getAttribute('aria-pressed') !== 'true'));
  reducedMotion.addEventListener('change', event => setMotion(event.matches));
  all('.signal-buttons [data-signal]').forEach(button => button.addEventListener('click', () => {
    const [description, href, category] = signals[button.dataset.signal];
    one('.orbit').dataset.signal = button.dataset.signal;
    one('#signal-description').textContent = description;
    one('#signal-destination').href = href;
    all('.signal-buttons [data-signal]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    // Clear old search so the selected workstream is always a valid destination.
    one('#project-search').value = '';
    const filterButton = all('[data-filter]').find(item => item.dataset.filter === (category || 'All'));
    filterButton.click();
  }));

  const dialog = one('#project-dialog');
  let selected = null;
  let previous = null;
  let opener = null;
  const cards = all('.project');
  const previews = all('.quick-look');
  function openProject(card, trigger) {
    selected = card;
    previous = card.id;
    opener = trigger;
    one('#dialog-category').textContent = card.dataset.category + ' / PUBLIC PROJECT';
    one('#dialog-project-name').textContent = card.querySelector('h3').textContent;
    one('#dialog-tagline').textContent = card.querySelector('.tagline').textContent;
    one('#dialog-description').textContent = card.querySelector('.description').textContent;
    one('#dialog-ask').textContent = card.querySelector('.agent-ask').textContent.trim();
    one('#dialog-repo').href = card.querySelector('h3 a').href;
    one('#dialog-art').textContent = card.querySelector('.project-emblem').textContent;
    one('#dialog-art').dataset.category = card.dataset.category;
    dialog.showModal();
  }
  // Keep direct repository links as the no-script / older-browser fallback.
  if (typeof dialog.showModal === 'function') {
    previews.forEach(button => {
      button.hidden = false;
      button.addEventListener('click', () => openProject(button.closest('.project'), button));
    });
    one('#surprise-me').hidden = false;
    one('#surprise-me').addEventListener('click', event => {
      const candidates = cards.filter(card => card.id !== previous);
      openProject(candidates[Math.floor(Math.random() * candidates.length)], event.currentTarget);
    });
    one('#close-project-dialog').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }});
    dialog.addEventListener('close', () => { if (opener?.isConnected) opener.focus({preventScroll:true}); });
    one('#dialog-propose').addEventListener('click', () => {
      if (!selected) return;
      const repo = selected.querySelector('h3 a').href.split('github.com/')[1];
      const form = one('#proposal-form');
      form.elements.target.value = repo;
      dialog.close();
      form.scrollIntoView({block:'center', behavior: reducedMotion.matches ? 'instant' : 'smooth'});
      form.elements.counterparty.focus({preventScroll:true});
    });
  }
})();
