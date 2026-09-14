
/* Legge il file JSON di contenuto della pagina (gestito da Decap CMS
   nel pannello /admin) e lo inserisce nello scheletro HTML statico. */

function md(testo){
  if(!testo) return '';
  if(typeof marked !== 'undefined') return marked.parse(testo);
  return '<p>' + testo + '</p>';
}

function immagineHtml(src, alt){
  if(src){
    return '<img src="' + src + '" alt="' + (alt || '') + '" style="width:100%;border:1px solid var(--linea);border-radius:2px;margin-bottom:1rem;">';
  }
  return '<div class="placeholder-img">Nessuna immagine caricata</div>';
}

var TEMPLATES = {
  home: function(d){
    return '<p class="eyebrow">Esposizione permanente</p>' +
           '<h1>' + (d.title || '') + '</h1>' +
           md(d.intro);
  },
  page: function(d){
    return '<p class="eyebrow">Storia</p>' +
           '<h1>' + (d.title || '') + '</h1>' +
           immagineHtml(d.image, d.title) +
           md(d.body);
  },
  section: function(d){
    return '<p class="eyebrow">Esposizione</p>' +
           '<h1>' + (d.title || '') + '</h1>' +
           md(d.intro);
  },
  item: function(d){
    var html = '<h1>' + (d.title || '') + '</h1>' + immagineHtml(d.image, d.title) + md(d.description);
    html += '<dl class="campi-scheda">';
    html += '<dt>Provenienza / periodo</dt><dd>' + (d.provenienza || '&nbsp;') + '</dd>';
    html += '<dt>Note tecniche</dt><dd>' + md(d.note) + '</dd>';
    html += '</dl>';
    return html;
  }
};

document.addEventListener('DOMContentLoaded', function(){
  if (typeof PAGE_TYPE === 'undefined' || typeof CONTENT_URL === 'undefined') return;
  var target = document.getElementById('dyn-' + PAGE_TYPE);
  if(!target) return;
  fetch(CONTENT_URL)
    .then(function(r){ if(!r.ok) throw new Error('non trovato'); return r.json(); })
    .then(function(data){ target.innerHTML = TEMPLATES[PAGE_TYPE](data); })
    .catch(function(){ target.innerHTML = '<p class="provvisorio">Contenuto non ancora disponibile.</p>'; });
});
