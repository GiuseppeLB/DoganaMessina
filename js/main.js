
document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('menu-btn');
  var nav = document.getElementById('site-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var aperto = nav.classList.toggle('aperto');
    btn.setAttribute('aria-expanded', aperto ? 'true' : 'false');
  });
});
