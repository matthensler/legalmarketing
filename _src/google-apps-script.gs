/**
 * Legal Marketing Firm — website lead capture (v2).
 *
 * Handles every form on legalmarketingfirm.net:
 *   - "Strategy request"   (Contact page 3-step form)        → sheet "Leads"
 *   - "Budget calculator"  (Law Firm Marketing Budget Calculator) → sheet "Calculator"
 *   - everything else      (Free audit, AI visibility audit, scorecard,
 *                           SEO audit, research updates)       → sheet "Requests"
 *
 * Budget calculator submissions are recalculated here (the browser's numbers
 * are never trusted), de-duplicated by submission_id, given a lead tier, and
 * trigger two emails: an internal alert to NOTIFY and a results email (with a
 * PDF report attached) to the prospect.
 *
 * UPDATING AN EXISTING DEPLOYMENT (keeps the same URL):
 *   1. Paste this file over the old code. Save.
 *   2. Run testCalculator once (approve any new permissions).
 *   3. Deploy > Manage deployments > pencil icon > Version: New version > Deploy.
 */

const NOTIFY = 'hello@legalmarketingfirm.net';
const BOOKING_URL = 'https://www.legalmarketingfirm.net/contact/';
const SITE = 'LegalMarketingFirm.net';

const GOALS = {
  'Maintain Business': 5,
  'Moderate Growth': 10,
  'Accelerated Growth': 15,
  'Market Expansion': 25
};

const LEAD_COLS = ['Timestamp', 'Form', 'Name', 'Firm', 'Email', 'Phone', 'Practice area',
  'Monthly budget', 'Page', 'First landing page', 'Referrer', 'UTM source', 'UTM medium', 'UTM campaign'];

const CALC_COLS = ['Submitted at', 'Submission ID', 'Lead tier', 'First name', 'Last name', 'Firm', 'Email',
  'Phone', 'Website', 'Practice area', 'City', 'State', 'Annual revenue', 'Current monthly spend',
  'Current annual spend', 'Current spend %', 'Growth objective', 'Recommended %', 'Recommended monthly',
  'Recommended annual', 'Monthly gap', 'Annual gap', 'Consent', 'Originating page', 'Page type',
  'Page market', 'Page practice', 'First landing page', 'Referrer', 'UTM source', 'UTM medium',
  'UTM campaign', 'UTM content', 'UTM term', 'Tool ID'];

const REQ_COLS = ['Timestamp', 'Form', 'First name', 'Last name', 'Name', 'Firm', 'Email', 'Phone',
  'Firm website', 'Practice area', 'City', 'State', 'Budget', 'Details', 'Email opt-in', 'Page',
  'Page type', 'Page market', 'First landing page', 'Referrer', 'UTM source', 'UTM medium', 'UTM campaign'];

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.hp) return json_({ ok: true });                       // spam trap
  try {
    if (rateLimited_(p.email)) return json_({ ok: false, error: 'rate_limited' });
    if (p.form === 'Budget calculator') return json_(calculator_(p));
    if (p.form === 'Strategy request') return json_(strategy_(p));
    return json_(request_(p));
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'server_error' });
  }
}

function doGet() { return json_({ ok: true, service: 'lmf-leads' }); }

/* ---------------- Contact page ---------------- */
function strategy_(p) {
  if (!validEmail_(p.email) || !p.name) return { ok: false, error: 'invalid' };
  const row = [new Date(), p.form, p.name, p.firm || '', p.email, p.phone || '', p.practice || '',
    p.budget || '', p.page || '', p.first_landing_page || '', p.referrer || '', p.utm_source || '',
    p.utm_medium || '', p.utm_campaign || ''];
  sheet_('Leads', LEAD_COLS).appendRow(row);
  const lines = LEAD_COLS.map((c, i) => row[i] ? c + ': ' + row[i] : null).filter(Boolean).slice(1);
  MailApp.sendEmail(NOTIFY, 'New lead: ' + (p.firm || 'Strategy request') + (p.practice ? ' (' + p.practice + ')' : ''),
    lines.join('\n') + '\n\nAll leads: ' + SpreadsheetApp.getActive().getUrl(),
    { name: SITE + ' website', replyTo: p.email });
  return { ok: true };
}

/* ---------------- Other request forms ---------------- */
function request_(p) {
  if (!validEmail_(p.email)) return { ok: false, error: 'invalid' };
  const name = p.name || [p.first_name, p.last_name].filter(Boolean).join(' ');
  const row = [new Date(), p.form || 'Website form', p.first_name || '', p.last_name || '', name,
    p.firm || p.firm_name || '', p.email, p.phone || '', p.firm_website || '', p.practice_area || p.practice || '',
    p.city || '', p.state || '', p.budget || '', p.details || '', p.consent || '', p.page || '',
    p.page_type || '', p.page_market || '', p.first_landing_page || '', p.referrer || '',
    p.utm_source || '', p.utm_medium || '', p.utm_campaign || ''];
  sheet_('Requests', REQ_COLS).appendRow(row);
  const lines = REQ_COLS.map((c, i) => row[i] ? c + ': ' + row[i] : null).filter(Boolean).slice(1);
  MailApp.sendEmail(NOTIFY, 'New request: ' + (p.form || 'Website form') + ' — ' + (row[5] || name || p.email),
    lines.join('\n') + '\n\nAll requests: ' + SpreadsheetApp.getActive().getUrl(),
    { name: SITE + ' website', replyTo: p.email });
  return { ok: true };
}

/* ---------------- Budget calculator ---------------- */
function calculator_(p) {
  const req = ['first_name', 'last_name', 'firm_name', 'email', 'website', 'practice_area', 'annual_revenue', 'growth_objective'];
  for (const k of req) if (!String(p[k] || '').trim()) return { ok: false, error: 'missing_' + k };
  if (!validEmail_(p.email)) return { ok: false, error: 'invalid_email' };
  const revenue = num_(p.annual_revenue);
  if (!(revenue > 0)) return { ok: false, error: 'invalid_revenue' };
  const pct = GOALS[p.growth_objective];
  if (!pct) return { ok: false, error: 'invalid_objective' };
  const hasCurrent = String(p.current_monthly_spend || '').trim() !== '';
  const current = hasCurrent ? num_(p.current_monthly_spend) : null;
  if (hasCurrent && !(current >= 0)) return { ok: false, error: 'invalid_current' };

  // Server-side recalculation (full precision; whole-dollar display).
  const annual = revenue * pct / 100;
  const monthly = annual / 12;
  const c = {
    annual_revenue: revenue, current_monthly_spend: current,
    current_annual_spend: hasCurrent ? current * 12 : null,
    current_spend_pct: hasCurrent ? current * 12 / revenue * 100 : null,
    growth_objective: p.growth_objective, recommended_pct: pct,
    recommended_monthly: monthly, recommended_annual: annual,
    monthly_gap: hasCurrent ? Math.max(0, monthly - current) : null,
    annual_gap: hasCurrent ? Math.max(0, annual - current * 12) : null
  };
  const tier = tier_(annual);
  const sid = String(p.submission_id || Utilities.getUuid());

  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const sh = sheet_('Calculator', CALC_COLS);
    // De-duplicate retries: same submission_id is stored and emailed once.
    if (sh.getLastRow() > 1) {
      const ids = sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues().flat().map(String);
      if (ids.indexOf(sid) !== -1) return { ok: true, duplicate: true };
    }
    const nul = v => (v === null || v === undefined) ? '' : v;
    sh.appendRow([new Date(), sid, tier, p.first_name, p.last_name, p.firm_name, p.email, p.phone || '',
      p.website, p.practice_area, p.city || '', p.state || '', revenue, nul(c.current_monthly_spend),
      nul(c.current_annual_spend), c.current_spend_pct === null ? '' : round1_(c.current_spend_pct),
      p.growth_objective, pct, Math.round(monthly), Math.round(annual), nul(c.monthly_gap === null ? null : Math.round(c.monthly_gap)),
      nul(c.annual_gap === null ? null : Math.round(c.annual_gap)), p.consent_status || 'not_opted_in',
      p.originating_page_url || '', p.page_type || '', p.page_market || '', p.page_practice || '',
      p.first_landing_page || '', p.referrer || '', p.utm_source || '', p.utm_medium || '',
      p.utm_campaign || '', p.utm_content || '', p.utm_term || '', p.tool_id || '']);
    SpreadsheetApp.flush();
  } finally {
    lock.releaseLock();
  }

  // Emails only after the row is saved.
  try { internalEmail_(p, c, tier); } catch (err) { console.error('internal email failed', err); }
  try { prospectEmail_(p, c); } catch (err) { console.error('prospect email failed', err); }
  return { ok: true, tier: tier };
}

function tier_(annual) {
  if (annual >= 500000) return 'Enterprise / immediate';
  if (annual >= 250000) return 'Premier / very high';
  if (annual >= 100000) return 'Growth / high';
  if (annual >= 50000) return 'Emerging / standard';
  return 'Nurture';
}

function internalEmail_(p, c, tier) {
  const has = c.current_monthly_spend !== null;
  const utm = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']
    .map(k => p[k] ? k + '=' + p[k] : null).filter(Boolean).join(', ') || '—';
  const body = [
    'A prospect has completed the Law Firm Marketing Budget Calculator.', '',
    'PROSPECT',
    'Name: ' + p.first_name + ' ' + p.last_name,
    'Firm: ' + p.firm_name,
    'Email: ' + p.email,
    'Phone: ' + (p.phone || '—'),
    'Website: ' + p.website,
    'Practice: ' + p.practice_area,
    'City/State: ' + ([p.city, p.state].filter(Boolean).join(', ') || '—'), '',
    'BUSINESS PROFILE',
    'Annual revenue: ' + usd_(c.annual_revenue),
    'Current monthly spend: ' + (has ? usd_(c.current_monthly_spend) : '—'),
    'Current annual spend: ' + (has ? usd_(c.current_annual_spend) : '—'),
    'Current spend %: ' + (has ? round1_(c.current_spend_pct) + '%' : '—'),
    'Growth objective: ' + c.growth_objective, '',
    'RECOMMENDATION',
    'Recommended %: ' + c.recommended_pct + '%',
    'Monthly budget: ' + usd_(c.recommended_monthly),
    'Annual budget: ' + usd_(c.recommended_annual),
    'Monthly gap: ' + (has ? usd_(c.monthly_gap) : '—'),
    'Annual gap: ' + (has ? usd_(c.annual_gap) : '—'), '',
    'ATTRIBUTION',
    'Originating page: ' + (p.originating_page_url || '—'),
    'First landing page: ' + (p.first_landing_page || '—'),
    'Referrer: ' + (p.referrer || '—'),
    'UTMs: ' + utm,
    'Submitted: ' + new Date().toString(),
    'Lead tier: ' + tier,
    'Email opt-in: ' + (p.consent_status || 'not_opted_in'), '',
    'Review the firm\'s website and marketing presence before outreach.',
    'Note: recommended spend is a planning figure, not a confirmed budget.', '',
    'All calculator leads: ' + SpreadsheetApp.getActive().getUrl()
  ].join('\n');
  MailApp.sendEmail(NOTIFY, 'New Calculator Lead | ' + p.firm_name + ' | ' + usd_(c.recommended_annual),
    body, { name: SITE + ' website', replyTo: p.email });
}

function prospectEmail_(p, c) {
  const has = c.current_monthly_spend !== null;
  const rows = [['Annual revenue', usd_(c.annual_revenue)], ['Growth objective', c.growth_objective],
    ['Recommended investment', c.recommended_pct + '% of revenue'], ['Monthly budget', usd_(c.recommended_monthly)],
    ['Annual budget', usd_(c.recommended_annual)]];
  if (has) rows.push(['Current monthly investment', usd_(c.current_monthly_spend)], ['Monthly investment gap', usd_(c.monthly_gap)]);
  const table = rows.map(r => '<tr><td style="padding:8px 12px;border-bottom:1px solid #E4E1DB">' + r[0] +
    '</td><td style="padding:8px 12px;border-bottom:1px solid #E4E1DB;text-align:right;font-weight:600">' + r[1] + '</td></tr>').join('');
  const html = '<div style="font:15px/1.6 Helvetica,Arial,sans-serif;color:#1A1F29;max-width:600px">' +
    '<p>Hi ' + esc_(p.first_name) + ',</p>' +
    '<p>Thank you for using our Law Firm Marketing Budget Calculator. Based on your annual revenue and growth objectives, we recommend the following planning investment:</p>' +
    '<table style="width:100%;border-collapse:collapse;margin:16px 0">' + table + '</table>' +
    '<p>Knowing how much to invest is only the first step. Our team can help you allocate your marketing budget to increase visibility, generate qualified leads and drive new business.</p>' +
    '<p><a href="' + BOOKING_URL + '" style="display:inline-block;background:#CB9750;color:#03182A;padding:12px 20px;border-radius:4px;text-decoration:none;font-weight:600">Schedule Your Complimentary Marketing Consultation</a></p>' +
    '<p>Your full report is attached as a PDF.</p>' +
    '<p>The LegalMarketingFirm.net Team<br><a href="mailto:' + NOTIFY + '">' + NOTIFY + '</a></p>' +
    '<p style="font-size:12px;color:#5B6272">Our framework provides general planning recommendations and does not guarantee growth outcomes.</p></div>';
  const text = 'Hi ' + p.first_name + ',\n\nThank you for using our Law Firm Marketing Budget Calculator. Based on your annual revenue and growth objectives, we recommend the following planning investment:\n\n' +
    rows.map(r => r[0] + ': ' + r[1]).join('\n') +
    '\n\nKnowing how much to invest is only the first step. Our team can help you allocate your marketing budget to increase visibility, generate qualified leads and drive new business.\n\nSchedule Your Complimentary Marketing Consultation: ' + BOOKING_URL +
    '\n\nThe LegalMarketingFirm.net Team\n\nOur framework provides general planning recommendations and does not guarantee growth outcomes.';
  MailApp.sendEmail(p.email, 'Your Personalized Law Firm Marketing Budget', text, {
    name: SITE, replyTo: NOTIFY, htmlBody: html, attachments: [reportPdf_(p, c)]
  });
}

function reportPdf_(p, c) {
  const has = c.current_monthly_spend !== null;
  const rows = [['Annual revenue', usd_(c.annual_revenue)], ['Growth objective', c.growth_objective],
    ['Recommended investment', c.recommended_pct + '% of revenue'], ['Recommended monthly budget', usd_(c.recommended_monthly)],
    ['Recommended annual budget', usd_(c.recommended_annual)]];
  if (has) rows.push(['Current monthly investment', usd_(c.current_monthly_spend)], ['Current annual investment', usd_(c.current_annual_spend)],
    ['Current share of revenue', round1_(c.current_spend_pct) + '%'], ['Monthly investment gap', usd_(c.monthly_gap)], ['Annual investment gap', usd_(c.annual_gap)]);
  const fw = [['Maintain Business', '5%', 'Minimum recommended investment to maintain business and market presence.'],
    ['Moderate Growth', '10%', 'Generate consistent leads and steadily grow your client base.'],
    ['Accelerated Growth', '15%', 'Increase case volume and capture greater market share.'],
    ['Market Expansion', '25%', 'Enter new markets and aggressively pursue new business.']];
  const td = 'padding:7px 10px;border-bottom:1px solid #E4E1DB;';
  const html = '<html><body style="font-family:Helvetica,Arial,sans-serif;color:#1A1F29;font-size:12pt">' +
    '<p style="color:#5B6272;font-size:10pt">LegalMarketingFirm.net · Law Firm Marketing Budget Report</p>' +
    '<h1 style="color:#05253B;font-size:22pt;margin:0">' + esc_(p.firm_name) + '</h1>' +
    '<p style="color:#5B6272">Prepared for ' + esc_(p.first_name + ' ' + p.last_name) + ' · ' +
    Utilities.formatDate(new Date(), 'America/Los_Angeles', 'MMMM d, yyyy') + '</p>' +
    '<h2 style="color:#05253B;font-size:14pt;border-bottom:2px solid #CB9750;padding-bottom:4px">Your results</h2>' +
    '<table style="width:100%;border-collapse:collapse">' + rows.map(r => '<tr><td style="' + td + '">' + r[0] + '</td><td style="' + td + 'text-align:right;font-weight:bold">' + r[1] + '</td></tr>').join('') + '</table>' +
    '<h2 style="color:#05253B;font-size:14pt;border-bottom:2px solid #CB9750;padding-bottom:4px">Growth investment framework</h2>' +
    '<table style="width:100%;border-collapse:collapse">' + fw.map(r => '<tr><td style="' + td + 'font-weight:bold">' + r[0] + '</td><td style="' + td + '">' + r[1] + '</td><td style="' + td + '">' + r[2] + '</td></tr>').join('') + '</table>' +
    '<p style="background:#05253B;color:#fff;padding:14px 16px;margin-top:20px">Next step: schedule a complimentary marketing consultation at ' + BOOKING_URL + ' or ' + NOTIFY + '</p>' +
    '<p style="font-size:9pt;color:#5B6272">These are LegalMarketingFirm.net planning recommendations, not measured industry averages or guaranteed outcomes. Total marketing investment includes agency fees, media, personnel, technology and production. Consider cash flow, profitability and acquisition costs.</p>' +
    '</body></html>';
  return Utilities.newBlob(html, 'text/html', 'report.html').getAs('application/pdf')
    .setName('Marketing Budget Report - ' + p.firm_name.replace(/[^\w\s&.-]/g, '') + '.pdf');
}

/* ---------------- helpers ---------------- */
function sheet_(name, cols) {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  if (sh.getLastRow() === 0 || sh.getLastColumn() < cols.length) {
    // New sheet, or an older header row with fewer columns: (re)write the header.
    sh.getRange(1, 1, 1, cols.length).setValues([cols]).setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  return sh;
}
function rateLimited_(email) {
  // Max 6 submissions per email address per 10 minutes.
  if (!email) return false;
  const cache = CacheService.getScriptCache(), key = 'rl_' + String(email).toLowerCase().slice(0, 200);
  const n = Number(cache.get(key) || 0);
  if (n >= 6) return true;
  cache.put(key, String(n + 1), 600);
  return false;
}
function validEmail_(e) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(e || '').trim()); }
function num_(v) { const n = Number(String(v).replace(/[$,\s]/g, '')); return isFinite(n) ? n : NaN; }
function usd_(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
function round1_(n) { return Math.round(n * 10) / 10; }
function esc_(s) { return String(s || '').replace(/[&<>"]/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch])); }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/* ---------------- tests (run from the editor) ---------------- */
function testLead() {
  Logger.log(strategy_({ form: 'Strategy request', name: 'Test Lead', firm: 'Test & Partners LLP', email: NOTIFY,
    phone: '(555) 000-0000', practice: "Workers' comp", budget: '$5–15k', page: '/contact/' }));
}
function testCalculator() {
  // Brief example: $2M revenue, $5k/mo current, Accelerated Growth → $25,000 / $300,000; gap $20,000 / $240,000
  Logger.log(calculator_({ form: 'Budget calculator', submission_id: 'test-' + Date.now(), first_name: 'Test',
    last_name: 'Lead', firm_name: 'Test & Partners LLP', email: NOTIFY, website: 'https://example.com',
    practice_area: 'Personal Injury', annual_revenue: '2000000', current_monthly_spend: '5000',
    growth_objective: 'Accelerated Growth', originating_page_url: 'https://www.legalmarketingfirm.net/tools/law-firm-marketing-budget-calculator/',
    page_type: 'tool', tool_id: 'law-firm-marketing-budget-calculator', consent_status: 'not_opted_in' }));
}
