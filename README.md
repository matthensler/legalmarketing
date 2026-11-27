# legalmarketingfirm.net

Static site for Legal Marketing Firm, served by GitHub Pages (custom domain in `CNAME`).

## Editing and rebuilding

All pages are generated. Don't hand-edit the HTML output; edit the source and rebuild:

```
python3 _src/build.py
```

| What | Where |
| --- | --- |
| Page templates, home, about, contact, legal, tools | `_src/build.py` |
| 20 service pages | `_src/data_services.py` |
| 15 practice areas + 20 practice/service combos | `_src/data_practices.py` |
| 163 city pages (from the 2027 blueprint) | `_src/data_cities.py` |
| 35 state hubs | `_src/data_states.py` |
| 16 answer articles + 8 research pages | `_src/data_insights.py` |
| Styles / scripts | `assets/site.css`, `assets/site.js` |

The build deletes and regenerates every page folder in the repo root (it keeps `_src`, `assets`, `CNAME`, `README.md`, `.git`).

## Leads (Google Sheet + Apps Script)

Every form posts to the Apps Script web app set as `LEADS_URL` in `assets/site.js`. Script source: `_src/google-apps-script.gs`.

- Contact page → sheet **Leads**
- Budget calculator → sheet **Calculator** (server-side recalculation, de-duplication by submission ID, lead tier, internal alert + prospect email with PDF)
- Audits, tools, research sign-ups → sheet **Requests**

To update the script without changing its URL: paste the new code, save, run `testCalculator`, then **Deploy → Manage deployments → edit → Version: New version → Deploy**.
