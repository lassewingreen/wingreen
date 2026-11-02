(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const hero = document.querySelector('.hero');
  const left = document.querySelector('[data-name-left]');
  const right = document.querySelector('[data-name-right]');
  const objects = document.querySelector('[data-objects]');
  const head = document.querySelector('[data-head]');
  const footer = document.querySelector('footer');
  const footerHead = document.querySelector('[data-footer-peek]');
  const fill = document.querySelector('[data-fill]');
  let words = [];
  if (fill) {
    const text = fill.textContent.trim();
    fill.setAttribute('aria-label', text);
    const fragment = document.createDocumentFragment();
    text.split(/\s+/).forEach((word, index) => {
      if (index) fragment.append(document.createTextNode(' '));
      const span = document.createElement('span');
      span.textContent = word; span.setAttribute('aria-hidden', 'true');
      fragment.append(span); words.push(span);
    });
    fill.replaceChildren(fragment);
  }
  let observer;
  const animate = element => {
    if (reduced.matches || !element.animate) return;
    const peek = element.querySelector('[data-peek]');
    element.animate([{opacity:0,translate:'0 36px'},{opacity:1,translate:'0 0'}],{duration:1000,easing:'cubic-bezier(.22,1,.36,1)'});
    if (peek) peek.animate([{opacity:0,transform:'translateY(70%) rotate(-24deg) scale(.4)'},{opacity:1,transform:'translateY(0) rotate(-10deg) scale(1)'}],{duration:1500,delay:300,fill:'backwards',easing:'cubic-bezier(.22,1,.36,1)'});
  };
  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) {animate(entry.target);observer.unobserve(entry.target);} });
    },{threshold:.08,rootMargin:'0px 0px -7% 0px'});
    document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
  }
  const clamp = n => Math.max(0,Math.min(1,n));
  let requested = false;
  function update() {
    requested = false;
    if (reduced.matches) return;
    if (innerWidth >= 768 && hero) {
      const progress = clamp(-hero.getBoundingClientRect().top / hero.offsetHeight);
      left.style.transform = `translateX(${-progress*28}%)`;
      right.style.transform = `translateX(${progress*22}%)`;
      if (objects) objects.style.transform = `translateY(${-progress*14}%) scale(${1+progress*.08})`;
      head.style.transform = `translateY(${progress*12}%)`;
    } else [left,right,objects,head].forEach(el=>{if(el)el.style.transform='';});
    if(fill){const box=fill.getBoundingClientRect();const progress=clamp((innerHeight*.87-box.top)/(box.height+innerHeight*.35));words.forEach((word,i)=>{word.style.opacity=String(.22+.78*clamp(progress*words.length-i));});}
    if(footerHead){const box=footer.getBoundingClientRect();const progress=clamp((innerHeight-box.top)/(Math.min(box.height,innerHeight)));footerHead.style.transform=`translateY(${(1-progress)*70}%) rotate(${12+(1-progress)*16}deg)`;}
  }
  function requestUpdate(){if(!requested){requested=true;requestAnimationFrame(update);}}
  addEventListener('scroll',requestUpdate,{passive:true});addEventListener('resize',requestUpdate,{passive:true});
  document.fonts.ready.then(requestUpdate);
  const skipEntrance=()=>{hero.getAnimations({subtree:true}).forEach(animation=>{if(animation instanceof CSSAnimation)animation.finish();});};
  ['wheel','touchstart','keydown'].forEach(event=>addEventListener(event,skipEntrance,{passive:true,once:true}));
  reduced.addEventListener('change',()=>{
    if(reduced.matches){document.getAnimations().forEach(a=>a.finish());[left,right,objects,head,footerHead].forEach(el=>{if(el)el.style.transform='';});words.forEach(word=>word.style.opacity='1');}
    else requestUpdate();
  });
  requestUpdate();
  // Load the performance only when requested; restore focus to its opener.
  const dialog = document.getElementById('performance-dialog');
  const player = document.getElementById('performance-player');
  let opener;
  document.querySelectorAll('[data-play-video]').forEach(button=>button.addEventListener('click',()=>{
    if(typeof dialog.showModal!=='function'){window.open('https://fast.wistia.net/embed/iframe/to40tf54hb','_blank','noopener');return;}
    opener=button;const iframe=document.createElement('iframe');
    iframe.src='https://fast.wistia.net/embed/iframe/to40tf54hb?seo=false&videoFoam=true&autoplay=true';
    iframe.title=document.documentElement.lang==='da'?'Flow & Green spiller No Diggity':'Flow & Green performing No Diggity';
    iframe.allow='autoplay; fullscreen';iframe.allowFullscreen=true;player.replaceChildren(iframe);dialog.showModal();
  }));
  document.querySelector('[data-close-video]').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const box=dialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)dialog.close();});
  dialog.addEventListener('close',()=>{player.replaceChildren();opener?.focus();});
})();
