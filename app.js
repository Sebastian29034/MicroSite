// app.js (módulo)
const API = 'http://127.0.0.1:8000/peliculas'; // ajusta si tu endpoint usa otro path
const grid = document.getElementById('grid');
const status = document.getElementById('status');
const search = document.getElementById('search');
const reloadBtn = document.getElementById('reload');

let moviesCache = [];

// fetch y render
async function loadMovies() {
  status.textContent = 'Cargando películas...';
  grid.innerHTML = '';
  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error('Respuesta ' + res.status);
    const data = await res.json();
    moviesCache = data;
    renderGrid(data);
    status.textContent = `Mostrando ${data.length} películas`;
  } catch (err) {
    console.error(err);
    status.textContent = 'Error al cargar películas. Revisa la consola.';
    grid.innerHTML = `<div style="color:#ffb4b4;padding:10px;border-radius:8px;background:#3b1010">Error: ${escapeHtml(err.message)}</div>`;
  }
}

function renderGrid(list) {
  grid.innerHTML = '';
  if (!list || list.length === 0) {
    grid.innerHTML = '<div style="color:var(--muted)">No se encontraron películas.</div>';
    return;
  }

  for (const item of list) {
    const card = document.createElement('article');
    card.className = 'card';

    const thumb = document.createElement('div');
    thumb.className = 'thumb';
    const img = document.createElement('img');
    img.loading = 'lazy';
    img.src = item.image_url || '';
    img.alt = item.titulo || 'Poster';
    img.onerror = () => { img.src = placeholderImage(); };
    thumb.appendChild(img);

    const title = document.createElement('div');
    title.className = 'title';
    title.textContent = item.titulo || '';

    const desc = document.createElement('div');
    desc.className = 'desc';
    desc.textContent = item.descripcion || '';

    const actions = document.createElement('div');
    actions.className = 'actions';
    const detailsBtn = document.createElement('button');
    detailsBtn.className = 'small';
    detailsBtn.textContent = 'Ver detalle';
    detailsBtn.onclick = () => openDetail(item);

    const trailerBtn = document.createElement('button');
    trailerBtn.className = 'small';
    trailerBtn.textContent = 'Ver tráiler';
    trailerBtn.onclick = () => {
      const url = item.video_url || null;
      if (url) {
        const modal = document.getElementById('trailerModal');
        const frame = document.getElementById('trailerFrame');
        frame.src = url.replace("watch?v=", "embed/"); // convierte link de YouTube a embed
        modal.style.display = "block";
      } else {
        alert('No hay tráiler disponible para esta película.');
      }
    };

    // ---- SUGGEST BUTTON (agregado) ----
    const suggestBtn = document.createElement('button');
    suggestBtn.className = 'small';
    suggestBtn.textContent = 'Sugerencias';
    suggestBtn.onclick = () => {
      fetch(`http://127.0.0.1:8000/ai/recommendations/${encodeURIComponent(item.id)}?n=4`)
        .then(r => { if (!r.ok) throw new Error('Respuesta ' + r.status); return r.json(); })
        .then(data => {
          openRecommendationsModal(item, data || []);
        })
        .catch(err => {
          console.error('Error al pedir recomendaciones:', err);
          alert('No se pudieron cargar recomendaciones. Revisa la consola.');
        });
    };
    // ------------------------------------

    actions.appendChild(detailsBtn);
    actions.appendChild(trailerBtn);
    actions.appendChild(suggestBtn);


    card.appendChild(thumb);
    card.appendChild(title);
    card.appendChild(desc);
    card.appendChild(actions);

    grid.appendChild(card);
  }
}

function openDetail(item) {
  // Simple alert con descripción larga (puedes mejorar con modal)
  alert(`${item.titulo}\n\n${item.descripcion}`);
}

function placeholderImage() {
  return 'data:image/svg+xml;utf8,' + encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600"><rect width="100%" height="100%" fill="#07121b"/><text x="50%" y="50%" fill="#fff" font-family="Arial" font-size="20" text-anchor="middle">Sin imagen</text></svg>`
  );
}

function escapeHtml(s) {
  if (!s) return '';
  return String(s).replace(/[&<>"']/g, (m)=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

// eventos
reloadBtn.addEventListener('click', loadMovies);
search.addEventListener('input', (e) => {
  const q = (e.target.value || '').trim().toLowerCase();
  if (!q) renderGrid(moviesCache);
  else renderGrid(moviesCache.filter(m => (m.titulo||'').toLowerCase().includes(q)));
});

// Cerrar modal
document.getElementById('closeModal').onclick = () => {
  const modal = document.getElementById('trailerModal');
  const frame = document.getElementById('trailerFrame');
  frame.src = ""; // detener video al cerrar
  modal.style.display = "none";
};

// Si el usuario hace clic fuera del modal, se cierra
window.onclick = (e) => {
  const modal = document.getElementById('trailerModal');
  if (e.target === modal) {
    const frame = document.getElementById('trailerFrame');
    frame.src = "";
    modal.style.display = "none";
  }
};


// ----- Modal de recomendaciones (creado dinámicamente) -----
function createRecommendationsModalIfNeeded() {
  if (document.getElementById('recModal')) return;
  const modal = document.createElement('div');
  modal.id = 'recModal';
  Object.assign(modal.style, {
    display: 'none',
    position: 'fixed',
    inset: '0',
    background: 'rgba(0,0,0,0.75)',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1300,
  });

  const box = document.createElement('div');
  Object.assign(box.style, {
    width: 'min(720px, 96%)',
    maxHeight: '80%',
    overflowY: 'auto',
    background: '#0b0b0b',
    borderRadius: '10px',
    padding: '14px',
    boxShadow: '0 20px 60px rgba(0,0,0,0.7)',
    color: '#fff'
  });

  const close = document.createElement('button');
  close.textContent = 'Cerrar ✕';
  Object.assign(close.style, {
    float: 'right',
    background: '#fff',
    color: '#000',
    border: 'none',
    padding: '6px 10px',
    borderRadius: '6px',
    cursor: 'pointer',
    marginLeft: '8px'
  });
  close.onclick = () => { modal.style.display = 'none'; box.querySelector('.rec-body').innerHTML = ''; };

  const title = document.createElement('h3');
  title.textContent = 'Recomendaciones';
  title.style.marginTop = '0';
  title.style.marginBottom = '8px';

  const body = document.createElement('div');
  body.className = 'rec-body';

  box.appendChild(close);
  box.appendChild(title);
  box.appendChild(body);
  modal.appendChild(box);
  document.body.appendChild(modal);

  // cerrar al dar click fuera
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      body.innerHTML = '';
    }
  });
}

function openRecommendationsModal(item, recs) {
  createRecommendationsModalIfNeeded();
  const modal = document.getElementById('recModal');
  const body = modal.querySelector('.rec-body');
  body.innerHTML = ''; // limpiar

  // Cabecera con la película base
  const header = document.createElement('div');
  header.style.display = 'flex';
  header.style.gap = '12px';
  header.style.alignItems = 'center';
  header.innerHTML = `<div style="width:64px;height:96px;background:#111;border-radius:6px;overflow:hidden"><img src="${item.image_url||''}" style="width:100%;height:100%;object-fit:cover"></div>
                      <div style="flex:1"><strong style="font-size:1rem">${escapeHtml(item.titulo||'')}</strong><div style="color:var(--muted);font-size:0.9rem">${escapeHtml((item.descripcion||'').slice(0,140))}...</div></div>`;
  body.appendChild(header);

  if (!recs || recs.length === 0) {
    const p = document.createElement('p');
    p.textContent = 'No se encontraron recomendaciones.';
    p.style.marginTop = '12px';
    body.appendChild(p);
  } else {
    const list = document.createElement('div');
    list.style.marginTop = '12px';
    for (const r of recs) {
      const row = document.createElement('div');
      row.style.display = 'flex';
      row.style.gap = '10px';
      row.style.alignItems = 'center';
      row.style.padding = '8px 0';
      row.style.borderTop = '1px solid rgba(255,255,255,0.03)';

      const mv = document.createElement('div');
      mv.style.width = '60px';
      mv.style.height = '84px';
      mv.style.overflow = 'hidden';
      mv.style.borderRadius = '6px';
      mv.style.background = '#111';

      const movieObj = (moviesCache || []).find(m=>String(m.id) === String(r.id));
      const imgUrl = movieObj ? movieObj.image_url : '';
      mv.innerHTML = `<img src="${imgUrl||''}" style="width:100%;height:100%;object-fit:cover">`;

      const info = document.createElement('div');
      info.style.flex = '1';
      info.innerHTML = `<strong>${escapeHtml(r.titulo)}</strong><div style="color:var(--muted);font-size:0.9rem">Score: ${r.score}</div>`;

      const actions = document.createElement('div');
      actions.style.display = 'flex';
      actions.style.gap = '6px';
      const openBtn = document.createElement('button');
      openBtn.textContent = 'Ver';
      Object.assign(openBtn.style, {background: 'var(--primary)', color:'#000', border:'0', padding:'6px 8px', borderRadius:'6px', cursor:'pointer'});
      openBtn.onclick = () => {
        alert(`${r.titulo}`);
      };
      actions.appendChild(openBtn);

      row.appendChild(mv);
      row.appendChild(info);
      row.appendChild(actions);
      list.appendChild(row);
    }
    body.appendChild(list);
  }

  // mostrar modal
  modal.style.display = 'flex';
}

// auto-load
loadMovies();
