/* Legal Marketing Firm — shared site script. No dependencies. */
(function () {
  'use strict';
  var LEADS_URL = 'https://script.google.com/macros/s/AKfycbxIeH_e8a2QopGls5BImXP40cvBwWxYudqxurniejeyus8HAhafUnjbo3FwffopECil/exec';
  var EMAIL = 'hello@legalmarketingfirm.net';
  var GOALS = {
    maintain: { name: 'Maintain Business', pct: 5 },
    moderate: { name: 'Moderate Growth', pct: 10 },
    accelerated: { name: 'Accelerated Growth', pct: 15 },
    expansion: { name: 'Market Expansion', pct: 25 }
  };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce) document.documentElement.classList.add('motion');
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function track(name, params) { try { if (typeof window.gtag === 'function') window.gtag('event', name, params || {}); } catch (e) {} }
  function store(k, v) { try { if (v === undefined) return window.localStorage.getItem(k); window.localStorage.setItem(k, v); } catch (e) { return null; } }
  function uid() { return 'lmf-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10); }
  function fmt(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function parseMoney(v) { v = String(v || '').replace(/[$,\s]/g, ''); if (v === '') return null; return /^\d+(\.\d+)?$/.test(v) ? parseFloat(v) : NaN; }

  /* ---------- old single-page hash links → real URLs ---------- */
  var HASH = { '#services': '/services/', '#ai-search': '/law-firm-ai-search-optimization/', '#results': '/results/', '#contact': '/contact/' };
  if (location.pathname === '/' && HASH[location.hash]) location.replace(HASH[location.hash]);

  /* ---------- attribution (first touch + UTMs) ---------- */
  (function () {
    var q = new URLSearchParams(location.search);
    if (!store('lmf_first_landing')) {
      store('lmf_first_landing', location.href.split('#')[0]);
      store('lmf_referrer', document.referrer || '');
    }
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) { if (q.get(k)) store('lmf_' + k, q.get(k)); });
  })();
  function attribution(ctx) {
    var a = {
      originating_page_url: location.href.split('#')[0].split('?')[0],
      page_type: ctx.pageType || document.body.getAttribute('data-page-type') || '',
      page_market: ctx.market || document.body.getAttribute('data-market') || '',
      page_practice: ctx.practice || document.body.getAttribute('data-practice') || '',
      first_landing_page: store('lmf_first_landing') || '',
      referrer: store('lmf_referrer') || ''
    };
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) { a[k] = store('lmf_' + k) || ''; });
    return a;
  }
  function post(payload) {
    var body = new URLSearchParams();
    Object.keys(payload).forEach(function (k) { body.set(k, payload[k] === null || payload[k] === undefined ? '' : String(payload[k])); });
    return fetch(LEADS_URL, { method: 'POST', body: body }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j || !j.ok) throw new Error((j && j.error) || 'not ok');
      return j;
    });
  }

  /* ---------- header menu ---------- */
  var burger = $('.hdr-burger'), mnav = $('#mnav');
  if (burger && mnav) burger.addEventListener('click', function () {
    var open = mnav.hidden; mnav.hidden = !open; burger.setAttribute('aria-expanded', String(open));
    burger.querySelector('use').setAttribute('href', open ? '#i-x' : '#i-menu');
  });

  /* ---------- count-up ---------- */
  var io = ('IntersectionObserver' in window && !reduce) ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); countUp(e.target); } });
  }, { threshold: .2 }) : null;
  function countUp(el) {
    var v = el.getAttribute('data-count'), m = /^([^\d]*)([\d.]+)(.*)$/.exec(v);
    if (!m) { el.textContent = v; return; }
    var target = parseFloat(m[2]), dec = (m[2].split('.')[1] || '').length, t0 = null;
    function step(t) { t0 = t0 || t; var p = Math.min(1, (t - t0) / 1400); el.textContent = m[1] + (target * (1 - Math.pow(1 - p, 3))).toFixed(dec) + m[3]; if (p < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  if (io) $$('[data-count]').forEach(function (el) {
    var m = /^([^\d]*)([\d.]+)(.*)$/.exec(el.getAttribute('data-count'));
    if (m) { el.setAttribute('aria-label', el.getAttribute('data-count')); el.textContent = m[1] + (0).toFixed((m[2].split('.')[1] || '').length) + m[3]; }
    io.observe(el);
  });

  /* ---------- accordions ---------- */
  $$('.acc').forEach(function (acc) {
    $$('.acc-item', acc).forEach(function (it) {
      it.querySelector('.acc-q').addEventListener('click', function () {
        var open = !it.classList.contains('open');
        $$('.acc-item', acc).forEach(function (o) { o.classList.remove('open'); o.querySelector('.acc-a').hidden = true; o.querySelector('.acc-q').setAttribute('aria-expanded', 'false'); });
        if (open) { it.classList.add('open'); it.querySelector('.acc-a').hidden = false; it.querySelector('.acc-q').setAttribute('aria-expanded', 'true'); }
      });
    });
  });

  /* ---------- channel board (services) ---------- */
  $$('.svc').forEach(function (svc) {
    var mq = window.matchMedia('(min-width:900px)'), items = $$('.svc-item', svc), sel = +(svc.getAttribute('data-sel') || 0);
    function render() {
      var desk = mq.matches;
      items.forEach(function (it, i) {
        var on = i === sel; it.classList.toggle('on', on);
        it.querySelector('.svc-btn').setAttribute('aria-expanded', String(on));
        it.querySelector('.svc-chev use').setAttribute('href', desk ? '#i-arrow-right' : (on ? '#i-chevron-up' : '#i-chevron-down'));
      });
      var cur = items[sel < 0 ? 0 : sel], d = $('.svc-detail', svc);
      $('.svc-detail-icon svg', d).innerHTML = cur.querySelector('template.svc-icon').content.querySelector('svg').innerHTML;
      $('.svc-detail-n', d).textContent = 'CHANNEL ' + cur.querySelector('.svc-n').textContent + ' / ' + String(items.length).padStart(2, '0');
      $('.svc-detail-t', d).textContent = cur.querySelector('.svc-t').textContent;
      $('.svc-detail-b', d).textContent = cur.querySelector('.svc-inline p').textContent;
      $('.svc-detail-tags', d).innerHTML = cur.querySelector('.svc-inline .tags').innerHTML;
      var link = cur.querySelector('.svc-inline a.textlink'), dl = $('.svc-detail-link', d);
      if (dl) { dl.hidden = !link; if (link) { dl.href = link.href; dl.firstChild.textContent = link.textContent.trim() + ' '; } }
    }
    items.forEach(function (it, i) { it.querySelector('.svc-btn').addEventListener('click', function () { sel = (!mq.matches && sel === i) ? -1 : i; render(); }); });
    (mq.addEventListener ? mq.addEventListener('change', render) : mq.addListener(render));
    render();
  });

  /* ---------- 3-step contact flow ---------- */
  var flow = $('#contact-flow');
  if (flow) (function () {
    var step = 0, answers = { practice: '', budget: '' }, f = $('#lead-form', flow);
    function render() {
      $$('.c-step', flow).forEach(function (s) { s.hidden = +s.getAttribute('data-step') !== step; });
      $$('.c-progress span', flow).forEach(function (s, i) { s.classList.toggle('on', i <= step); });
      $('.c-step-label', flow).textContent = step < 3 ? 'Question ' + (step + 1) + ' of 3' : 'Done';
      $('.c-back', flow).hidden = !(step > 0 && step < 3);
    }
    $$('.chips', flow).forEach(function (group) {
      var field = group.getAttribute('data-field');
      $$('.chip', group).forEach(function (c) {
        c.addEventListener('click', function () {
          $$('.chip', group).forEach(function (o) { o.classList.remove('on'); }); c.classList.add('on');
          answers[field] = c.textContent.trim(); step = field === 'practice' ? 1 : 2; render();
          track('lead_step', { step: field });
          var nx = $('.c-step:not([hidden]) .chip, .c-step:not([hidden]) input:not(.hp)', flow); if (nx) nx.focus({ preventScroll: true });
        });
      });
    });
    $('.c-back', flow).addEventListener('click', function (e) { e.preventDefault(); if (step > 0) step--; render(); });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = { name: f.name.value.trim(), firm: f.firm.value.trim(), email: f.email.value.trim(), phone: f.phone.value.trim() };
      var bad = false, er = $('.form-err', f);
      [['name', !d.name], ['firm', !d.firm], ['email', !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)]].forEach(function (x) { f[x[0]].setAttribute('aria-invalid', String(x[1])); if (x[1]) bad = true; });
      er.textContent = 'Please add your name, firm, and a valid email.'; er.hidden = !bad;
      if (bad) return;
      var btn = f.querySelector('button[type="submit"]'); btn.disabled = true;
      var a = attribution({});
      post({ form: 'Strategy request', name: d.name, firm: d.firm, email: d.email, phone: d.phone, practice: answers.practice, budget: answers.budget,
        page: a.originating_page_url, first_landing_page: a.first_landing_page, referrer: a.referrer, utm_source: a.utm_source, utm_medium: a.utm_medium, utm_campaign: a.utm_campaign, hp: f.hp.value })
        .then(function () { track('generate_lead', { form_name: 'strategy_request', page_type: a.page_type }); f.reset(); step = 3; render(); })
        .catch(function () { er.innerHTML = 'We couldn’t send that. Please try again, or email <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>.'; er.hidden = false; })
        .then(function () { btn.disabled = false; });
    });
    render();
  })();

  /* ---------- generic lead forms (audit, tools, research updates) ---------- */
  $$('form[data-lead-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = false;
      $$('[required]', f).forEach(function (el) {
        var v = el.type === 'checkbox' ? el.checked : el.value.trim();
        var invalid = !v || (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim()));
        el.setAttribute('aria-invalid', String(!!invalid)); if (invalid) bad = true;
      });
      var st = $('.status', f), ok = $('.ok', f);
      if (bad) { st.className = 'status err'; st.textContent = 'Please complete the required fields.'; st.hidden = false; var first = $('[aria-invalid=true]', f); if (first) first.focus(); return; }
      st.hidden = true;
      var btn = f.querySelector('button[type="submit"]'); btn.disabled = true;
      var data = { form: f.getAttribute('data-lead-form') };
      $$('input,select,textarea', f).forEach(function (el) { if (!el.name) return; data[el.name] = el.type === 'checkbox' ? (el.checked ? 'yes' : 'no') : el.value.trim(); });
      var a = attribution({}); Object.keys(a).forEach(function (k) { data[k] = a[k]; }); data.page = a.originating_page_url;
      post(data).then(function () {
        track('generate_lead', { form_name: f.getAttribute('data-lead-form').toLowerCase().replace(/\W+/g, '_'), page_type: a.page_type });
        $$('.form-body', f).forEach(function (b) { b.hidden = true; }); ok.hidden = false; ok.focus && ok.focus();
      }).catch(function () {
        st.className = 'status err'; st.innerHTML = 'We couldn’t send that. Your answers are still here — please try again, or email <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>.'; st.hidden = false;
      }).then(function () { btn.disabled = false; });
    });
  });

  /* ---------- money inputs: format as you type ---------- */
  $$('input[data-money]').forEach(function (el) {
    el.addEventListener('blur', function () { var n = parseMoney(el.value); if (n !== null && !isNaN(n)) el.value = Math.round(n).toLocaleString('en-US'); });
  });

  /* ---------- law firm marketing budget calculator ---------- */
  $$('.calc[data-calc]').forEach(function (calc) {
    var id = calc.id, ctx = { pageType: calc.getAttribute('data-page-type'), market: calc.getAttribute('data-market'), practice: calc.getAttribute('data-practice'), placement: calc.getAttribute('data-placement') };
    var form = $('.calc-form', calc), gate = $('.gate', calc), gform = $('.gate-form', calc), res = $('.results-panel', calc);
    var started = false, inputs = null, result = null, sid = null;
    function ga(name, extra) { var p = { tool_id: 'budget_calculator', page_type: ctx.pageType || '', placement: ctx.placement || '' }; if (extra) for (var k in extra) p[k] = extra[k]; track(name, p); }
    form.addEventListener('input', function () { if (!started) { started = true; ga('marketing_calculator_start'); } });
    $$('input[name="goal"]', form).forEach(function (r) { r.addEventListener('change', function () { ga('growth_objective_selected', { growth_objective: r.value }); }); });
    function compute(i) {
      var g = GOALS[i.goal], annual = i.revenue * g.pct / 100, monthly = annual / 12, o = { goal: i.goal, goalName: g.name, pct: g.pct, annual: annual, monthly: monthly, revenue: i.revenue, current: i.current };
      if (i.current !== null) {
        o.curAnnual = i.current * 12; o.curPct = o.curAnnual / i.revenue * 100;
        o.gapMonthly = Math.max(0, monthly - i.current); o.gapAnnual = Math.max(0, annual - o.curAnnual);
        var a = Math.round(i.current), b = Math.round(monthly);
        o.position = a < b ? 'below' : (a === b ? 'at' : 'above');
      }
      return o;
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var rev = form.revenue, cur = form.current, revN = parseMoney(rev.value), curN = parseMoney(cur.value), ok = true;
      var revBad = revN === null || isNaN(revN) || revN <= 0, curBad = isNaN(curN) || (curN !== null && curN < 0);
      rev.setAttribute('aria-invalid', String(revBad)); cur.setAttribute('aria-invalid', String(curBad));
      $('#' + id + '-rev-err').hidden = !revBad; $('#' + id + '-cur-err').hidden = !curBad;
      if (revBad) { ok = false; rev.focus(); } else if (curBad) { ok = false; cur.focus(); }
      if (!ok) return;
      var goal = ($('input[name="goal"]:checked', form) || {}).value || 'moderate';
      inputs = { revenue: revN, current: curN, goal: goal };
      result = compute(inputs);
      if (!sid) sid = uid();
      if (res.hidden === false && result) { showResults(); return; }
      gate.hidden = false; ga('marketing_calculator_gate_view');
      var h = $('h3', gate); h.setAttribute('tabindex', '-1'); h.focus();
    });
    gform.addEventListener('submit', function (e) {
      e.preventDefault();
      var st = $('.status', gform), bad = false;
      $$('[required]', gform).forEach(function (el) {
        var v = el.value.trim(), invalid = !v || (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v));
        el.setAttribute('aria-invalid', String(invalid)); if (invalid) bad = true;
      });
      if (bad) { st.className = 'status err'; st.textContent = 'Please complete the required fields.'; st.hidden = false; $('[aria-invalid=true]', gform).focus(); return; }
      st.hidden = true;
      var btn = $('button[type="submit"]', gform); btn.disabled = true; btn.setAttribute('aria-busy', 'true');
      var r = result, g = gform, a = attribution(ctx), cs = r.current !== null;
      var payload = {
        tool_id: 'law-firm-marketing-budget-calculator', form: 'Budget calculator', submission_id: sid,
        first_name: g.first_name.value.trim(), last_name: g.last_name.value.trim(), firm_name: g.firm_name.value.trim(), email: g.email.value.trim(),
        phone: g.phone.value.trim(), website: g.site.value.trim(), practice_area: g.practice_area.value, city: g.city.value.trim(), state: g.state.value.trim(),
        annual_revenue: r.revenue, current_monthly_spend: cs ? r.current : '', growth_objective: r.goalName,
        consent_status: g.consent.checked ? 'opted_in' : 'not_opted_in', hp: g.hp.value
      };
      Object.keys(a).forEach(function (k) { payload[k] = a[k]; });
      post(payload).then(function () {
        ga('marketing_calculator_lead'); gate.hidden = true; showResults(); ga('marketing_calculator_complete');
      }).catch(function () {
        st.className = 'status err'; st.innerHTML = 'We couldn’t save your request, so your results aren’t unlocked yet. Your answers are still here — please try again. If it keeps failing, email <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>.'; st.hidden = false;
      }).then(function () { btn.disabled = false; btn.removeAttribute('aria-busy'); });
    });
    function showResults() {
      var r = result;
      $('[data-r=monthly]', res).textContent = fmt(r.monthly);
      $('[data-r=annual]', res).textContent = fmt(r.annual);
      $('[data-r=goal]', res).textContent = r.goalName + ' · ' + r.pct + '% of revenue';
      var cmp = $('.r-compare', res);
      if (r.current !== null) {
        cmp.hidden = false;
        $('[data-r=cur-m]', res).textContent = fmt(r.current);
        $('[data-r=cur-a]', res).textContent = fmt(r.curAnnual);
        $('[data-r=cur-pct]', res).textContent = (Math.round(r.curPct * 10) / 10) + '%';
        $('[data-r=gap-m]', res).textContent = fmt(r.gapMonthly);
        $('[data-r=gap-a]', res).textContent = fmt(r.gapAnnual);
        var max = Math.max(r.current, r.monthly) || 1;
        $('[data-r=bar-cur]', res).style.setProperty('--w', (r.current / max * 100).toFixed(1) + '%');
        $('[data-r=bar-rec]', res).style.setProperty('--w', (r.monthly / max * 100).toFixed(1) + '%');
        $('[data-r=bar-cur-v]', res).textContent = fmt(r.current) + '/mo';
        $('[data-r=bar-rec-v]', res).textContent = fmt(r.monthly) + '/mo';
        var msg = { below: 'Your current marketing investment is below our recommended level for your selected growth objective.', at: 'Your investment aligns with our recommendation. Focus on allocating it effectively.', above: 'Your investment exceeds our recommendation. Evaluate acquisition efficiency and returns before increasing spend.' };
        $('.r-msg', res).textContent = msg[r.position];
      } else { cmp.hidden = true; }
      res.hidden = false;
      var h = $('h3', res); h.setAttribute('tabindex', '-1'); h.focus();
    }
    $('[data-act=plan]', res).addEventListener('click', function () { ga('marketing_plan_cta_click'); });
    $('[data-act=report]', res).addEventListener('click', function () { ga('marketing_budget_report_request'); openReport(result, gform); });
  });

  function openReport(r, g) {
    var name = (g.first_name.value + ' ' + g.last_name.value).trim(), firm = g.firm_name.value.trim(), d = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    var rows = [['Annual revenue', fmt(r.revenue)], ['Growth objective', r.goalName], ['Recommended investment', r.pct + '% of revenue'], ['Recommended monthly budget', fmt(r.monthly)], ['Recommended annual budget', fmt(r.annual)]];
    if (r.current !== null) rows.push(['Current monthly investment', fmt(r.current)], ['Current annual investment', fmt(r.curAnnual)], ['Current share of revenue', (Math.round(r.curPct * 10) / 10) + '%'], ['Monthly investment gap', fmt(r.gapMonthly)], ['Annual investment gap', fmt(r.gapAnnual)]);
    var fw = [['Maintain Business', '5%', 'Minimum recommended investment to maintain business and market presence.'], ['Moderate Growth', '10%', 'Generate consistent leads and steadily grow your client base.'], ['Accelerated Growth', '15%', 'Increase case volume and capture greater market share.'], ['Market Expansion', '25%', 'Enter new markets and aggressively pursue new business.']];
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var html = '<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>Marketing Budget Report — ' + esc(firm) + '</title><style>body{font:15px/1.55 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#1A1F29;max-width:760px;margin:40px auto;padding:0 24px}h1{font-size:28px;color:#05253B;margin:0 0 4px}h2{font-size:17px;color:#05253B;margin:28px 0 8px;border-bottom:2px solid #CB9750;padding-bottom:6px}table{width:100%;border-collapse:collapse}td,th{padding:8px 10px;border-bottom:1px solid #E4E1DB;text-align:left}td:last-child{text-align:right;font-weight:600}.hl td{background:#FAF5EE}.meta{color:#5B6272}.cta{background:#05253B;color:#fff;padding:18px 20px;border-radius:6px;margin-top:24px}.cta a{color:#D8AE74}.fine{font-size:12px;color:#5B6272;margin-top:24px}@media print{body{margin:0}}</style></head><body>' +
      '<p class="meta">LegalMarketingFirm.net · Law Firm Marketing Budget Report</p><h1>' + esc(firm || 'Your firm') + '</h1><p class="meta">Prepared for ' + esc(name) + ' · ' + d + '</p>' +
      '<h2>Your results</h2><table>' + rows.map(function (x, i) { return '<tr' + (i === 3 || i === 4 ? ' class="hl"' : '') + '><td>' + x[0] + '</td><td>' + x[1] + '</td></tr>'; }).join('') + '</table>' +
      '<h2>Growth investment framework</h2><table><tr><th>Objective</th><th>Revenue %</th><th>Description</th></tr>' + fw.map(function (x) { return '<tr><td>' + x[0] + '</td><td style="text-align:left">' + x[1] + '</td><td style="text-align:left;font-weight:400">' + x[2] + '</td></tr>'; }).join('') + '</table>' +
      '<div class="cta"><strong>Next step:</strong> Knowing how much to invest is only the first step. Schedule a complimentary marketing consultation: <a href="https://www.legalmarketingfirm.net/contact/">legalmarketingfirm.net/contact</a> or ' + EMAIL + '</div>' +
      '<p class="fine">These are LegalMarketingFirm.net planning recommendations, not measured industry averages or guaranteed outcomes. Total marketing investment includes agency fees, media, personnel, technology and production. Consider cash flow, profitability and acquisition costs. Our framework provides general planning recommendations and does not guarantee growth outcomes.</p>' +
      '<script>window.onload=function(){setTimeout(function(){window.print()},300)}<\/script></body></html>';
    var w = window.open('', '_blank');
    if (w) { w.document.open(); w.document.write(html); w.document.close(); }
    else { var b = new Blob([html], { type: 'text/html' }), u = URL.createObjectURL(b), a = document.createElement('a'); a.href = u; a.download = 'marketing-budget-report.html'; a.click(); }
  }

  /* ---------- simple tool calculators ---------- */
  $$('form[data-tool]').forEach(function (f) {
    var tool = f.getAttribute('data-tool'), out = $('.tool-out', f.parentNode), started = false;
    f.addEventListener('input', function () { if (!started) { started = true; track('tool_start', { tool_id: tool }); } });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = {}, bad = false;
      $$('input[data-num]', f).forEach(function (el) {
        var n = parseMoney(el.value), req = el.hasAttribute('required'), invalid = (req && (n === null || n <= 0)) || isNaN(n) || (n !== null && n < 0);
        el.setAttribute('aria-invalid', String(!!invalid)); if (invalid) bad = true; v[el.name] = n;
      });
      var st = $('.status', f);
      if (bad) { st.hidden = false; st.className = 'status err'; st.textContent = 'Please enter positive numbers in the required fields.'; return; }
      st.hidden = true;
      var o = [];
      if (tool === 'roi') {
        var cases = v.leads * (v.conv / 100), rev = cases * v.value, roi = (rev - v.spend) / v.spend * 100;
        o = [['Estimated signed cases / mo', (Math.round(cases * 10) / 10).toString()], ['Estimated fee revenue / mo', fmt(rev)], ['Return on marketing spend', Math.round(roi) + '%'], ['Cost per signed case', cases > 0 ? fmt(v.spend / cases) : '—']];
      } else if (tool === 'cpl') {
        var cpl = v.spend / v.leads, cpc = v.signed ? v.spend / v.signed : null;
        o = [['Cost per lead', fmt(cpl)], ['Cost per signed case', cpc ? fmt(cpc) : 'Add signed cases'], ['Lead-to-case rate', v.signed ? (Math.round(v.signed / v.leads * 1000) / 10) + '%' : '—']];
      } else if (tool === 'intake') {
        var now = v.leads * v.conv / 100, tgt = v.leads * v.target / 100, add = tgt - now;
        o = [['Signed cases / mo now', (Math.round(now * 10) / 10).toString()], ['Signed cases / mo at target', (Math.round(tgt * 10) / 10).toString()], ['Added cases / mo', (Math.round(add * 10) / 10).toString()], ['Added fee revenue / yr', v.value ? fmt(add * v.value * 12) : 'Add average fee']];
      }
      out.innerHTML = o.map(function (x) { return '<div><span class="mono-label">' + x[0] + '</span><span class="v">' + x[1] + '</span></div>'; }).join('');
      out.hidden = false; track('tool_complete', { tool_id: tool });
    });
  });
})();
