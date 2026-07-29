# Operating contexts

helm's technical core supports multiple operating contexts, but their authority
and data must remain separate.

## Supported design contexts

### Individual self-directed

An individual uses helm for accounts and capital they own. The authenticated
owner may approve mandates within the locally configured policy, but Hermes
cannot exercise that approval.

### Institutional proprietary

A proposed Dubai-based helm entity uses helm only for the entity's own capital.
Institutional operation requires explicit roles, segregation of duties,
portfolio and account limits, maker-checker approvals, independent
reconciliation, record retention, and incident governance.

The proposed location or own-capital model is not a claim of regulatory
authorization. Entity structure, financial-free-zone choice, regulatory
perimeter, broker onboarding, data status, tax, AML/sanctions, market access,
and reporting require qualified review.

### Client activity

Advising, managing, executing, pooling, or holding assets for clients is not a
supported context. It must remain disabled unless separately designed,
reviewed, and authorized.

## Resource hierarchy

The planned control-plane hierarchy is:

```text
LegalEntity
└── OperatingContext
    └── Workspace
        └── Portfolio
            └── BrokerOrVenueAccount
                ├── Mandate
                ├── Order and fill ledger
                ├── Reconciliation state
                └── Audit events
```

Hermes memory and sessions belong to one workspace. Credentials, positions,
orders, mandates, audit state, and kill switches belong to the specific entity,
portfolio, and account. No context may read or inherit another context's
authority.

## Authority model

An authorized principal commits a mandate:

- In the individual context, this is the verified account owner.
- In the institutional context, this is the role or approval quorum defined by
  the entity's governance policy.
- Hermes is never an authorized principal.

Authentication proves identity; policy determines authority. Any change to
entity, context, account, market, asset class, broker, data entitlement,
approval policy, or capability expiry requires a new authorization decision.

## Live isolation

Each live capability is separately compiled, signed, deployed, and revocable.
Individual and institutional operation use separate credentials, secrets,
databases, account identifiers, signing keys, capability manifests,
reconciliation state, and audit exports.

Paper success proves technical behavior only. It does not prove broker
eligibility, data rights, regulatory classification, or permission to trade.

## Institutional decision gates

Before forming or funding the proposed institution, qualified UAE counsel and
tax advisers should compare the relevant legal and regulatory perimeters. The
decision packet should include:

- DIFC and the DFSA financial-services perimeter.
- Dubai mainland or non-financial-free-zone formation and the applicable
  federal capital-markets perimeter.
- VARA NOC, registration, or licensing treatment for proprietary virtual-asset
  activity outside DIFC.
- Other UAE alternatives only where there is an operating reason to consider
  them.
- Corporate tax, qualifying-free-zone, substance, beneficial ownership,
  transfer-pricing, VAT, and accounting consequences.
- Broker, bank, custodian, and professional market-data onboarding for the
  exact entity and own-capital activity.
- U.S. corporate-account, tax-documentation, dealer-versus-trader, and
  non-display-data questions.
- A DDP/custodian opinion on FPI eligibility and onboarding before building
  Indian institutional execution.

Starting references include the
[DFSA General Module](https://dfsaen.thomsonreuters.com/entiresection/1873),
[VARA FAQs](https://www.vara.ae/en/faq/),
[UAE corporate-tax legislation index](https://tax.gov.ae/en/legislation/corporate.tax.aspx),
[SEBI FPI regulations](https://www.sebi.gov.in/sebi_data/attachdocs/dec-2025/1765192425627.pdf),
and [NSDL FPI onboarding](https://pilot.fpi.nsdl.co.in/HomePage/FrmHomePage.aspx).
These are starting points, not legal conclusions.
