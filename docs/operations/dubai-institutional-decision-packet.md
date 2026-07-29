# Dubai institutional decision packet

- **Milestone:** M1 — Operating contexts and jurisdiction decisions
- **Status:** Draft / not approved
- **Owner:** `[name and role]`
- **Target decision date:** `[YYYY-MM-DD]`
- **Last reviewed:** `[YYYY-MM-DD]`
- **Next mandatory revalidation:** `[YYYY-MM-DD or triggering event]`

> [!CAUTION]
> This packet records questions, evidence, and decisions. It is not legal, tax,
> regulatory, accounting, broker, or investment advice. Incorporation,
> proprietary capital, a commercial licence, a regulator response, or successful
> paper trading does not by itself authorize any live activity. Qualified
> advisers and each relevant provider must confirm the exact entity, activity,
> market, instrument, account, data use, and operating model in writing.

## How to use this packet

Keep this tracked file as an unpopulated public template. Complete it in an
access-controlled private system, not in Git. Only redacted summaries that an
accountable owner has expressly approved for public release may be committed.

Use `Proposed`, `Confirmed`, `Rejected`, or `Blocked` for decision status.
Every `Confirmed` entry must cite an item in the evidence register. Oral advice
is a lead only; record signed advice, regulator correspondence, provider terms,
or another durable primary source before clearing a gate.

Re-open affected decisions after any change to ownership, control, domicile,
licence, activity, revenue, customers, capital source, market, instrument,
broker, custodian, venue, data use, Hermes authority, or UAE or destination-
market rules.

## 1. Decision summary

| Decision | Selection | Status | Evidence IDs | Approver |
| --- | --- | --- | --- | --- |
| UAE domicile and legal form | `[TBD]` | Proposed | — | `[TBD]` |
| Commercial and regulated activities | `[TBD]` | Proposed | — | `[TBD]` |
| First funded market and asset class | `[TBD]` | Proposed | — | `[TBD]` |
| First broker, custodian, and bank | `[TBD]` | Proposed | — | `[TBD]` |
| Crypto path | `[disabled / VARA path TBD]` | Proposed | — | `[TBD]` |
| Indian-market path | `[research only / FPI feasibility]` | Proposed | — | `[TBD]` |
| Commodity exposure | `[ETF only / futures deferred]` | Proposed | — | `[TBD]` |
| Institutional live capability | `NO-GO (repository default)` | Blocked | — | — |

The institutional live decision remains `NO-GO` until every gate in section 15
is independently cleared. Paper operation may continue only in an environment
that cannot reach funded accounts.

## 2. Dual-use charter

### Public product context

- helm remains open-source software for self-directed individuals using their
  own accounts and capital.
- The software does not pool assets, hold customer assets, open accounts, or
  grant trading authority merely because a user authenticates.
- Personalized advice, managed accounts, client execution, copy trading,
  strategy marketplaces, and transaction- or asset-linked compensation remain
  disabled unless separately designed and authorized.

### Institutional context

- The proposed UAE entity uses a separate helm deployment solely for capital
  legally and beneficially owned by that same entity.
- The entity's accounts, credentials, positions, mandates, approvals, audit
  state, market-data rights, and kill switches never mix with an individual's.
- Hermes proposes; authorized humans approve; deterministic helm policy may
  release only an order inside a current mandate. Hermes cannot access
  credentials, change policy, approve itself, or rearm execution.
- Open-source publication and institutional operation are separate activities.
  Counsel must identify the publisher, operator, IP owner, service provider,
  revenue recipient, and associated obligations for each.

### Charter attestations

- [ ] `capital_owner = legal_entity = mandate_owner = broker_account_owner`
- [ ] No third party has contributed capital, beneficial economic exposure, or
      a withdrawal right.
- [ ] No client, investor, subscriber, or individual account is managed by the
      institutional deployment.
- [ ] No transaction-based, performance-based, asset-based, referral, copy-
      trading, or order-flow-linked compensation is received.
- [ ] No public statement calls incorporation, paper readiness, or a provider
      account proof of regulatory authorization.
- [ ] Any failure of an attestation automatically blocks institutional live use.

**Exceptions or unresolved facts:** `[none / describe and assign owner]`

## 3. Own-account-only boundary

Counsel must test substance, not only the label “proprietary” or “own account.”

| Question | Recorded answer | Evidence ID | Status |
| --- | --- | --- | --- |
| Who legally and beneficially owns all contributed capital? | `[TBD]` | — | Proposed |
| Can any other person direct, redeem, share, or receive returns? | `[TBD]` | — | Proposed |
| Are shareholder loans or external financing used? | `[TBD]` | — | Proposed |
| Does helm act for an affiliate, founder, employee, client, fund, or SPV? | `[TBD]` | — | Proposed |
| Is any advice, signal, model, execution, custody, transfer, or account service supplied to another person? | `[TBD]` | — | Proposed |
| Is any compensation linked to assets, returns, referrals, trades, or execution? | `[TBD]` | — | Proposed |
| Does any mandate create discretion over capital not owned by the entity? | `[TBD]` | — | Proposed |
| Could the frequency or character of activity change a trader/dealer or other regulatory analysis in a destination market? | `[TBD]` | — | Proposed |

Any answer that introduces third-party capital, authority, benefit, or service
is a scope change and a `NO-GO`, not an exception to document later.

## 4. Domicile and perimeter comparison

Do not choose a domicile from headline tax rates. Compare the exact activity,
perimeter, commercial licence, regulator, substance, cost, banking, provider
eligibility, staffing, governance, and destination-market access.

| Candidate | Questions requiring written resolution | Evidence to collect | Decision |
| --- | --- | --- | --- |
| **DIFC / DFSA** | Does the proposed own-capital activity fall within or outside a DFSA Financial Service? Does instrument type, frequency, market making, dealing as principal, fund structure, advice, or services to affiliates change the answer? Is a DFSA application, waiver, or perimeter response required? | DIFC activity and incorporation response; UAE counsel memo; DFSA rule analysis and any written response; capital, staffing, office, audit, and ongoing-cost estimate | `[TBD]` |
| **Dubai mainland or non-financial free zone** | Which DET or free-zone activity precisely covers proprietary securities, virtual assets, and/or commodity exposure? Which federal or Dubai financial-services perimeter applies? Does the licensor require regulator consent? | Activity code and licence terms; licensor confirmation; UAE counsel memo; applicable federal/SCA analysis; office, substance, and cost estimate | `[TBD]` |
| **VARA path outside DIFC** | Is the entity conducting VA proprietary trading “in or from” Dubai? Which NOC, registration threshold, disclosure, ongoing supervision, AML/sanctions, custody, venue, and reporting requirements apply? Does any software, advice, management, transfer, or service activity require a VASP licence? | Commercial-licensor process; completed activity description; VARA NOC/registration/licence response as applicable; crypto operating-policy approval | `[TBD]` |
| **Other UAE alternative** | Is there a concrete operating reason to compare ADGM or another emirate/free zone? Which regulator, licensor, substance, banking, provider, and tax consequences differ? | Counsel-defined comparator using the same facts and cost horizon | `[not considered unless justified]` |

Starting sources:

- [DFSA General Module](https://dfsaen.thomsonreuters.com/entiresection/1873)
- [Invest in Dubai activity search](https://app.invest.dubai.ae/search-business-activities)
- [VARA licensed activities and proprietary-trading path](https://www.vara.ae/en/licenses-and-register/licensed-activities/)
- [VARA FAQs](https://www.vara.ae/en/faq/)
- [UAE corporate-tax legislation](https://tax.gov.ae/en/legislation/corporate.tax.aspx)
- [FTA Free Zone Persons guide](https://tax.gov.ae/Datafolder/Files/Guides/CT/Free%20Zone%20Persons%20-%2020%2005%202024%20final%20for%20GCD.pdf)

- **Selected option:** `[TBD]`
- **Rejected options and evidence:** `[TBD]`
- **Conditions and expiry of selection:** `[TBD]`

## 5. Entity, ownership, and capital provenance

- Legal name and form: `[TBD]`
- Incorporation authority and licence number: `[TBD]`
- Registered and operating addresses: `[TBD]`
- Financial year and reporting currency: `[TBD]`
- Direct shareholders and percentages: `[TBD]`
- Ultimate beneficial owners and control rights: `[TBD]`
- Directors, managers, and authorized signatories: `[TBD]`
- Related entities and transactions: `[TBD]`
- Initial capital amount, contributor, route, and currency: `[TBD]`
- Source of wealth and source of funds evidence: `[TBD]`
- Shareholder loans, leverage, guarantees, or liens: `[none / TBD]`
- Sanctions, PEP, adverse-media, and conflicts review owner: `[TBD]`
- UBO, corporate, accounting, and regulatory record-retention policy:
  `[TBD]`

Evidence must cover the complete ownership chain, control by means other than
shares, funding bank trail, resolutions authorizing capital and accounts, and
provider-specific KYC refreshes. Starting sources:
[UAE beneficial-ownership procedures](https://www.moec.gov.ae/en/-/ministry-of-economy-reviews-cabinet-resolution-on-the-organization-of-real-beneficiary-procedures-and-its-role-in-supporting-the-competitiveness-of-the-business-environment)
and the [UAE AML overview](https://u.ae/en/information-and-services/business/combatting-money-laundering).

## 6. Tax, substance, accounting, and reporting

Obtain written UAE and destination-market tax advice covering:

- [ ] UAE tax residence and corporate-tax registration.
- [ ] Whether free-zone treatment is available for the exact income and
      activities; no assumed zero rate.
- [ ] Adequate substance, premises, employees, expenditure, and decision-making.
- [ ] Qualifying and excluded income, permanent establishments, and elections.
- [ ] Transfer pricing and related-party or connected-person transactions.
- [ ] VAT treatment and any financial-services exemption questions.
- [ ] Accounting framework, audit, valuation, and books-and-records retention.
- [ ] FATCA/CRS status, registrations, self-certifications, and reporting.
- [ ] Foreign withholding, capital gains, dividends, interest, and tax reclaims.
- [ ] Controlled-foreign-company, management-and-control, and personal tax
      consequences for founders or owners in other jurisdictions.

**Tax adviser conclusion and limitations:** `[evidence ID and summary]`

## 7. Banking and treasury feasibility

Record evidence from at least two institutions where practical.

| Requirement | Bank A | Bank B | Status |
| --- | --- | --- | --- |
| Entity and licensed-activity eligibility | `[TBD]` | `[TBD]` | Proposed |
| Proprietary trading accepted | `[TBD]` | `[TBD]` | Proposed |
| Securities/crypto/commodity flows accepted | `[TBD]` | `[TBD]` | Proposed |
| USD, AED, INR, and required currency rails | `[TBD]` | `[TBD]` | Proposed |
| Broker/custodian transfers and beneficiary controls | `[TBD]` | `[TBD]` | Proposed |
| Source-of-funds and ongoing KYC requirements | `[TBD]` | `[TBD]` | Proposed |
| Dual approval, limits, alerts, and API capability | `[TBD]` | `[TBD]` | Proposed |
| Fees, minimum balance, reserves, and timeline | `[TBD]` | `[TBD]` | Proposed |

Banking is not cleared by an account opening alone. The bank must understand the
actual funded markets and flows. Treasury policy must forbid third-party
receipts and payments and require maker-checker approval.

## 8. Broker, custodian, venue, and data-provider feasibility

Create one row per exact legal entity/provider/account combination.

| Provider | Role and markets | Entity eligibility confirmed | Own-capital/API use confirmed | Custody and asset location | Data classification and rights | Evidence ID | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `[TBD]` | `[broker / custodian / venue / data]` | `[TBD]` | `[TBD]` | `[TBD]` | `[TBD]` | — | Proposed |

Written provider evidence must address:

- legal entity, domicile, beneficial owners, licensed activity, and tax status;
- account owner and permitted proprietary activity;
- each market, asset class, venue, order type, and API;
- custody chain, asset protection, cash and securities location, and insolvency
  treatment;
- professional/nonprofessional classification;
- display, non-display, historical, derived, retention, redistribution, and
  model-training rights;
- subaccounts, user counts, devices, environments, and geographic restrictions;
- paper/live endpoints, credentials, statements, fills, reconciliation, and
  incident support;
- restrictions on automation, AI, third-party software, or commercial use;
- onboarding, minimums, fees, insurance, limits, and termination.

Absence of a written right is a denied capability.

## 9. United States securities and tax questions

For a UAE entity proposing U.S. securities activity, obtain written U.S. legal
and tax answers for:

- entity-account and beneficial-owner onboarding;
- FATCA classification, GIIN if applicable, Form W-8BEN-E, withholding, and
  treaty position;
- whether activity creates a U.S. trade or business, permanent establishment,
  filing obligation, or effectively connected income;
- investor/trader/dealer status and how strategy, frequency, liquidity
  provision, affiliates, or services to others affect it;
- dividends, interest, capital gains, corporate actions, securities lending,
  withholding, and reclaim processes;
- broker-dealer, investment-adviser, CTA, or other perimeter questions caused
  by software publication, institutional use, or future services;
- SEC/FINRA/exchange/broker requirements and U.S. market-data non-display use;
- sanctions, restricted securities, ownership reporting, recordkeeping, and
  incident obligations.

Starting sources:
[IRS Form W-8BEN-E](https://www.irs.gov/forms-pubs/about-form-w-8-ben-e),
[SEC broker-dealer registration guide](https://www.sec.gov/answers/bdregis.htm),
and the
[UTP non-display declaration](https://www.utpplan.com/DOC/NonDisplayDeclaration.pdf).

- **First proposed U.S. capability:** `[TBD]`
- **U.S. counsel/tax evidence IDs:** `[TBD]`

## 10. Indian securities access

Do not start an institutional execution adapter until a current DDP or custodian
has assessed the exact UAE entity and ownership/control structure.

- [ ] FPI eligibility category and disqualifications assessed.
- [ ] DDP and custodian feasibility response obtained.
- [ ] UBO, investor-group, common-control, and beneficial-owner aggregation
      assessed.
- [ ] PAN, KYC, tax, treaty, bank, demat, custody, and repatriation path mapped.
- [ ] Investment limits, restricted instruments, disclosure thresholds, and
      reporting mapped.
- [ ] Broker, exchange, algo registration/tagging, static-IP, authentication,
      and strategy-change treatment confirmed.
- [ ] NSE/BSE display, non-display, historical, derived, retention, and
      model-training data rights confirmed.
- [ ] INR funding, FX, settlement, fees, taxes, corporate actions, and
      reconciliation mapped.
- [ ] Research/sandbox remains unable to reach live Indian accounts.

Starting sources:
[SEBI FPI Regulations](https://www.sebi.gov.in/sebi_data/attachdocs/dec-2025/1765192425627.pdf),
[NSDL FPI onboarding](https://pilot.fpi.nsdl.co.in/HomePage/FrmHomePage.aspx),
and
[SEBI retail-algo framework](https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html).

- **DDP/custodian contacted:** `[TBD]`
- **Feasibility evidence ID and expiry:** `[TBD]`

## 11. Crypto and VARA

The initial institutional crypto profile, if approved, must remain spot-only,
unleveraged, allowlisted, and incapable of withdrawal or transfer.

- Exact activity description supplied to commercial licensor: `[TBD]`
- VARA NOC, registration, licence, or other written treatment: `[TBD]`
- Trading-volume registration threshold and monitoring owner: `[TBD]`
- Approved venues, custody model, asset location, and insolvency treatment:
  `[TBD]`
- AML/sanctions, blockchain analytics, Travel Rule, and recordkeeping
  applicability: `[TBD]`
- Fiat rails, stablecoins, staking, lending, borrowing, derivatives, DeFi,
  wallets, transfers, and withdrawals: `[all disabled unless separately cleared]`
- 24/7 staffing, venue outage, key compromise, asset suspension, fork, and
  incident controls: `[TBD]`
- Key permissions independently verified at venue: `[TBD]`

Any customer-facing activity, custody, transfer, advice, management, lending,
broker-dealer service, exchange service, or issuance is outside this packet and
remains disabled. See the
[VARA licensed-activities page](https://www.vara.ae/en/licenses-and-register/licensed-activities/).

## 12. Commodity instrument decision

| Option | Initial decision | Required evidence before change |
| --- | --- | --- |
| Unleveraged listed commodity ETFs | `[paper only / TBD]` | Securities, broker, data, tax, concentration, and product-allowlist approval |
| Physically backed exchange-traded products | `[disabled / TBD]` | Structure, custody, redemption, tax, sanctions, and issuer-risk review |
| Commodity futures | `Deferred` | Regulatory perimeter, broker/exchange permission, professional data rights, margin, position limits, expiry, rolling, first notice, delivery, overnight risk, and operations |
| Options, swaps, CFDs, leveraged/inverse products | `Disabled` | Separate product, legal, risk, and governance approval |

**Founder decision:** Are securities-based proxies sufficient for the first two
years? `[yes / no / evidence required]`

## 13. Governance and operating roles

Name a primary and backup for every role. A person may hold multiple roles only
where counsel, provider rules, and the approved segregation-of-duties matrix
allow it.

| Role | Primary | Backup | Authority | Prohibited combination or action |
| --- | --- | --- | --- | --- |
| Board / governing body | `[TBD]` | `[TBD]` | Strategy, risk appetite, markets, providers | Cannot delegate live authority to Hermes |
| Executive accountable owner | `[TBD]` | `[TBD]` | Operations within board policy | Cannot self-review all incidents |
| Compliance / MLRO as applicable | `[TBD]` | `[TBD]` | Perimeter, AML, sanctions, reporting | Cannot suppress a risk or reconciliation halt |
| Investment proposer | `[TBD]` | `[TBD]` | Submit evidence-backed proposals | Cannot approve own proposal alone |
| Mandate approver | `[TBD]` | `[TBD]` | Maker-checker approval | Cannot change deterministic risk in approval flow |
| Risk owner | `[TBD]` | `[TBD]` | Limits, independent challenge, halt | Cannot be Hermes |
| Execution operator | `[TBD]` | `[TBD]` | Release approved mandates | Cannot access policy administration |
| Reconciliation owner | `[TBD]` | `[TBD]` | Independent books/provider comparison | Cannot auto-trade to cure a break |
| Security / key custodian | `[TBD]` | `[TBD]` | Secrets, signing, incident containment | Cannot expose credentials to Hermes |
| Tax and finance owner | `[TBD]` | `[TBD]` | Books, filings, valuations, treasury | Cannot accept third-party funds |

Record board resolutions, delegated authorities, approval thresholds, conflicts,
access reviews, key ceremonies, incident escalation, business continuity,
record retention, independent code/security review, and live rearming.

## 14. Adviser question list

Each response must describe facts assumed, jurisdictions covered, limitations,
effective date, change triggers, and whether regulator or provider confirmation
is also required.

### UAE legal and regulatory counsel

1. Which domicile, legal form, and licensed activities fit the exact proprietary
   securities, crypto, and commodity plan?
2. What activity falls within the DFSA, SCA/federal, VARA, or another perimeter?
3. What written pre-application, NOC, registration, licence, or exemption
   determination is appropriate?
4. Does any affiliate, open-source, support, data, IP, or software activity turn
   the model into a service to another person?
5. What governance, capital, substance, AML/sanctions, UBO, reporting,
   cybersecurity, recordkeeping, and audit requirements apply?
6. What changes would invalidate an own-account-only conclusion?

### UAE tax and accounting advisers

1. What tax status and filings apply to each domicile candidate and income type?
2. Do free-zone qualifying-income rules apply to the exact trading and software
   facts, and under what continuing conditions?
3. What substance, transfer-pricing, VAT, accounting, audit, valuation, FATCA,
   CRS, and record-retention duties apply?
4. What founder-residency, management-and-control, permanent-establishment, or
   controlled-entity exposures exist outside the UAE?

### Destination-market counsel and providers

1. Can this exact UAE entity open and automate the proposed account?
2. What investor/trader/dealer, FPI, algo-provider, adviser, CTA, market-access,
   tax, AML, sanctions, reporting, and data classifications apply?
3. Which instruments, venues, APIs, order types, data uses, and custody models
   are permitted in writing?
4. Which activity or system change requires re-onboarding or new approval?

## 15. Go/no-go gates

| Gate | Required evidence | Owner | Status |
| --- | --- | --- | --- |
| G1 — Charter | Approved dual-use and own-account attestations; client activity disabled | Board | NO-GO |
| G2 — Domicile/perimeter | Comparative memo, selected domicile, activity licence, and required regulator/licensor responses | UAE counsel | NO-GO |
| G3 — Entity/capital | Formation, UBO/control, source-of-funds, sanctions, and capital evidence | Board / compliance | NO-GO |
| G4 — Tax/substance | UAE and destination-market advice, registrations, accounting, audit, and substance plan | Tax owner | NO-GO |
| G5 — Banking | Funded corporate bank account approved for disclosed flows and dual controls | Treasury | NO-GO |
| G6 — Providers/data | Written entity, API, custody, instrument, and data-right eligibility | Operations | NO-GO |
| G7 — Market-specific | U.S., India, crypto, or commodity evidence complete for one narrowly defined capability | Counsel / compliance | NO-GO |
| G8 — Governance | Roles, maker-checker, reconciliation, incidents, records, and key management approved and rehearsed | Board | NO-GO |
| G9 — Technical safety | M5 controls complete; separate live environment, mandate, deterministic risk, reconciliation, kill switch, and independent security review proven | Engineering / risk | NO-GO |
| G10 — Final capability | Dated and signed capability tuple approved with evidence hashes and expiry | Board / counsel / risk | NO-GO |

The final capability record must bind:

```text
legal_entity
operating_context = INSTITUTIONAL_PROPRIETARY
capital_owner
broker_or_venue_account
jurisdiction
market
asset_class
instrument_allowlist
data_entitlements
approval_policy
legal_evidence_hash
provider_evidence_hash
tax_evidence_hash
security_review_hash
effective_from
effective_until
```

**Automatic NO-GO conditions:** missing or expired evidence; oral-only advice;
unclear beneficial ownership or funds; third-party capital or authority;
customer activity; provider terms that do not cover the exact automation or
data use; unresolved regulatory, tax, sanctions, custody, reconciliation, or
security issue; Hermes access to credentials or policy; shared individual and
institutional state; or any requested capability outside the signed tuple.

## 16. Evidence register

Do not store credentials, identity documents, bank statements, or confidential
advice in the public repository. Store only an opaque evidence ID, safe summary,
hash, owner, location, permissions, effective date, and expiry.

| ID | Decision/gate | Evidence type and safe description | Issuer/adviser/provider | Effective date | Expiry/review trigger | Confidential location | SHA-256 | Verified by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `E-001` | `[TBD]` | `[TBD]` | `[TBD]` | `[YYYY-MM-DD]` | `[date/event]` | `[vault reference]` | `[hash]` | `[name/date]` |

## 17. Decision and review log

| Date | Decision or reopened question | Evidence IDs | Approvers | Next review |
| --- | --- | --- | --- | --- |
| `[YYYY-MM-DD]` | `[TBD]` | `[TBD]` | `[TBD]` | `[date/event]` |

Final M1 completion requires dated approval from helm's governing body and
accountable risk and compliance owners. That internal decision must be
supported by scoped, dated written opinions or deliverables from UAE legal and
tax advisers and the owner of each relevant market-specific review, with their
limitations recorded. M1 completion permits engineering planning and paper
rehearsal only; funded activation remains independently gated by M11B.
