// Niners Faithful Europe, Provisorium: kleine Interaktionen ohne Bibliothek.
(function () {
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Spotlight auf Listen und Karten
  document.querySelectorAll('.spot').forEach(function (el) {
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      el.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  });

  // Parallaxe im Plakat
  var poster = document.querySelector('.poster');
  if (poster && !reduce) {
    poster.addEventListener('pointermove', function (e) {
      var r = poster.getBoundingClientRect();
      poster.style.setProperty('--px', (((e.clientX - r.left) / r.width - 0.5) * -24).toFixed(1) + 'px');
      poster.style.setProperty('--py', (((e.clientY - r.top) / r.height - 0.5) * -12).toFixed(1) + 'px');
    });
    poster.addEventListener('pointerleave', function () {
      poster.style.setProperty('--px', '0px');
      poster.style.setProperty('--py', '0px');
    });
  }

  // Playbook-Filter
  var pb = document.querySelector('[data-playbook]');
  if (pb) {
    var rows = Array.prototype.slice.call(pb.querySelectorAll('[data-row]'));
    var state = { fmt: 'all', rub: 'all', aut: 'all', q: '' };
    var params = new URLSearchParams(location.search);
    if (params.get('rub')) state.rub = params.get('rub');
    if (params.get('fmt')) state.fmt = params.get('fmt');
    var rubSel = pb.querySelector('#f-rub'), autSel = pb.querySelector('#f-aut'), q = pb.querySelector('#f-q');
    var count = pb.querySelector('[data-count]'), empty = pb.querySelector('[data-empty]');
    var fmtBtns = Array.prototype.slice.call(pb.querySelectorAll('[data-fmt]'));
    function apply() {
      var n = 0, needle = state.q.trim().toLowerCase();
      rows.forEach(function (r) {
        var ok = (state.fmt === 'all' || r.dataset.fmt === state.fmt) &&
          (state.rub === 'all' || r.dataset.rub === state.rub) &&
          (state.aut === 'all' || r.dataset.aut === state.aut) &&
          (!needle || r.dataset.text.indexOf(needle) >= 0);
        r.hidden = !ok; if (ok) n++;
      });
      fmtBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.fmt === state.fmt)); });
      count.textContent = n + ' ' + (n === 1 ? count.dataset.one : count.dataset.many);
      empty.hidden = n !== 0;
    }
    fmtBtns.forEach(function (b) { b.addEventListener('click', function () { state.fmt = b.dataset.fmt; apply(); }); });
    rubSel.value = state.rub;
    rubSel.addEventListener('change', function () { state.rub = rubSel.value; apply(); });
    autSel.addEventListener('change', function () { state.aut = autSel.value; apply(); });
    q.addEventListener('input', function () { state.q = q.value; apply(); });
    pb.querySelector('[data-reset]').addEventListener('click', function () {
      state = { fmt: 'all', rub: 'all', aut: 'all', q: '' }; rubSel.value = 'all'; autSel.value = 'all'; q.value = ''; apply(); q.focus();
    });
    apply();
  }

  // Line-up und Roster: Auswahl links, Profil rechts
  document.querySelectorAll('[data-picker]').forEach(function (picker) {
    var btns = Array.prototype.slice.call(picker.querySelectorAll('[data-pick]'));
    var panels = Array.prototype.slice.call(document.querySelectorAll('[data-panel]'));
    function show(id) {
      btns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.pick === id)); });
      panels.forEach(function (p) { p.classList.toggle('on', p.dataset.panel === id); });
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.pick); }); });
    show(btns[0].dataset.pick);
  });

  // Tryout-Formular
  var form = document.querySelector('[data-tryout]');
  if (form) {
    var done = document.querySelector('[data-done]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      [['f-name', function (v) { return v.trim().length > 0; }], ['f-url', function (v) { return /^https:\/\/\S+\.\S+/.test(v.trim()); }]].forEach(function (c) {
        var input = form.querySelector('#' + c[0]), field = input.closest('.field'), err = field.querySelector('.err');
        var valid = c[1](input.value);
        field.dataset.invalid = String(!valid); input.setAttribute('aria-invalid', String(!valid)); err.hidden = valid;
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (ok) {
        done.querySelector('[data-name]').textContent = form.querySelector('#f-name').value.trim();
        form.hidden = true; done.hidden = false; done.focus();
      }
    });
    done.querySelector('[data-again]').addEventListener('click', function () { form.reset(); done.hidden = true; form.hidden = false; form.querySelector('#f-name').focus(); });
  }

  // Link kopieren
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var label = b.textContent;
      navigator.clipboard.writeText(location.href).then(function () { b.textContent = b.dataset.copied; setTimeout(function () { b.textContent = label; }, 2000); }, function () {});
    });
  });
})();
