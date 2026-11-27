/**
 * Legal Marketing Firm — website lead capture.
 *
 * Saves every "Let's Build Your Strategy" submission as a row in this
 * Google Sheet and emails a lead alert.
 *
 * Setup (one time, ~5 minutes):
 * 1. Create a new Google Sheet (e.g. "Legal Marketing Firm — Leads").
 * 2. Extensions > Apps Script. Replace the starter code with this file. Save.
 * 3. Run testLead once from the editor and approve the permissions.
 *    A test row and a test email should arrive.
 * 4. Deploy > New deployment > Web app
 *      Execute as: Me
 *      Who has access: Anyone
 * 5. Copy the web app URL into data-leads on <form id="lead-form"> in
 *    index.html (it's empty until then, and the form falls back to email).
 */

const NOTIFY = 'hello@legalmarketingfirm.net';
const SHEET_NAME = 'Leads';

const COLUMNS = [
  'Timestamp', 'Form', 'Name', 'Firm', 'Email', 'Phone',
  'Practice area', 'Monthly budget', 'Page'
];

function doPost(e) {
  const p = (e && e.parameter) || {};

  // Spam trap: real visitors never fill the hidden "website" field.
  if (p.website) return ok_();

  const sheet = sheet_();
  const row = [
    new Date(), p.form || '', p.name || '', p.firm || '', p.email || '',
    p.phone || '', p.practice || '', p.budget || '', p.page || ''
  ];
  sheet.appendRow(row);

  const lines = COLUMNS.map((c, i) => row[i] ? c + ': ' + row[i] : null)
                       .filter(Boolean).slice(1);
  const subject = 'New lead: ' + (row[3] || 'Strategy request') +
                  (row[6] ? ' (' + row[6] + ')' : '');
  const opts = { name: 'Legal Marketing Firm website' };
  if (p.email) opts.replyTo = p.email;   // hit Reply to answer the lead directly
  MailApp.sendEmail(NOTIFY, subject,
    lines.join('\n') + '\n\nAll leads: ' + SpreadsheetApp.getActive().getUrl(), opts);

  return ok_();
}

function sheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) sh = ss.insertSheet(SHEET_NAME);
  if (sh.getLastRow() === 0) {
    sh.appendRow(COLUMNS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
  }
  return sh;
}

function ok_() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true }))
                       .setMimeType(ContentService.MimeType.JSON);
}

/** Run once from the editor to approve permissions and send yourself a test lead. */
function testLead() {
  doPost({ parameter: {
    form: 'Test', name: 'Test Lead', firm: 'Test & Partners LLP', email: NOTIFY,
    phone: '(555) 000-0000', practice: "Workers' comp", budget: '$5–15k', page: '/#contact'
  }});
}
