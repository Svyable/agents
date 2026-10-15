'use strict';
const $ = selector => document.querySelector(selector);
let filter = 'All';
let packet = null;
let toastTimer;
function notify(message) {
  const toast = $('#toast');
  toast.textContent = message;
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.hidden = true; }, 4200);
}
async function copy(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const field = document.createElement('textarea');
      field.value = text; field.style.position = 'fixed'; field.style.opacity = '0';
      document.body.append(field); field.select();
      const success = document.execCommand('copy'); field.remove();
      if (!success) throw new Error('Clipboard unavailable');
    }
    notify('Copied. Ready for your next conversation.');
  } catch (_) { notify('Clipboard unavailable. Open the manifest or select the packet text to copy.'); }
}
const brief = `Sven Hardy Benson (GitHub: Svyable) is a builder, author, and electronic music producer. Explore public work in learning (mAIth), research (ScrolIQ, Frontier Lab, ProofBot), writing (Shelf, Bookself), human flourishing (Human Kind), and commerce (Opps, Agent Business, Agent for Hire). Music: Svyable; former duo PRFFTT & Svyable, with early Ellie Goulding and Taylor Swift bootlegs. Sommee began as a wine-learning app for his wife, inspired by his vintner brother-in-law.\n\nDiscover: https://svyable.github.io/agents/docs/agent-index.json\nRead rules: https://github.com/Svyable/agents/blob/main/AGENTS.md\nChoose work: https://github.com/Svyable/agents/tree/main/invitations\nRoute contributions to the target repository. Preserve evidence and upstream credit; do not infer benchmark results, endorsements, or delegated authority. Proposals require scope, acceptance criteria, sources, and an accountable principal.`;
$('#copy-brief').addEventListener('click', () => copy(brief));
$('#copy-manifest').addEventListener('click', () => copy('https://svyable.github.io/agents/docs/agent-index.json'));
$('#agent-toggle').addEventListener('click', event => {
  const on = event.currentTarget.getAttribute('aria-pressed') !== 'true';
  event.currentTarget.setAttribute('aria-pressed', String(on));
  document.body.classList.toggle('agent-active', on);
  event.currentTarget.textContent = on ? '◉ Human view' : '◉ Agent view';
  notify(on ? 'Agent view: contribution routes are now visible on every project.' : 'Human view restored.');
});
function applyFilters() {
  const query = $('#project-search').value.trim().toLocaleLowerCase();
  let count = 0;
  document.querySelectorAll('.project').forEach(card => {
    const visible = (filter === 'All' || card.dataset.category === filter) && card.textContent.toLocaleLowerCase().includes(query);
    card.hidden = !visible;
    if (visible) count++;
  });
  $('#results').textContent = `${count} public project${count === 1 ? '' : 's'} · ${filter === 'All' ? 'all disciplines' : filter.toLowerCase()}${query ? ' · matching your search' : ''}`;
  $('#empty').hidden = count > 0;
}
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
  filter = button.dataset.filter;
  document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  applyFilters();
}));
$('#project-search').addEventListener('input', applyFilters);
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !document.activeElement.isContentEditable) {
    event.preventDefault(); $('#project-search').focus(); $('#work').scrollIntoView({block:'start'});
  }
});
function packetMarkdown(data) {
  return `## Collaboration proposal\n\n- **Counterparty:** ${data.counterparty}\n- **Target:** ${data.target}\n- **Budget / intent:** ${data.budget}\n- **Authority / principal:** ${data.authority}\n\n### Proposed outcome\n${data.outcome}\n\n### Deliverable & acceptance criteria\n${data.acceptance_criteria}\n\n### Evidence\n${data.evidence}\n\n### Authority boundary\nProposal only. No order, payment, contract, or representation authority is created. Scope and commercial terms require explicit agreement.\n`;
}
$('#proposal-form').addEventListener('submit', event => {
  event.preventDefault();
  const raw = Object.fromEntries(new FormData(event.currentTarget));
  for (const key of ['counterparty', 'outcome', 'acceptance_criteria', 'evidence', 'authority']) {
    if (!raw[key]?.trim()) { notify('Please complete the required fields with more than whitespace.'); event.currentTarget.elements[key].focus(); return; }
  }
  packet = Object.fromEntries(Object.entries(raw).map(([key,value]) => [key, value.trim()]));
  packet.budget = packet.budget || 'To discuss; no spend authorized';
  packet.schema_version = '1.0.0';
  packet.generated_at = new Date().toISOString();
  packet.principal = 'Sven Hardy Benson';
  packet.status = 'proposal';
  packet.delegated_authority = 'none';
  const body = packetMarkdown(packet);
  $('#packet-preview').value = body;
  const url = new URL('https://github.com/Svyable/agents/issues/new');
  url.searchParams.set('title', `[Proposal] ${packet.outcome.slice(0, 85)}`);
  url.searchParams.set('body', body);
  // Large packets can exceed practical browser/hosting URL limits. Carry them by clipboard instead.
  $('#open-issue').href = url.href.length < 7000 ? url.href : 'https://github.com/Svyable/agents/issues/new';
  $('#open-issue').textContent = url.href.length < 7000 ? 'Continue on GitHub ↗' : 'Open GitHub & paste packet ↗';
  $('#packet-result').hidden = false;
  $('#packet-preview').focus();
});
$('#copy-packet').addEventListener('click', () => copy($('#packet-preview').value));
$('#download-packet').addEventListener('click', () => {
  if (!packet) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(packet, null, 2) + '\n'], {type:'application/json'}));
  const link = document.createElement('a'); link.href = url; link.download = 'sven-hardy-benson-collaboration-proposal.json';
  document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
