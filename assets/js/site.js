(() => {
  const dialog = document.getElementById('performance-dialog');
  const player = document.getElementById('performance-player');
  const play = document.querySelector('[data-play-video]');
  const close = document.querySelector('[data-close-video]');
  if (!dialog || !player || !play || typeof dialog.showModal !== 'function') return;
  play.hidden = false;
  play.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = 'https://fast.wistia.net/embed/iframe/to40tf54hb?seo=false&videoFoam=true&autoplay=true';
    iframe.title = 'Flow & Green performing No Diggity';
    iframe.allow = 'autoplay; fullscreen'; iframe.allowFullscreen = true;
    player.replaceChildren(iframe); dialog.showModal();
  });
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const b = dialog.getBoundingClientRect();
    if (event.clientX < b.left || event.clientX > b.right || event.clientY < b.top || event.clientY > b.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => { player.replaceChildren(); play.focus(); });
})();
