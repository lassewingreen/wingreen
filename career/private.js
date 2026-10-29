(() => {
  'use strict';
  const form = document.getElementById('unlock-form');
  const input = document.getElementById('application-password');
  const toggle = document.getElementById('password-toggle');
  const submit = document.getElementById('unlock-button');
  const status = document.getElementById('unlock-status');
  const locked = document.getElementById('lock-panel');
  const unlocked = document.getElementById('unlocked-panel');
  const frame = document.getElementById('application-frame');
  const download = document.getElementById('download-application');
  const heading = document.getElementById('document-title');
  let blobUrl = null;
  let attempt = 0;
  const bytes = text => Uint8Array.from(atob(text), char => char.charCodeAt(0));
  const clearDocument = () => {
    attempt += 1;
    frame.removeAttribute('srcdoc');
    frame.src = 'about:blank';
    heading.textContent = '';
    download.removeAttribute('href');
    download.removeAttribute('download');
    if (blobUrl) URL.revokeObjectURL(blobUrl);
    blobUrl = null;
    input.value = '';
    input.type = 'password';
    toggle.textContent = 'Show';
    toggle.setAttribute('aria-label', 'Show password');
    toggle.setAttribute('aria-pressed', 'false');
    submit.disabled = !supported;
    unlocked.hidden = true;
    locked.hidden = false;
    status.textContent = '';
  };
  const supported = window.crypto && window.crypto.subtle;
  if (!supported) {
    submit.disabled = true;
    status.textContent = 'This browser cannot unlock the document here. Open the HTTPS website, or use a modern browser on localhost.';
  }
  toggle.addEventListener('click', () => {
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    toggle.textContent = show ? 'Hide' : 'Show';
    toggle.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    toggle.setAttribute('aria-pressed', String(show));
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!supported || submit.disabled) return;
    let password = input.value;
    if (!password) return;
    const activeAttempt = ++attempt;
    submit.disabled = true;
    status.textContent = 'Opening your document…';
    try {
      const payload = JSON.parse(document.getElementById('encrypted-payload').textContent);
      if (payload.version !== 1 || payload.iterations !== 600000 || payload.kdf !== 'PBKDF2-SHA256' || payload.cipher !== 'AES-256-GCM') throw new Error('Invalid envelope');
      const salt = bytes(payload.salt);
      const iv = bytes(payload.iv);
      if (salt.length !== 16 || iv.length !== 12) throw new Error('Invalid envelope');
      const encoding = new TextEncoder();
      const material = await crypto.subtle.importKey('raw', encoding.encode(password), 'PBKDF2', false, ['deriveKey']);
      password = '';
      input.value = '';
      const key = await crypto.subtle.deriveKey({name:'PBKDF2',hash:'SHA-256',salt,iterations:payload.iterations},material,{name:'AES-GCM',length:256},false,['decrypt']);
      const plaintext = await crypto.subtle.decrypt({name:'AES-GCM',iv,additionalData:encoding.encode('wingreen-private-application-v1'),tagLength:128},key,bytes(payload.ciphertext));
      if (activeAttempt !== attempt) return;
      const data = JSON.parse(new TextDecoder().decode(plaintext));
      if (data.version !== 1 || typeof data.html !== 'string' || typeof data.title !== 'string' || data.pdf?.mime !== 'application/pdf' || typeof data.pdf.base64 !== 'string') throw new Error('Invalid document');
      const pdf = bytes(data.pdf.base64);
      blobUrl = URL.createObjectURL(new Blob([pdf], {type:'application/pdf'}));
      download.href = blobUrl;
      download.download = data.pdf.name || 'Application.pdf';
      heading.textContent = data.title;
      frame.removeAttribute('src');
      frame.srcdoc = data.html;
      locked.hidden = true;
      unlocked.hidden = false;
      status.textContent = '';
      input.type = 'password';
      toggle.textContent = 'Show';
      toggle.setAttribute('aria-label', 'Show password');
      toggle.setAttribute('aria-pressed', 'false');
      heading.focus();
      data.html = '';
      data.pdf.base64 = '';
      pdf.fill(0);
      new Uint8Array(plaintext).fill(0);
    } catch {
      if (activeAttempt !== attempt) return;
      status.textContent = 'That password did not open the document. Please check it and try again.';
      input.value = '';
      input.focus();
    } finally {
      password = '';
      if (activeAttempt === attempt) submit.disabled = false;
    }
  });
  document.getElementById('lock-button').addEventListener('click', () => {
    clearDocument();
    input.focus();
  });
  window.addEventListener('pagehide', clearDocument);
  window.addEventListener('pageshow', event => {
    if (event.persisted) clearDocument();
  });
})();
