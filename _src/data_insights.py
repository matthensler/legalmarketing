# AEO editorial articles under /insights/. Body is trusted HTML authored here.
# Each: concise answer first, deeper explanation, examples, named expert, reviewed date, sources, FAQs, internal links.
REVIEWED = '2026-11-27'
AUTHOR = 'Matt Hensler'
AUTHOR_ROLE = 'Head of Strategy, Legal Marketing Firm'

SRC_ABA71 = ('ABA Model Rule 7.1: Communication Concerning a Lawyer’s Services', 'https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/rule_7_1_communication_concerning_a_lawyer_s_services/')
SRC_HELPFUL = ('Google Search Central: Creating helpful, reliable, people-first content', 'https://developers.google.com/search/docs/fundamentals/creating-helpful-content')
SRC_GBP = ('Google Business Profile: Guidelines for representing your business', 'https://support.google.com/business/answer/3038177')
SRC_LSA = ('Google Local Services Ads help center', 'https://support.google.com/localservices')
SRC_AIO = ('Google Search Central: AI features and your website', 'https://developers.google.com/search/docs/appearance/ai-features')
SRC_SD = ('Google Search Central: Introduction to structured data', 'https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data')

ARTICLES = [
 dict(slug='how-much-does-law-firm-marketing-cost', title='How much does law firm marketing cost?', tag='Budget',
  desc='What law firm marketing really costs: the components of a budget, how agency fees and media differ, and how to set a number that fits your growth goals.',
  answer='Law firm marketing costs depend on your market, practice area and goals. A practical starting point is a percentage of revenue: our framework recommends 5% to maintain your position, 10% for moderate growth, 15% for accelerated growth and 25% to enter new markets. That total covers agency fees, media, staff, technology and production.',
  body='''<h2>What goes into the cost</h2>
<p>“Marketing cost” is really several costs bundled together. Comparing quotes is easier once you separate them:</p>
<ul><li><strong>Media spend</strong> — what you pay Google, Microsoft, TV and radio stations, streaming platforms or social networks. This scales with your goals and your market.</li>
<li><strong>Agency or management fees</strong> — strategy, campaign management, SEO, content and reporting.</li>
<li><strong>Production</strong> — video shoots, design, website builds and copywriting.</li>
<li><strong>Technology</strong> — call tracking, CRM and intake software, analytics.</li>
<li><strong>People</strong> — in-house marketing staff and intake team time.</li></ul>
<h2>Why practice area and market matter</h2>
<p>A personal injury firm in a major metro competes against national advertisers for some of the most expensive clicks in search. An estate planning firm in a smaller market may win most of its clients through local search and referrals. The same total budget can be far too small in one situation and generous in another.</p>
<h2>A simple way to set your number</h2>
<ol><li>Choose a growth objective: maintain, moderate growth, accelerated growth or market expansion.</li>
<li>Apply the matching percentage to annual revenue (5%, 10%, 15% or 25%).</li>
<li>Divide by 12 for a monthly planning figure.</li>
<li>Allocate across channels based on where your clients search and what you can measure.</li></ol>
<p><strong>Example:</strong> a firm with $2 million in revenue pursuing accelerated growth would plan around $300,000 a year — about $25,000 a month — across all marketing costs.</p>
<p>These percentages are our planning recommendations, not industry averages, and they don’t guarantee results. Cash flow, profitability and your intake capacity should shape the final number.</p>
<h2>What to avoid</h2>
<ul><li>Setting a budget with no way to measure what it produces.</li>
<li>Spreading a small budget across too many channels.</li>
<li>Paying for traffic your intake team can’t handle.</li></ul>''',
  faqs=[('Is a percentage of revenue the right way to budget?','It’s a useful planning anchor because it scales with your firm. Refine it with your actual cost per signed case once you have data.'),
        ('Do agency fees count toward the marketing budget?','Yes. Total marketing investment includes agency fees, media, staff, technology and production.')],
  links=['/tools/law-firm-marketing-budget-calculator/','/insights/how-much-should-a-law-firm-spend-on-marketing/','/law-firm-marketing-strategy/'], sources=[SRC_ABA71], calc=True),

 dict(slug='how-much-should-a-law-firm-spend-on-marketing', title='How much should a law firm spend on marketing?', tag='Budget',
  desc='How much a law firm should spend on marketing as a percentage of revenue, based on growth goals — with examples and a free calculator.',
  answer='Spend in line with your growth goal. Our framework recommends 5% of annual revenue to maintain your current position, 10% for moderate growth, 15% for accelerated growth and 25% if you’re expanding into new markets or practice areas.',
  body='''<h2>The growth investment framework</h2>
<div class="table-wrap"><table><tr><th>Objective</th><th>% of revenue</th><th>When it fits</th></tr>
<tr><td>Maintain Business</td><td>5%</td><td>Minimum to maintain business and market presence.</td></tr>
<tr><td>Moderate Growth</td><td>10%</td><td>Generate consistent leads and steadily grow your client base.</td></tr>
<tr><td>Accelerated Growth</td><td>15%</td><td>Increase case volume and capture greater market share.</td></tr>
<tr><td>Market Expansion</td><td>25%</td><td>Enter new markets and aggressively pursue new business.</td></tr></table></div>
<p>These are LegalMarketingFirm.net planning recommendations, not measured industry averages or guaranteed outcomes.</p>
<h2>Annual budget examples</h2>
<div class="table-wrap"><table><tr><th>Revenue</th><th>5%</th><th>10%</th><th>15%</th><th>25%</th></tr>
<tr><td>$500,000</td><td>$25,000</td><td>$50,000</td><td>$75,000</td><td>$125,000</td></tr>
<tr><td>$1,000,000</td><td>$50,000</td><td>$100,000</td><td>$150,000</td><td>$250,000</td></tr>
<tr><td>$2,000,000</td><td>$100,000</td><td>$200,000</td><td>$300,000</td><td>$500,000</td></tr>
<tr><td>$5,000,000</td><td>$250,000</td><td>$500,000</td><td>$750,000</td><td>$1,250,000</td></tr></table></div>
<h2>How to adjust the number</h2>
<ul><li><strong>Competition:</strong> crowded markets and practices may need more to make progress.</li>
<li><strong>Case value:</strong> higher average fees can justify higher acquisition costs.</li>
<li><strong>Intake capacity:</strong> don’t buy more leads than your team can answer well.</li>
<li><strong>Measurement:</strong> once you know your cost per signed case by channel, budget from that.</li></ul>''',
  faqs=[('What if we’re already spending more than the framework suggests?','Evaluate acquisition efficiency and returns before increasing spend further.'),
        ('Does more spend guarantee more clients?','No. Strategy, competition, intake and conversion all affect outcomes.')],
  links=['/tools/law-firm-marketing-budget-calculator/','/insights/how-much-does-law-firm-marketing-cost/','/insights/law-firm-marketing-budget-guide/'], sources=[], calc=True),

 dict(slug='how-to-choose-a-legal-marketing-agency', title='How to choose a legal marketing agency', tag='Strategy',
  desc='A practical checklist for choosing a legal marketing agency: what to ask, red flags to avoid and how to compare proposals.',
  answer='Choose an agency that understands legal advertising rules, reports on qualified intake and signed cases (not just clicks), owns none of your assets, and can show verifiable results. Ask how they measure success, who does the work and what happens if you leave.',
  body='''<h2>Questions to ask</h2>
<ol><li><strong>How do you define success?</strong> Look for intake and signed-case metrics, not impressions and traffic alone.</li>
<li><strong>Who owns the accounts, website and data?</strong> You should own your ad accounts, analytics, domain and content.</li>
<li><strong>Do you work with competing firms in my market?</strong> Ask how conflicts are handled.</li>
<li><strong>How do you handle attorney advertising rules?</strong> They should know claims, testimonials and disclaimer requirements vary by state.</li>
<li><strong>Who actually does the work?</strong> Meet the people on your account.</li>
<li><strong>What’s the contract length and exit process?</strong></li></ol>
<h2>Red flags</h2>
<ul><li>Guaranteed rankings or “#1 on Google.”</li><li>Guaranteed placement in ChatGPT or other AI tools.</li><li>Shared leads sold as exclusive.</li><li>Reporting that never mentions calls, forms or cases.</li><li>Paid link schemes or fake reviews.</li></ul>
<h2>How to compare proposals</h2>
<p>Line up proposals by the same components: media, management fees, production and technology. Ask each agency to state assumptions about cost per lead and conversion, and how they’ll prove or disprove those assumptions in the first 90 days.</p>''',
  faqs=[('Should we hire a legal-only agency?','Legal experience helps with compliance and intake, but the bigger question is whether they measure what matters to your firm.'),
        ('How long should an agency contract be?','Many firms prefer shorter initial terms with clear performance reviews. SEO and AI visibility need several months to show results.')],
  links=['/about/','/results/','/free-marketing-audit/'], sources=[SRC_ABA71], calc=False),

 dict(slug='how-long-does-law-firm-seo-take', title='How long does law firm SEO take?', tag='SEO',
  desc='How long law firm SEO takes to show results, what affects the timeline and what you should see in the first 3, 6 and 12 months.',
  answer='Most law firms see early movement from technical and on-page fixes within weeks, meaningful ranking gains in 4–6 months and competitive practice-area results in 6–12 months or more. Timelines depend on competition, your site’s starting point and how consistently you publish and earn authority.',
  body='''<h2>A realistic timeline</h2>
<ul><li><strong>Weeks 1–6:</strong> technical fixes, metadata and internal linking. Some long-tail rankings improve.</li>
<li><strong>Months 2–4:</strong> rewritten practice pages and new answer content start ranking for specific questions.</li>
<li><strong>Months 4–6:</strong> local rankings and mid-competition terms improve; organic inquiries rise.</li>
<li><strong>Months 6–12+:</strong> competitive practice-plus-city terms move as authority builds.</li></ul>
<h2>What speeds it up</h2>
<ul><li>A technically sound, fast website.</li><li>Clear practice and location structure.</li><li>Content that answers real client questions better than competitors.</li><li>Earned mentions from relevant, credible sources.</li><li>A steady flow of reviews for local results.</li></ul>
<h2>What slows it down</h2>
<ul><li>Highly competitive markets and practices (personal injury in a major metro).</li><li>Thin or duplicated pages.</li><li>Site migrations handled without redirects.</li></ul>
<p>Google’s own guidance emphasizes helpful, reliable, people-first content. That aligns with what works for law firms: expert-reviewed answers to real questions.</p>''',
  faqs=[('Can we speed up SEO with paid search?','Paid search doesn’t improve rankings, but it produces leads while SEO builds — and its search-term data shows which topics to prioritize.'),
        ('When should we expect leads from SEO?','Usually some within the first few months, with steady growth after six months if the work is consistent.')],
  links=['/law-firm-seo/','/law-firm-local-seo/','/insights/how-can-lawyers-rank-in-google-maps/'], sources=[SRC_HELPFUL], calc=False),

 dict(slug='how-can-lawyers-rank-in-google-maps', title='How can lawyers rank in Google Maps?', tag='Local SEO',
  desc='How lawyers rank in Google Maps and the local pack: Google Business Profile, reviews, citations, proximity and website signals.',
  answer='Lawyers rank in Google Maps through a complete, accurate Google Business Profile, the right primary category, a steady flow of genuine reviews, consistent firm information across directories and a website with strong local relevance. Proximity to the searcher also matters and can’t be changed.',
  body='''<h2>The main factors</h2>
<ul><li><strong>Relevance:</strong> categories, services and descriptions that match what people search.</li>
<li><strong>Distance:</strong> how close your verified address is to the searcher.</li>
<li><strong>Prominence:</strong> reviews, mentions, links and overall reputation.</li></ul>
<h2>Step by step</h2>
<ol><li>Claim and verify your profile at a real office location.</li>
<li>Choose the most specific primary category (for example, “Personal injury attorney”).</li>
<li>Add services, hours, photos and a clear description; use your real firm name.</li>
<li>Build a consistent, incentive-free review request process.</li>
<li>Respond to every review professionally without revealing client details.</li>
<li>Make your name, address and phone consistent across legal directories and data aggregators.</li>
<li>Strengthen the location page your profile links to.</li></ol>
<h2>What not to do</h2>
<ul><li>Don’t stuff keywords into your business name.</li><li>Don’t use virtual offices to create fake locations — this violates Google’s guidelines and can get profiles suspended.</li><li>Don’t buy reviews.</li></ul>''',
  faqs=[('Can we rank in cities where we don’t have an office?','Map rankings are tied to proximity, so it’s difficult. Use location content, paid search and LSAs for those areas.'),
        ('How many reviews do we need?','There’s no fixed number. Compare your count, rating and recency with the firms currently in the map pack.')],
  links=['/law-firm-local-seo/','/law-firm-reputation-management/','/law-firm-local-services-ads/'], sources=[SRC_GBP], calc=False),

 dict(slug='google-ads-vs-local-services-ads-for-lawyers', title='Google Ads vs Local Services Ads for lawyers', tag='Paid',
  desc='Google Ads vs Local Services Ads for law firms: how pricing, placement, control and lead quality compare — and when to use both.',
  answer='Local Services Ads charge per lead and appear at the very top of results with a Google Screened badge, but give you limited control. Google Ads charge per click and give you full control over keywords, ads and landing pages. Many firms get the best results running both.',
  body='''<h2>Side by side</h2>
<div class="table-wrap"><table><tr><th></th><th>Local Services Ads</th><th>Google Ads</th></tr>
<tr><td>Pricing</td><td>Per lead</td><td>Per click</td></tr>
<tr><td>Placement</td><td>Top of page, with badge</td><td>Top/bottom ad slots</td></tr>
<tr><td>Targeting control</td><td>Practice categories and area</td><td>Keywords, audiences, schedule, geography</td></tr>
<tr><td>Landing page</td><td>Your LSA profile</td><td>Your own page</td></tr>
<tr><td>Setup</td><td>Screening and verification</td><td>Account build and tracking</td></tr>
<tr><td>Key ranking factors</td><td>Reviews, responsiveness, proximity</td><td>Bids, ad relevance, landing page quality</td></tr></table></div>
<h2>When LSAs fit best</h2>
<ul><li>Your practice category is supported in your market.</li><li>You have strong reviews and fast response times.</li><li>You want predictable per-lead pricing.</li></ul>
<h2>When Google Ads fit best</h2>
<ul><li>You need control over which case types you pay for.</li><li>You want to test messaging and landing pages.</li><li>You’re targeting specific searches LSAs don’t cover.</li></ul>
<h2>Running both</h2>
<p>LSAs capture the top slot; Google Ads cover specific case types and searches. Track both to the same intake outcomes so you can compare cost per signed case.</p>''',
  faqs=[('Can we dispute bad LSA leads?','Yes, Google allows disputes for invalid leads within its rules. Review leads regularly.'),
        ('Do reviews affect Google Ads?','Not directly, but they influence LSAs and click-through on your profile.')],
  links=['/law-firm-local-services-ads/','/law-firm-google-ads/','/law-firm-ppc/'], sources=[SRC_LSA], calc=False),

 dict(slug='what-is-a-good-cost-per-lead-for-law-firms', title='What is a good cost per lead for law firms?', tag='Measurement',
  desc='How to judge cost per lead for a law firm — and why cost per signed case is the number that really matters.',
  answer='A “good” cost per lead is one that produces signed cases at a profit for your firm. It varies too much by practice, market and channel for one benchmark to be reliable. Work backward from your average fee and your lead-to-case conversion rate to find the most you can afford per lead.',
  body='''<h2>Work backward from case value</h2>
<ol><li>Average fee per signed case (for example, $8,000).</li><li>Lead-to-signed-case rate (for example, 1 in 10, or 10%).</li><li>Target marketing cost as a share of fee (for example, 25%).</li></ol>
<p><strong>Math:</strong> $8,000 × 25% = $2,000 affordable cost per signed case. At a 10% conversion rate, you can afford up to <strong>$200 per lead</strong>.</p>
<p>This is an illustration, not a benchmark. Your own numbers will differ.</p>
<h2>Why cost per lead alone misleads</h2>
<ul><li>Cheap leads often convert poorly.</li><li>Channels produce different case types and values.</li><li>Intake performance changes everything: the same leads can produce very different results with faster follow-up.</li></ul>
<h2>What to track instead</h2>
<ul><li>Cost per qualified lead</li><li>Lead-to-consultation rate</li><li>Consultation-to-client rate</li><li>Cost per signed case by channel</li></ul>''',
  faqs=[('Why don’t you publish benchmark numbers?','Published averages mix very different markets and practices. We’d rather help you calculate yours.'),
        ('How do we track cost per signed case?','Tag every lead with its source and record outcomes in your intake system.')],
  links=['/tools/cost-per-lead-calculator/','/tools/marketing-roi-calculator/','/insights/how-to-measure-law-firm-marketing-roi/'], sources=[], calc=False),

 dict(slug='how-can-law-firms-appear-in-chatgpt', title='How can law firms appear in ChatGPT?', tag='AI Search',
  desc='How law firms can show up in ChatGPT and other AI assistants: entity consistency, reviews, citable content, third-party mentions and tracking.',
  answer='Law firms improve their chances of appearing in ChatGPT and other AI assistants by keeping firm information consistent across the web, earning reviews and credible third-party mentions, publishing clear answer content AI tools can cite, and tracking a set of prompts over time. No one can guarantee placement.',
  body='''<h2>How AI assistants choose firms</h2>
<p>AI assistants that browse the web assemble answers from sources they find relevant and trustworthy: directories, review sites, news, firm websites and other published content. Firms that appear consistently across reputable sources are easier for them to recognize and recommend.</p>
<h2>What to do</h2>
<ol><li><strong>Make your identity consistent.</strong> Same firm name, address, phone, practice areas and attorney names everywhere.</li>
<li><strong>Earn reviews.</strong> Steady, genuine reviews on Google and relevant legal directories.</li>
<li><strong>Publish citable answers.</strong> Clear, dated, attorney-reviewed content that answers specific questions.</li>
<li><strong>Get mentioned.</strong> Local media, bar associations, community organizations and legal publications.</li>
<li><strong>Use structured data.</strong> Organization, Person and Article markup help machines understand your content.</li>
<li><strong>Track prompts.</strong> Test the questions your prospects ask, monthly, and log mentions and citations.</li></ol>
<h2>What not to do</h2>
<ul><li>Don’t publish unverifiable “best lawyer” claims.</li><li>Don’t create fake reviews or listings.</li><li>Don’t block AI crawlers unintentionally if you want to be cited.</li></ul>''',
  faqs=[('Can we pay to appear in ChatGPT?','We’re not aware of a way to pay for recommendations in AI answers. Visibility comes from the signals above.'),
        ('Is this different from SEO?','It overlaps but isn’t the same; ranking well in Google doesn’t guarantee AI visibility.')],
  links=['/law-firm-ai-search-optimization/','/insights/seo-vs-aeo-vs-geo-for-law-firms/','/tools/ai-visibility-audit/'], sources=[SRC_AIO, SRC_SD], calc=False),

 dict(slug='seo-vs-aeo-vs-geo-for-law-firms', title='SEO vs AEO vs GEO for law firms', tag='AI Search',
  desc='The difference between SEO, AEO and GEO for law firms — what each optimizes for, how they overlap and where to start.',
  answer='SEO helps your pages rank in search results. AEO (answer engine optimization) helps your content become the direct answer in snippets and voice or AI responses. GEO (generative engine optimization) helps AI tools cite and recommend your firm in generated answers. They share foundations, and most firms need all three.',
  body='''<div class="table-wrap"><table><tr><th></th><th>SEO</th><th>AEO</th><th>GEO</th></tr>
<tr><td>Goal</td><td>Rank pages</td><td>Be the direct answer</td><td>Be cited/recommended by AI</td></tr>
<tr><td>Main surfaces</td><td>Organic results, map pack</td><td>Featured snippets, People Also Ask, voice</td><td>ChatGPT, Gemini, Perplexity, AI Overviews</td></tr>
<tr><td>Key tactics</td><td>Technical, content, links</td><td>Question-led structure, concise answers</td><td>Entity consistency, original info, mentions</td></tr>
<tr><td>Measured by</td><td>Rankings, organic leads</td><td>Snippets, answer traffic</td><td>Mentions, citations, AI referrals</td></tr></table></div>
<h2>Where they overlap</h2>
<p>All three reward accurate, well-structured, expert content and a strong reputation. Work on one usually helps the others.</p>
<h2>Where to start</h2>
<ol><li>Fix technical SEO and practice pages.</li><li>Rewrite key pages answer-first.</li><li>Establish a prompt baseline for AI visibility.</li><li>Add original information and earn mentions.</li></ol>''',
  faqs=[('Is GEO replacing SEO?','No. Search engines remain a major source of legal clients, and SEO foundations support GEO.'),
        ('Which matters most for a small firm?','Usually local SEO first, then answer content that supports AEO and GEO.')],
  links=['/law-firm-seo/','/law-firm-aeo/','/law-firm-geo/'], sources=[SRC_AIO], calc=False),

 dict(slug='how-to-grow-a-law-firm', title='How to grow a law firm', tag='Strategy',
  desc='How to grow a law firm through marketing: set a goal, fix intake, choose channels by practice and market, measure cost per case and reinvest.',
  answer='To grow a law firm, set a clear growth goal, fix intake so you convert the leads you already get, invest in the channels your clients actually use, measure cost per signed case by channel and reinvest in what works. Growth usually comes from doing a few things consistently, not from adding every channel at once.',
  body='''<h2>1. Choose a growth objective</h2><p>Maintain, grow moderately, accelerate or expand. Your objective sets your budget and priorities.</p>
<h2>2. Fix intake first</h2><p>If calls go unanswered or follow-up is slow, more marketing makes the problem more expensive. Measure answer rate and speed to lead.</p>
<h2>3. Match channels to your practice</h2><p>Urgent practices (PI, criminal defense) lean on paid search, LSAs and the map pack. Planning practices (estate planning, business) lean on content, referrals and nurture.</p>
<h2>4. Build owned visibility</h2><p>SEO, AI search visibility and reviews compound over time and reduce dependence on paid media.</p>
<h2>5. Measure what matters</h2><p>Track leads, qualified leads, consultations and signed cases by source.</p>
<h2>6. Reinvest</h2><p>Shift budget toward channels with the best cost per signed case, and revisit quarterly.</p>''',
  faqs=[('What’s the fastest way to grow?','Usually fixing intake plus paid search and LSAs, while SEO and AI visibility build.'),
        ('Should we expand practice areas?','Only where you can deliver and market credibly; our Market Expansion objective assumes a larger investment.')],
  links=['/law-firm-marketing-strategy/','/tools/law-firm-marketing-budget-calculator/','/law-firm-intake-optimization/'], sources=[], calc=True),

 dict(slug='how-to-improve-law-firm-intake-conversion', title='How to improve law firm intake conversion', tag='Intake',
  desc='Practical ways law firms can convert more inquiries into clients: speed to lead, answer rates, scripts, follow-up and tracking.',
  answer='Improve intake conversion by answering every call live, responding to forms within minutes, using consistent screening scripts, following up multiple times with unbooked leads and tracking outcomes by source. Small improvements here often produce more new clients than a bigger ad budget.',
  body='''<h2>Measure your baseline</h2><ul><li>Answer rate (calls answered live)</li><li>Speed to lead for forms and chats</li><li>Lead-to-consultation rate</li><li>Consultation-to-client rate</li></ul>
<h2>Quick wins</h2><ol><li>Cover after-hours calls with an answering service or on-call rotation.</li><li>Send an instant acknowledgment to every form submission.</li><li>Call web leads back within minutes during business hours.</li><li>Use a short, consistent screening script.</li><li>Follow up unbooked leads several times over days, by phone, text (with consent) and email.</li></ol>
<h2>Track it</h2><p>Connect call tracking and form sources to your intake system so you can see which channels produce clients — not just calls.</p>''',
  faqs=[('What’s a good answer rate?','As close to 100% as you can get. Missed calls in urgent practices often go straight to the next firm.'),
        ('Should we use chat?','Live or AI-assisted chat can help, but only if it’s staffed or configured to hand off quickly.')],
  links=['/law-firm-intake-optimization/','/tools/intake-conversion-calculator/','/law-firm-email-marketing/'], sources=[], calc=False),

 dict(slug='how-to-measure-law-firm-marketing-roi', title='How to measure law firm marketing ROI', tag='Measurement',
  desc='How to measure law firm marketing ROI: tracking sources, cost per signed case and fee revenue by channel, with a simple formula.',
  answer='Measure marketing ROI by tracking every lead to its source, recording which leads become signed clients and what fees they produce, then comparing fee revenue to marketing cost by channel. ROI = (fee revenue from marketing − marketing cost) ÷ marketing cost.',
  body='''<h2>The formula</h2><p><strong>ROI</strong> = (Fee revenue attributed to marketing − Marketing cost) ÷ Marketing cost</p>
<p><strong>Example:</strong> $20,000 in monthly marketing produces 6 signed cases worth an average $10,000 in fees. ROI = ($60,000 − $20,000) ÷ $20,000 = 200%.</p>
<h2>What you need to track</h2><ul><li>Lead source for every call, form and chat</li><li>Outcome of each lead (qualified, consultation, signed)</li><li>Fee revenue per signed case (or a reliable average by case type)</li><li>All marketing costs by channel</li></ul>
<h2>Common pitfalls</h2><ul><li>Long case cycles — contingency matters may take months or years to pay; use expected value until fees are realized.</li><li>Ignoring brand and referral effects from TV, reviews and content.</li><li>Comparing channels on cost per lead instead of cost per case.</li></ul>''',
  faqs=[('How do we handle contingency cases?','Use an expected value per case type until fees are collected, then reconcile.'),
        ('What ROI should we target?','That depends on your margins and growth goals; consistent measurement matters more than a target number.')],
  links=['/tools/marketing-roi-calculator/','/insights/what-is-a-good-cost-per-lead-for-law-firms/','/law-firm-marketing-strategy/'], sources=[], calc=False),

 dict(slug='what-is-law-firm-geo', title='What is law firm GEO?', tag='AI Search',
  desc='What generative engine optimization (GEO) means for law firms, why it matters and how to start.',
  answer='Law firm GEO (generative engine optimization) is the practice of improving how often AI tools like ChatGPT, Gemini, Perplexity and Google AI Overviews mention, cite or recommend your firm. It focuses on consistent entity information, citable original content, reviews and third-party mentions — and on tracking results across a defined set of prompts.',
  body='''<h2>Why it matters</h2><p>Prospects increasingly ask AI tools legal questions and for recommendations. Those answers draw on sources across the web, so firms that are well represented in trustworthy sources are more likely to be included.</p>
<h2>How to start</h2><ol><li>Write down 25–100 prompts your prospects might ask (by practice and city).</li><li>Test them across major AI tools and record mentions and citations.</li><li>Fix inconsistent firm information across profiles and directories.</li><li>Publish original, specific content — local data, clear explanations, dated updates.</li><li>Earn mentions from credible publications and organizations.</li><li>Re-test monthly.</li></ol>
<h2>What GEO isn’t</h2><p>It isn’t a trick or a guarantee. AI outputs vary by user and change over time, so measure trends rather than single answers.</p>''',
  faqs=[('Is GEO the same as AI search optimization?','GEO is one part of it. Our AI search optimization service combines GEO, AEO and entity work.'),
        ('How long does GEO take?','Entity fixes can show up relatively quickly; content and mentions build over months.')],
  links=['/law-firm-geo/','/law-firm-ai-search-optimization/','/insights/legal-ai-visibility-index/'], sources=[SRC_AIO], calc=False),

 dict(slug='what-is-answer-engine-optimization-for-lawyers', title='What is answer engine optimization for lawyers?', tag='AI Search',
  desc='Answer engine optimization (AEO) for lawyers: structuring content to win featured snippets, People Also Ask, voice and AI answers.',
  answer='Answer engine optimization (AEO) for lawyers means structuring your content so search engines and AI assistants can lift a clear, accurate answer to a client’s question — and credit your firm. In practice: answer the question in the first two or three sentences, explain in more depth below, show who reviewed it and keep it current.',
  body='''<h2>The AEO page pattern</h2><ol><li>A heading that matches the question.</li><li>A concise answer (40–60 words) immediately below.</li><li>Deeper explanation, examples and exceptions.</li><li>Named reviewer and review date.</li><li>Related questions and internal links.</li></ol>
<h2>Where the questions come from</h2><ul><li>Intake calls and consultation notes</li><li>Search Console queries</li><li>People Also Ask results</li><li>Questions prospects type into AI tools</li></ul>
<h2>Example</h2><p><em>Question:</em> “How long do I have to report a work injury?” A strong page answers with the state-specific deadline first, then explains exceptions and what to do next.</p>''',
  faqs=[('Does AEO need special markup?','Structured data helps machines understand content, but the clear answer on the page matters most.'),
        ('Who should review answers?','A licensed attorney in the relevant jurisdiction.')],
  links=['/law-firm-aeo/','/insights/seo-vs-aeo-vs-geo-for-law-firms/','/law-firm-content-marketing/'], sources=[SRC_SD, SRC_HELPFUL], calc=False),

 dict(slug='how-to-market-a-personal-injury-law-firm', title='How to market a personal injury law firm', tag='Practice',
  desc='How to market a personal injury law firm: channels, intake, local visibility, AI search and budget planning.',
  answer='Market a personal injury firm by capturing urgent demand with Google Ads and Local Services Ads, winning the map pack with reviews and a strong Google Business Profile, building case-type content for SEO and AI search, and answering every call immediately. Track cost per signed case so you can shift budget to what works.',
  body='''<h2>Capture urgent demand</h2><p>Accident victims often call the first credible firm they find. Paid search and LSAs put you at the top while organic visibility builds.</p>
<h2>Win local search</h2><p>Most “near me” searches resolve in the map pack. A complete profile and steady reviews are essential.</p>
<h2>Build case-type content</h2><p>Car, truck, motorcycle, pedestrian, premises and wrongful death pages, each with real answers about insurance, deadlines and process.</p>
<h2>Show up in AI answers</h2><p>Prospects increasingly ask AI who to hire. Consistent firm information, reviews and citable content help.</p>
<h2>Intake is half the battle</h2><p>24/7 live answering and fast follow-up convert more of the same leads.</p>
<h2>Consider brand media</h2><p>In many markets, TV and CTV build the recognition that lifts every other channel.</p>''',
  faqs=[('How much should a PI firm spend?','Use our framework: 5–25% of revenue depending on growth objective.'),
        ('Is TV necessary?','Not always. In smaller markets, digital channels often deliver better returns first.')],
  links=['/practice-areas/personal-injury/','/practice-areas/personal-injury/ppc/','/tools/law-firm-marketing-budget-calculator/'], sources=[SRC_ABA71], calc=True),

 dict(slug='how-to-market-a-small-law-firm', title='How to market a small law firm', tag='Strategy',
  desc='How to market a small law firm on a focused budget: local SEO, reviews, a few high-intent channels, referrals and measurement.',
  answer='Market a small law firm by focusing on a few high-impact channels: a strong Google Business Profile and reviews, a fast website with clear practice pages, one paid channel aimed at high-intent searches, and a simple referral and follow-up system. Measure where clients come from and add channels only when the first ones work.',
  body='''<h2>Start with the foundation</h2><ul><li>Google Business Profile, fully complete</li><li>A steady review request process</li><li>A fast, mobile-friendly website with one page per practice</li><li>Call tracking and a basic intake log</li></ul>
<h2>Add one paid channel</h2><p>Local Services Ads or a tightly targeted Google Ads campaign. Start small, measure, then scale.</p>
<h2>Use your relationships</h2><p>Stay in touch with past clients and referral sources with a simple newsletter.</p>
<h2>Answer questions online</h2><p>A handful of strong answer articles can rank locally and get cited by AI tools.</p>
<h2>Smaller markets are an advantage</h2><p>In many smaller metros, competition for search and AI visibility is lighter — a focused firm can lead its market.</p>''',
  faqs=[('What’s the minimum budget?','Use the calculator with the Maintain objective (5% of revenue) as a floor.'),
        ('Should small firms do SEO?','Yes — especially local SEO and practice pages, which compound over time.')],
  links=['/law-firm-local-seo/','/tools/law-firm-marketing-budget-calculator/','/markets/'], sources=[SRC_GBP], calc=True),
]
ART = {a['slug']: a for a in ARTICLES}

# Research pages: methodology-first; no data published until measured.
RESEARCH = [
 dict(slug='state-of-legal-marketing', title='State of Legal Marketing', desc='Our planned annual study of how law firms invest in and measure marketing — methodology, scope and release updates.',
  what='An annual study of how law firms allocate marketing budgets, which channels they use and how they measure results.',
  method=['Sample: law firm owners, partners and marketing leaders across practice areas and firm sizes.','Geography: United States, reported by region and market size where sample allows.','Data source: structured survey plus anonymized, aggregated campaign data where clients permit.','Limitations: self-reported data and non-random sampling; results will be presented with sample sizes and margins.']),
 dict(slug='legal-ai-visibility-index', title='Legal AI Visibility Index', desc='How often law firms are mentioned and cited by AI assistants for legal queries — methodology and release updates.',
  what='A recurring measurement of which law firms AI assistants mention and cite for common legal questions, by practice and market.',
  method=['Prompt set: standardized prompts by practice area and city (e.g., “best workers comp lawyer in Rockford”).','Engines: major AI assistants and Google AI Overviews, tested on a fixed schedule.','Metrics: mention rate, citation rate, sources cited and consistency across runs.','Limitations: AI outputs vary by user, location and time; results describe a sample of runs, not a guaranteed ranking.']),
 dict(slug='law-firm-cost-per-lead-benchmarks', title='Law Firm Cost Per Lead Benchmarks', desc='Planned cost-per-lead and cost-per-case benchmarks by practice area and market — methodology and release updates.',
  what='Cost per lead and, where available, cost per signed case by channel, practice area and market size.',
  method=['Data source: anonymized, aggregated campaign data from participating firms, with permission.','Segmentation: practice, channel and market tier, reported only where sample size is adequate.','Definitions: “lead” and “qualified lead” defined explicitly and applied consistently.','Limitations: not a guarantee of future costs; markets change quickly.']),
 dict(slug='law-firm-marketing-budget-guide', title='Law Firm Marketing Budget Guide', desc='A guide to planning a law firm marketing budget by growth objective, with examples and a free calculator.',
  what='Our growth investment framework, budget examples and how to allocate spend by channel.',
  method=['Framework: 5% maintain, 10% moderate growth, 15% accelerated growth, 25% market expansion — LegalMarketingFirm.net planning recommendations.','Scope: total marketing investment, including agency fees, media, personnel, technology and production.','Limitations: not measured industry averages; adjust for cash flow, profitability and acquisition costs.'], guide=True),
 dict(slug='personal-injury-marketing-benchmarks', title='Personal Injury Marketing Benchmarks', desc='Planned personal injury marketing benchmarks: channel mix, cost per case and intake performance — methodology and updates.',
  what='Channel mix, cost per signed case and intake metrics for personal injury firms by market size.',
  method=['Sample: PI firms of varying size; participation voluntary.','Metrics: channel mix, cost per qualified lead, cost per signed case, answer rate and speed to lead.','Limitations: case values vary widely; results will be presented as ranges with sample sizes.']),
 dict(slug='legal-marketing-trends', title='Legal Marketing Trends', desc='Trends shaping law firm marketing: AI search, local search, intake technology and measurement — updated regularly.',
  what='A regularly updated briefing on shifts in how clients find and choose law firms.',
  method=['Sources: our own prompt tracking and campaign observations, platform announcements and published third-party research (cited individually).','Update cadence: quarterly.','Limitations: trends are directional; we cite sources for every quantitative claim.']),
 dict(slug='most-competitive-legal-markets', title='Most Competitive Legal Markets', desc='A planned ranking of U.S. legal markets by marketing competition — methodology and release updates.',
  what='A comparison of U.S. markets by search competition, advertiser density, review benchmarks and AI visibility.',
  method=['Markets: the city inventory on our Markets pages.','Factors: SEO competition, paid search competition, specialized agency presence, review benchmarks and AI citation patterns.','Limitations: city boundaries differ from metro areas; scores will be published only after measurement.']),
 dict(slug='law-firm-conversion-benchmarks', title='Law Firm Conversion Benchmarks', desc='Planned benchmarks for law firm website and intake conversion rates — methodology and release updates.',
  what='Website conversion rates, answer rates and lead-to-client rates by practice and channel.',
  method=['Data source: anonymized analytics and intake data from participating firms.','Metrics: visit-to-lead, lead-to-consultation and consultation-to-client rates.','Limitations: tracking quality varies by firm; data will be filtered for completeness.']),
]
