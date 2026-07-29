# helm: July 2026 product, regulatory and architecture roadmap

> [!IMPORTANT]
> This is a preserved ChatGPT Deep Research snapshot supplied to the helm project.
> It has not been independently validated by helm maintainers and is not legal,
> tax, regulatory, or investment advice. Provider terms, prices, eligibility, and
> regulatory facts must be revalidated before use. The Dubai institutional
> proprietary-trading context was identified after this research cut-off and is
> addressed separately in the maintained [product roadmap](../roadmap.md).

**Research cut-off:** July 29, 2026
**Scope:** U.S. equities, Indian equities, spot crypto, commodity ETFs and later commodity futures.

This is product and regulatory research, not legal or investment advice. It does not recommend any security, strategy or trade. Before public release, monetization or live execution, helm needs written advice from U.S. securities counsel, Indian securities counsel and—before futures—U.S. commodities counsel.

### Evidence labels

* **Confirmed fact:** directly supported by a regulator, exchange, broker or official project source.
* **Product inference:** a recommended product decision derived from the facts.
* **Unresolved legal question:** requires jurisdiction-specific counsel; user consent alone does not resolve it.

---

# 1. Executive recommendation

## Recommended launch

**Launch first with U.S. equities and U.S.-listed ETFs for one U.S.-resident, self-directed user, in read-only and paper-trading modes.**

The first live pilot should be:

* One approved U.S.-resident natural person.
* One cash brokerage account.
* Long-only U.S.-listed equities and unleveraged ETFs.
* Regular market hours.
* Whole-share `DAY LIMIT` orders only.
* No discretion, shorting, margin, options, OTC securities, crypto transfers or derivatives.
* A small founder-defined risk budget.
* Alpaca as the first paper/live adapter.
* Daily independent reconciliation.
* Market-specific live activation compiled and signed separately from the paper build.

This is a **product inference**, not a regulatory safe harbor.

Alpaca provides a realistic real-time paper environment using substantially the same API shape as live trading, supports equity and crypto simulation, exposes order-update streaming, and offers a relatively simple API-key development path. Its free market-data tier is limited to IEX for real-time equities, while the current $99/month Algo Trader Plus plan provides all-U.S.-exchange coverage, broader streaming and higher market-data limits. ([Alpaca US][1])

## Why not India live first?

India is an excellent second market, but not the simplest first live market. SEBI’s retail-algorithmic-trading framework became applicable to all stock brokers on **April 1, 2026**. It introduces explicit broker responsibility, algo registration/tagging, vendor or algo-provider relationships, authentication and static-IP requirements, and special treatment for black-box algorithms. ([Securities and Exchange Board of India][2])

India should therefore begin as:

1. A read-only NSE/BSE research profile.
2. A local simulator.
3. An Upstox sandbox adapter.
4. A single-user own-account paper pilot.
5. Live execution only after a broker confirms helm’s exact classification and onboarding path in writing.

## Core product boundary

The genuine product is not “an LLM that trades.” Several brokers already expose direct APIs, MCP servers or agent skills capable of trading. Alpaca promotes an MCP server tied to its Trading API, while Upstox publishes agent skills with order execution and sandbox support. ([Alpaca][3])

helm’s defensible differentiation should be:

> **An independent deterministic authorization, risk, execution, reconciliation and audit layer between an untrusted conversational agent and regulated market infrastructure.**

Hermes may research, explain, learn approved preferences and prepare proposals. It must not possess the authority or secrets required to execute those proposals.

---

# 2. Recommended market and customer-jurisdiction order

| Priority | Market                                         | Supported customer jurisdiction                              | Mode                                    | Recommendation                                                          |
| -------- | ---------------------------------------------- | ------------------------------------------------------------ | --------------------------------------- | ----------------------------------------------------------------------- |
| 1        | U.S. equities and unleveraged U.S.-listed ETFs | U.S.-resident self-directed user                             | Research → paper                        | First public technical profile                                          |
| 2        | U.S. equities and ETFs                         | One counsel-approved U.S. pilot user                         | Restricted live                         | First live pilot                                                        |
| 3        | Indian equities and Indian-listed ETFs         | Indian resident using own account                            | Research → local paper → Upstox sandbox | Build while U.S. paper is soaking                                       |
| 4        | Spot crypto                                    | Eligible U.S. state/jurisdiction and broker/exchange account | Paper first                             | Add only after equity controls are stable                               |
| 5        | Indian equities                                | Indian resident using own account                            | Restricted live                         | Only through a broker-approved SEBI algo path                           |
| 6        | Commodity ETFs                                 | Same jurisdiction as listing                                 | Paper → live                            | Treat as equity instruments operationally                               |
| 7        | Commodity futures                              | Jurisdiction-specific                                        | Paper only initially                    | Defer until CTA, exchange-data, margin and expiry controls are complete |

### Important jurisdiction qualification

Alpaca states that international accounts are available in many—but not all—countries and directs applicants to confirm current country eligibility; Canada is specifically identified as unsupported. A business account intended for the entity’s own trading is also distinct from an account used to build services for others. Therefore, do not infer that an India-resident founder or an Indian company can use the same account arrangement as a U.S.-resident consumer pilot. ([Alpaca][4])

**Founder decision:** identify the actual first account holder, tax residence, state or country of residence, contracting entity and source of product revenue before committing to the live-market sequence.

---

# 3. Likely regulatory classifications

## 3.1 United States

### Investment adviser

**Confirmed fact:** the U.S. investment-adviser analysis generally examines whether a person is:

1. Providing advice or analyses concerning securities.
2. In the business of doing so.
3. Receiving compensation.

SEC guidance treats automated advisers as investment advisers where those elements are present. Robo-adviser guidance specifically discusses systems that gather clients’ financial circumstances, goals and preferences and then generate or manage portfolios. Registered advisers remain subject to fiduciary, disclosure, suitability-related and compliance obligations even when the advice is automated. ([SEC][5])

**Product inference:** Hermes learning a user’s goals, risk preferences, holdings and constraints, then proposing security-specific actions at particular times, is much closer to personalized advisory activity than to a generic research publication.

The publisher exclusion is a weak foundation for this product because the SEC’s treatment of that exclusion focuses on bona fide, general and impersonal publications rather than advice adapted to the needs or portfolio of a particular person. ([SEC][6])

**Unresolved legal question:** whether free open-source distribution, paid support, hosting, data subscriptions, broker referral payments, commercial licensing, donations or another economic benefit would constitute direct or indirect compensation.

User approval does **not** by itself prevent adviser status. An adviser can make recommendations without discretionary authority over the account.

### Broker-dealer

**Confirmed fact:** broker status can arise from being engaged in the business of effecting transactions in securities for the account of others. SEC guidance identifies relevant factors such as solicitation, negotiation or execution participation, handling customer funds or securities, transaction-based compensation and facilitating securities transactions. ([SEC][7])

**Product inference:** helm’s risk is lower when:

* It never opens or funds accounts.
* It never handles assets.
* It receives no transaction-based or asset-based compensation.
* The customer independently contracts with the broker.
* The broker performs KYC, custody, routing, confirmations and statements.
* helm does not solicit particular trades or broker relationships.
* Execution is limited to a user’s own account.

But those facts do not establish a safe harbor. Automatically routing a personalized recommendation, transmitting a pre-filled order or being paid based on completed trades may materially increase broker-dealer risk.

### “Algo provider”

The United States does not have one generally applicable federal registration category called a retail-equity “algo provider” that substitutes for investment-adviser or broker-dealer analysis.

**Product inference:** the primary federal classifications remain investment adviser, broker-dealer and, for derivatives, CTA or related CFTC/NFA status. Broker market-access controls, FINRA obligations, exchange rules and broker API terms may nevertheless impose controls on third-party algorithms.

### Commodity trading adviser

**Confirmed fact:** a CTA generally includes a person who, for compensation or profit, engages in the business of advising others—or issuing analyses or reports—about futures, commodity options, swaps and certain other commodity-interest transactions. Discretion over the account is not a prerequisite. ([Commodity Futures Trading Commission][8])

Therefore:

* Advice on a gold or oil **ETF** is principally securities advice.
* Advice on gold, crude-oil or index **futures** can raise CTA questions.
* User approval before every futures order does not necessarily avoid CTA status.
* Backtests and hypothetical results introduce separate disclosure and advertising issues.

### Spot crypto

Spot crypto requires an activity- and asset-specific analysis:

* Some assets or arrangements may implicate securities laws.
* Derivatives implicate CFTC/CTA analysis.
* Custody, exchange, transmission or wallet-transfer functions can introduce money-transmission and AML issues.
* State availability and exchange eligibility vary.

A narrow 2026 SEC staff position concerning certain noncustodial interfaces should not be generalized to helm: a system that merely formats user-defined parameters is meaningfully different from one that learns preferences and recommends trades. ([SEC][9])

---

## 3.2 India

### Investment adviser

**Confirmed fact:** SEBI’s investment-adviser framework covers personalized investment advice, including advice concerning investing, purchasing, selling or otherwise dealing in securities or investment products. Risk profiling and suitability are central to the regulated IA model. ([Securities and Exchange Board of India][10])

**Product inference:** a conversational system that uses an individual’s finances, portfolio, goals and risk preferences to recommend specific actions is likely to create a serious IA-classification question.

### Research analyst

SEBI’s Research Analyst FAQ distinguishes broad market commentary and general trends from specific security recommendations. Buy, sell or hold recommendations concerning identified securities are not converted into unregulated general commentary merely because an algorithm produced them. SEBI also treats value-added research supplied for an economic benefit as potentially being “for consideration,” even where the fee is not separately itemized. ([Securities and Exchange Board of India][11])

The IA and RA regulations were both shown by SEBI as last amended on November 25, 2025, as of the July 2026 regulatory listing. ([Securities and Exchange Board of India][12])

### Retail algorithmic-trading provider

Under SEBI’s February 4, 2025 circular:

* API-generated automated orders come within the retail-algo framework.
* The broker is the principal for API-based algos.
* An algo provider or fintech vendor can act as the broker’s agent.
* Orders require exchange identifiers or tags.
* Brokers must obtain exchange permission or registration for applicable algorithms.
* APIs are to use prescribed security controls, including unique client/vendor credentials, OAuth-style authorization, two-factor authentication and static-IP controls.
* A black-box algo provider must register as a Research Analyst and maintain a detailed research report.
* A narrower treatment exists for certain self-developed algorithms below an exchange-defined order-per-second threshold, but that is not a general commercial-product exemption. ([Securities and Exchange Board of India][13])

The implementation circular confirms that this framework applies to all stock brokers from **April 1, 2026**. ([Securities and Exchange Board of India][14])

**Unresolved legal question:** whether Hermes-generated strategies are “black box.” Even where helm’s risk checks are deterministic and fully disclosed, the upstream strategy-generation process may still be considered opaque unless the recommendation methodology is sufficiently explainable, reproducible and documented.

### Stock broker, portfolio manager or account-handling service

Additional questions arise if helm:

* Controls the account continuously.
* Exercises standing discretion.
* pools or manages assets.
* opens accounts or solicits brokerage.
* receives trade-linked compensation.
* places orders for unrelated users through a commercial arrangement.

SEBI issued a February 2026 caution concerning stock-market account-handling services, reinforcing the need to avoid positioning helm as an account manager. ([Securities and Exchange Board of India][15])

### Indian spot crypto

FIU-IND’s January 8, 2026 VDA guidelines apply to reporting entities providing specified VDA-related services and cover registration, customer due diligence, monitoring, reporting and recordkeeping. A local tool that merely submits a user’s own order to an already regulated exchange may not perform all the activities of a VDA service provider, but custody, wallet transfers, exchange, broking or arranging transactions can change the analysis. ([Financial Intelligence Unit][16])

---

# 4. Broker and data-provider comparison

Prices and limits can change. helm should maintain them as dated capabilities in a provider manifest rather than hard-coding them into business logic.

## 4.1 U.S. equities

| Provider                | Paper environment                                                                                 | Live coverage and order support                                                                                             | Data, events and limits                                                                                                                                                                                                    | Authentication and reconciliation                                                                                                                                                                                     | Commercial constraints                                                                                                                          | helm verdict                                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Alpaca**              | Real-time simulated equities and crypto; same broad API workflow as live, but no exchange routing | U.S. equities/ETFs; market, limit, stop, stop-limit, trailing-stop; simple, bracket, OCO and OTO classes; multiple TIFs     | Free Basic data: real-time IEX, limited WebSocket symbols and 200 market-data calls/minute. Algo Trader Plus: $99/month, all U.S. exchanges, broader streaming and up to 10,000 calls/minute. Order updates over WebSocket | API key/secret for direct account; OAuth for platform integrations; REST snapshots plus `trade_updates` for order lifecycle                                                                                           | Personal account, business own-trading account and “build apps/services” relationships are distinct. International availability is case-by-case | **Best V1 paper and first live adapter** ([Alpaca US][1])                                                             |
| **Interactive Brokers** | Paper account available to funded/approved clients and supports broad simulated functionality     | Stocks, ETFs, options, futures, currencies, bonds and funds across a very broad global footprint; extensive order catalogue | Market-data subscriptions and entitlements vary. TWS API has a 50-message/second outbound limit; historical-data pacing rules apply                                                                                        | TWS or IB Gateway is operationally heavier and requires authenticated desktop/gateway infrastructure; Client Portal API also supports paper/live; detailed callbacks for orders, executions, errors and account state | Jurisdiction, entity and instrument permissions vary; professional/nonprofessional data classifications matter                                  | **Best long-term multi-asset adapter; too operationally heavy for the first four months** ([Interactive Brokers][17]) |
| **Tradier**             | Sandbox with paper balances and delayed market data                                               | U.S. equities and options; market, limit, stop and stop-limit plus OTO/OCO/OTOCO workflows                                  | Production standard/market-data limits around 120 requests/minute and sandbox around 60; account and market streaming available. Consolidated real-time data is tied to eligible brokerage accounts                        | Personal tokens for own account; OAuth for partner apps; streaming plus REST order/account recovery                                                                                                                   | Primarily U.S.-centric; public or multi-user applications require a proper partner arrangement                                                  | **Good secondary U.S. adapter, especially for options later** ([Tradier API][18])                                     |

### U.S. data-vendor strategy

For V1, do not buy a large institutional feed. Use:

* Broker-provided data for the named single user.
* A written confirmation that algorithmic/non-display use is permitted.
* A separately licensed historical source only when the product’s retention or research requirements exceed the broker entitlement.
* No public redistribution of raw quotes, trades or bars.

---

## 4.2 Indian equities

| Provider                 | Paper/sandbox                                                                                                                           | Live API and data                                                                                                                    | Authentication, events and rate limits                                                                                                                                                                                      | Costs and restrictions                                                                                                                                                            | helm verdict                                                                                                                                        |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Zerodha Kite Connect** | No official full paper brokerage environment was found; helm would need a local simulator                                               | Orders for equities, commodities and other supported products; portfolio, margins, GTT, alerts, WebSocket data and order updates     | Redirect-based session workflow; active account/TOTP requirements; WebSocket order updates and public-app postbacks. Published operating limits include 10 orders/sec, 400/minute, 5,000/day and modification limits        | Personal order/portfolio APIs are free; current Connect tier with real-time WebSocket and historical candles is ₹500/month. Business integrations require discussion with Zerodha | **Strong live candidate after broker approval; weak paper path** ([Kite][19])                                                                       |
| **Upstox**               | Official sandbox, currently supporting core place/modify/cancel and related integration paths; one sandbox app and 30-day sandbox token | NSE/BSE and supported derivative/commodity segments; V3 orders, GTT, multi-order, portfolio, historical and Protobuf WebSocket feeds | OAuth2/bearer tokens, analytics token for selected read-only/data operations, Webhooks and WebSockets. Rate limits distinguish regular and registered algo use. Static-IP and algo changes are being incorporated           | Trading and data APIs are advertised as free; commercial use and exchange algo approval still require the correct arrangement                                                     | **Best India development and sandbox adapter; live only after explicit SEBI/broker classification** ([Upstox - Online Stock and Share Trading][20]) |
| **DhanHQ**               | No equivalent official full paper environment identified                                                                                | Orders, positions, portfolio, market quotes, option chain and real-time feeds; multiple Indian segments                              | 24-hour access tokens; static IP required for order APIs; real-time order WebSocket and postbacks; up to five market-data WebSockets with 5,000 instruments each; REST quotes up to 1,000 instruments at one request/second | Trading APIs free for individual Dhan users; data APIs have additional charges                                                                                                    | **Excellent second India adapter for data depth and order events** ([dhanhq.co][21])                                                                |
| **FYERS**                | No official complete paper environment confirmed                                                                                        | Trading, historical and WebSocket functionality; published agent/MCP-oriented tooling                                                | Current official skills page states 10 requests/sec, 200/minute, 100,000/day, daily token expiry and preference for WebSockets over polling                                                                                 | API access is promoted as zero-cost; exact commercial app terms need written confirmation                                                                                         | **Useful fourth adapter; do not prioritize over Upstox/Zerodha** ([Fyers API][22])                                                                  |

### India-specific caveat

A broker API being free and technically capable does not mean helm may commercially place automated orders without:

* The correct broker relationship.
* Exchange registration or tagging where required.
* Static-IP and authentication compliance.
* A determination of whether helm is an algo provider.
* RA or IA analysis.
* Approval of the exact strategy/update process.

---

## 4.3 Spot crypto

| Provider                    | Paper/sandbox                                                                                 | Live/order capabilities                                                                | Data/auth/events                                                                                                                 | Jurisdiction and commercial issues                                                                                                  | helm verdict                                                                                                |
| --------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Alpaca Crypto**           | Real-time crypto paper simulation in the same paper account                                   | Market, limit and stop-limit; GTC/IOC; quantity or notional support for eligible pairs | Same key model and event infrastructure as Alpaca Trading API                                                                    | Availability varies by account and jurisdiction; custody/execution arrangement is broker-specific                                   | **Use for V1 crypto paper after equity paper is stable** ([Alpaca US][1])                                   |
| **Coinbase Advanced Trade** | Static sandbox returns predefined responses; it is not a realistic matching or fill simulator | REST and WebSocket order management; limit, stop-limit and multiple TIF policies       | CDP API credentials and JWT signing; public and user WebSocket channels; rate limits depend on API family/account                | Product and asset availability depend on residence and account eligibility                                                          | **Strong U.S. live candidate; helm must supply its own simulator** ([Coinbase Developer Documentation][23]) |
| **Kraken**                  | No official realistic spot-paper environment confirmed                                        | Spot REST, WebSocket and FIX; broad order-management functionality                     | Private WebSocket access uses a token obtained through authenticated REST; tiered counter-based limits and reconnection controls | Jurisdiction and asset eligibility vary                                                                                             | **Good second live crypto adapter; build only after Coinbase/Alpaca** ([Kraken Developers][24])             |
| **CoinDCX**                 | No mature official paper environment identified in reviewed sources                           | Indian VDA trading APIs and public market-data endpoints                               | API authentication and public data endpoints; exact production limits and commercial rights require diligence                    | Only consider after FIU, tax, custody and product-classification review; exchange registration does not automatically regulate helm | **India-only candidate for a later phase** ([CoinDCX][25])                                                  |

For crypto V1, API keys must have **no withdrawal, transfer, address-book or funding permissions**. helm should never support wallet withdrawals in its initial architecture.

---

## 4.4 Commodity ETFs and futures

| Exposure                                          | Realistic partners                                                          | Paper/live path                                                                                                                            | Recommendation                                                                |
| ------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| U.S. gold, silver, energy or broad-commodity ETFs | Alpaca, IBKR, Tradier                                                       | Same API and licensing framework as U.S.-listed equities                                                                                   | Include only unleveraged ETFs that pass an explicit allowlist                 |
| Indian gold/silver ETFs                           | Zerodha, Upstox, Dhan, FYERS                                                | Same trading account as Indian equities, subject to product support                                                                        | Add after Indian cash equities                                                |
| U.S. commodity futures                            | IBKR; Tradovate as a futures-specific alternative                           | IBKR paper supports broad products; Tradovate advertises a simulation environment and futures API                                          | Defer until CTA, NFA, data, margin, expiry and delivery controls are complete |
| Indian commodity futures                          | Broker-specific MCX access, including some Zerodha/Dhan/Upstox capabilities | Support is subject to current broker and exchange implementation; Upstox instrument files include MCX but live API availability can change | Defer; do not infer capability from an instrument master alone                |

IBKR is the most realistic eventual multi-asset futures adapter because it combines paper trading, futures permissions, account/margin data and broad global-market coverage. Tradovate is a viable buy-versus-build candidate for a futures-specific pilot. ([Interactive Brokers][17])

---

# 5. Market-data licensing

Market-data licensing is one of helm’s highest non-obvious risks.

## Display data

Data rendered for a human on a screen may be licensed by:

* Named user.
* Device.
* application.
* Subscriber classification.
* Professional versus nonprofessional status.
* Location.
* Concurrent session.

A retail broker’s permission to show a quote in its own application does not necessarily grant helm the right to display the same quote in a separate application.

## Non-display data

Non-display use includes machine consumption for trading, algorithms, order generation, risk, valuation, surveillance and similar processing.

The 2026 UTP non-display declaration specifically includes automated order or quote generation, price referencing for algorithmic trading, order verification, risk, compliance and portfolio valuation. CTA’s corresponding policy similarly defines non-display use as consuming real-time market data for purposes other than display or redistribution. ([UTPPlan][26])

NSE’s non-display policy similarly covers automated calculations and algorithms supporting trading decisions or trading-platform operation. Its paid non-display product page was updated April 24, 2026. ([NSE India][27])

### Consequence for helm

A system can be:

* Self-hosted.
* Used by one person.
* Running on that person’s computer.
* Not showing data publicly.

…and still be performing licensable **non-display** use.

## Historical data

Historical rights must address:

* Which fields are included.
* Tick, quote, trade, bar or order-book depth.
* Maximum lookback.
* Retention.
* Local caching.
* Backtesting.
* Model training.
* Corporate-action adjustment.
* Whether expired contracts are included.
* Whether data can be combined across users.

NSE separately offers paid end-of-day and historical order/trade data and lists different delivery mechanisms and products. Its historical page was updated June 19, 2026. ([NSE India][28])

## Derived data

Examples include:

* Indicators.
* Volatility estimates.
* Rankings.
* Embeddings.
* Sentiment scores.
* Feature vectors.
* Strategy outputs.
* Synthetic prices.

Calling an output “derived” does not automatically grant the right to:

* Publish it.
* Sell it.
* reverse-engineer the underlying feed.
* distribute enough information to reconstruct the source.
* use source data to train a reusable commercial model.

NSE’s data policy retains ownership of licensed data and prohibits various unauthorized sharing and reverse-engineering activities. ([NSE India][29])

## Redistribution

Redistribution means sending licensed data to another:

* Person.
* application.
* server.
* device.
* customer.
* API consumer.
* hosted agent.
* model-training pipeline.

BSE’s published tariff separately refers to licenses for redistributing delayed data, illustrating that even delayed data can require an explicit redistribution right. ([BSE India][30])

## Required entitlement design

Every market datum in helm should carry:

```text
provider
feed_product
asset_scope
subscriber_class
display_right
non_display_right
historical_right
derived_data_right
redistribution_right
model_training_right
retention_limit
authorized_user
authorized_device_or_system
territory
effective_from
effective_until
source_timestamp
received_timestamp
```

The risk engine must fail closed when an entitlement is absent, expired or incompatible with the intended operation.

### Vibe-Trading requirement

Vibe-Trading should normally return:

* Source links.
* Small evidence excerpts.
* Dated derived facts.
* Entitlement metadata.
* Provider identifiers.
* Staleness information.

It should not become a bulk quote-feed cache or an accidental redistribution gateway.

---

# 6. Canonical multi-asset domain model

The model must separate **economic identity** from broker and venue symbols.

## Reference entities

### `Instrument`

Represents the stable economic instrument.

```text
instrument_id
asset_class
asset_subtype
issuer_id
underlier_id
name
isin
figi
cusip_or_local_identifier
base_currency
quote_currency
settlement_currency
status
valid_from
valid_to
```

### `Listing`

Represents a venue-specific tradable listing.

```text
listing_id
instrument_id
venue_id
venue_symbol
broker_symbol_map[]
exchange_token
segment
price_tick
quantity_step
minimum_quantity
minimum_notional
round_lot
odd_lot_allowed
freeze_quantity
price_precision
quantity_precision
trading_calendar_id
settlement_cycle_id
shortable
fractionable
status
```

Symbols and exchange tokens must never be primary identities. Upstox explicitly recommends its stable `instrument_key` because exchange tokens can be reused after expiry. ([Upstox - Online Stock and Share Trading][31])

### `DerivativeContract`

```text
contract_id
underlier_id
contract_type
expiry_date
last_trade_date
first_notice_date
delivery_date
settlement_method
contract_multiplier
strike
option_right
exercise_style
margin_group
position_limit
delivery_asset
roll_group
```

### `Venue`

```text
venue_id
mic
country
timezone
segments
session_calendar
auction_rules
halt_model
price_band_model
settlement_entity
```

### `MarketCalendar`

Must model session phases rather than only “open” or “closed”:

```text
pre_open
opening_auction
continuous
closing_auction
post_close
after_hours
overnight
special_session
holiday
unscheduled_halt
```

### `CorporateAction`

```text
action_id
instrument_id
type
announcement_date
ex_date
record_date
effective_date
payment_date
ratio
cash_amount
currency
new_instrument_id
source
adjustment_policy
```

Supported actions should include:

* Splits and reverse splits.
* Cash and stock dividends.
* Rights issues.
* Mergers.
* Spinoffs.
* Tender offers.
* Symbol changes.
* Delistings.
* Bonus issues.
* India-specific corporate-action forms.

## Account and lifecycle entities

```text
BrokerAccount
CashBalance
Position
PositionLot
SettlementObligation
MarginSnapshot
OrderIntent
DecisionProposal
Mandate
RiskDecision
ExecutionOrder
OrderEvent
Fill
Fee
Tax
CashMovement
CorporateActionPosting
ReconciliationRun
ReconciliationBreak
DataEntitlement
AuditEnvelope
```

## Mandatory numeric rule

All prices, quantities, FX values, fees and balances must use decimal arithmetic with explicit units and currencies. Never use binary floating-point for monetary state.

## Order state machine

```text
DRAFT_PROPOSAL
→ VALIDATED_PROPOSAL
→ APPROVED_MANDATE
→ RISK_ACCEPTED
→ RELEASED
→ BROKER_PENDING
→ BROKER_ACCEPTED
→ PARTIALLY_FILLED
→ FILLED / CANCELED / REJECTED / EXPIRED
→ RECONCILED
```

Unknown broker state is not equivalent to rejection. It must produce `PENDING_RECONCILIATION` and block unsafe retries.

---

# 7. Deterministic risk rules

These are engineering controls, not recommended investment parameters. All numerical limits must be supplied by the founder and reviewed for the pilot.

## Common fail-closed controls

Reject an order when any of the following is true:

* Instrument identity is ambiguous.
* Quote or reference data exceeds its maximum age.
* Market-data entitlement is missing.
* Venue or session state is unknown.
* Broker environment does not match the mandate environment.
* Clock drift exceeds tolerance.
* Account, cash or positions have not been freshly reconciled.
* An unresolved reconciliation break exists.
* Order intent has expired.
* Idempotency key has already been used.
* Existing broker order state is unknown.
* Corporate-action processing is pending.
* Instrument is halted, suspended or delisting.
* Order type, TIF, venue or asset class is not allowlisted.
* Live-market capability manifest is absent or has expired.
* Broker terms, legal approval or data approval version does not match the active build.
* Kill switch is active.

## Portfolio controls

* Maximum order notional.
* Maximum daily aggregate notional.
* Maximum gross and net exposure.
* Maximum concentration by instrument, issuer, sector, venue and asset class.
* Maximum number of open orders.
* Maximum order frequency.
* Cooldown after rejection or rapid price movement.
* Maximum realized and unrealized daily loss.
* Maximum peak-to-trough drawdown.
* Maximum spread.
* Maximum expected slippage.
* Minimum liquidity.
* Price collars around a validated reference.
* Daily and per-strategy turnover limits.

## U.S. equities and ETFs V1

* Cash account only.
* Long-only.
* Whole shares.
* Regular session only.
* `DAY LIMIT` orders only.
* No margin.
* No shorting.
* No options.
* No OTC securities.
* No leveraged or inverse ETFs.
* No newly listed instruments until a seasoning period passes.
* No order while an exchange halt or security-status uncertainty exists.
* Check settled and available cash separately.
* Freeze affected instruments around unresolved splits, mergers or symbol changes.
* Reject prices outside a deterministic bid/ask and volatility collar.

## Indian equities V1

* Delivery/CNC-equivalent product only.
* Long-only.
* Regular cash-market session.
* Limit orders only.
* No MIS, MTF, F&O, intraday leverage or short sale.
* Validate tick size, lot size, freeze quantity and price bands.
* Check suspended-instrument and broker BOD masters daily.
* Treat T+1 settlement obligations separately from current cash.
* Block on auction, short-delivery or corporate-action ambiguity.
* Require broker-supplied algo ID/tag where applicable.
* Require active static-IP, OAuth and second-factor compliance.
* Track the broker’s applicable orders-per-second classification.

## Spot crypto V1

* Spot only.
* No leverage.
* No borrowing.
* No perpetuals or futures.
* No withdrawal or transfer permissions.
* Allowlisted liquid base/quote pairs.
* Venue-specific minimum quantity and notional checks.
* Maximum spread and minimum depth.
* Volatility circuit breaker.
* Exchange-status heartbeat.
* Venue and asset concentration limits.
* Explicit 24/7 risk-day boundary, preferably UTC.
* No automatic re-entry after exchange outage.
* Reconciliation against exchange balances, fills and fees.

## Futures, when eventually added

* Cash-settled micro or index contracts first.
* No deliverable commodity contract without an explicit delivery process.
* Mandatory liquidation before first-notice and last-trade buffers.
* Contract rollover policy.
* Initial and maintenance margin buffers.
* Contract multiplier-aware notional limits.
* Position limits.
* Expiry-calendar validation.
* No naked options.
* No strategy activation without CTA and market-data review.

---

# 8. Architecture and trust boundaries

## Security principle

**Hermes must be treated as an untrusted, network-exposed proposal generator—even when it is running locally.**

Hermes supports MCP integrations, profiles and mutable skills. Because its tool and skill environment is extensible, helm must not place deterministic policy or broker secrets inside a Hermes profile or skill. ([GitHub][32])

## Proposed architecture

```text
┌─────────────────────────────────────────────────────────────┐
│ Zone A: Hermes                                              │
│ - Conversation, research planning, preference memory        │
│ - No broker credentials                                     │
│ - No policy administration                                  │
│ - No direct order, cancel, funding or withdrawal tools      │
└───────────────────────┬─────────────────────────────────────┘
                        │ read-only MCP + strict Proposal API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Zone B: Vibe-Trading read-only finance runtime              │
│ - Curated sources                                           │
│ - Entitlement labels                                        │
│ - Prompt-injection taint tracking                           │
│ - No execution capability                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │ evidence IDs and dated facts
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Zone C: helm control plane                                  │
│ - Canonical domain model                                    │
│ - Proposal schema validation                                │
│ - Mandate compiler                                          │
│ - Deterministic risk engine                                 │
│ - Capability manifest validation                            │
└───────────────┬───────────────────────────┬─────────────────┘
                │                           │
                │ signed approval request   │ events
                ▼                           ▼
┌─────────────────────────────┐   ┌───────────────────────────┐
│ Zone D: Policy admin        │   │ Zone F: Audit & recon     │
│ - Separate UI/CLI           │   │ - Append-only event log   │
│ - Separate authentication   │   │ - Hash-chain checkpoints  │
│ - Policy diffs and signing  │   │ - Broker reconciliation   │
│ - Live arming and revoking  │   │ - Immutable export        │
└───────────────┬─────────────┘   └───────────────────────────┘
                │ signed mandate
                ▼
┌─────────────────────────────────────────────────────────────┐
│ Zone E: Execution enclave                                   │
│ - Broker adapter                                            │
│ - Credential vault                                          │
│ - Outbound allowlist to approved broker hosts only          │
│ - Verifies signature, nonce, expiry and environment         │
│ - No policy-edit endpoint                                   │
│ - Emits sanitized events; never emits credentials           │
└─────────────────────────────────────────────────────────────┘
```

## Proposal contract

Hermes may submit only a typed `DecisionProposal`:

```json
{
  "proposal_id": "uuid",
  "user_goal_reference": "approved-goal-id",
  "strategy_version": "hash",
  "evidence_ids": ["source-record-id"],
  "assumptions": [],
  "candidate_orders": [],
  "valid_until": "timestamp",
  "uncertainties": [],
  "requested_market": "US_EQUITIES_PAPER"
}
```

It may not submit:

* Executable code.
* Shell commands.
* SQL.
* Broker URLs.
* API credentials.
* Policy changes.
* A generic natural-language instruction such as “buy the best one.”

## Mandate contract

The control plane converts an accepted proposal into a bounded mandate:

```text
approved instruments
maximum aggregate quantity/notional
permitted side
permitted order type
permitted venue
permitted session
start/end time
maximum price/slippage
number of permitted child orders
strategy hash
evidence hash
environment
account ID hash
single-use nonce
```

Any material change requires a new mandate and new approval.

## Credential boundary

Broker credentials must exist only in:

* OS keychain or hardware-backed secret store.
* A separate execution service.
* A dedicated operating-system identity.
* An environment Hermes cannot read.
* A database Hermes cannot query.
* Logs with secret redaction and canary detection.

For crypto, API keys must have trading and read access only. Withdrawal permissions must be disabled at the exchange, not merely hidden in helm’s UI.

## Policy-administration boundary

Hermes must not be able to:

* Raise limits.
* Add an instrument.
* change a live market.
* enable a new broker.
* approve itself.
* disable reconciliation.
* clear a risk halt.
* rotate broker credentials.
* rearm after a kill switch.

Policy administration should require a separate login and preferably a hardware-backed credential.

## Paper/live isolation

Use separate:

* Credentials.
* Broker endpoints.
* DNS allowlists.
* processes or containers.
* databases.
* signing keys.
* CI deployment targets.
* UI themes and persistent banners.
* account IDs.
* capability manifests.

Never select paper versus live from an LLM-generated parameter.

## Prompt-injection defenses

External filings, social posts, research pages and MCP responses are untrusted data. They cannot:

* Add tools.
* change instructions.
* modify mandates.
* invoke execution.
* alter data entitlements.
* request secrets.

Vibe-Trading should label content lineage and contamination risk. helm should accept evidence IDs, not instructions extracted from source text.

---

# 9. Competitive position

| System                     | Strength                                                      | What it already covers                                                     | What helm should not duplicate                                                                                   | Genuine helm differentiation                                                                                        |
| -------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **NautilusTrader**         | High-performance deterministic trading engine in Rust/Python  | Backtesting, live trading, order management, risk and multi-venue adapters | Do not rebuild a broad institutional-grade engine prematurely                                                    | Agent isolation, signed mandates, entitlement enforcement and human-governed live activation ([NautilusTrader][33]) |
| **QuantConnect LEAN**      | Mature open-source quant engine and broad brokerage ecosystem | Research, backtesting and live algorithm execution                         | Do not compete on strategy framework breadth or cloud backtesting                                                | Self-hosted conversational proposal layer with independently enforceable trust boundaries ([GitHub][34])            |
| **OpenBB**                 | Unified financial research and provider connectors            | Research workspace, data integration, MCP-oriented access                  | Consider using connectors rather than rebuilding every research integration; review AGPL/commercial implications | Vibe’s entitlement-aware read-only runtime plus execution separation ([OpenBB Docs][35])                            |
| **Freqtrade**              | Mature crypto-bot workflow                                    | Backtest, dry-run, strategy execution and exchange integrations            | Do not recreate a general crypto strategy bot                                                                    | Multi-jurisdiction, multi-asset mandate and governance model rather than crypto autonomy ([GitHub][36])             |
| **Hummingbot**             | Crypto market making and connectors                           | Exchange connectivity, order tracking and strategy execution               | Reuse lessons or adapters where licensing permits                                                                | No direct LLM execution; policy and credential separation; regulated-market path ([Hummingbot][37])                 |
| **Broker MCP/agent tools** | Fast direct conversational trading                            | Broker-native data, account access and execution                           | helm should not merely wrap the same endpoint in another chat interface                                          | An independent fail-closed control plane where the agent cannot execute or administer policy ([Alpaca][3])          |

## Positioning statement

> helm is an open-source, self-hosted trading control plane that converts conversational research into bounded, signed and auditable mandates, while keeping AI agents cryptographically and operationally separated from broker credentials, policy administration and direct execution.

That is meaningfully different from:

* A chatbot around a brokerage API.
* A strategy backtester.
* A generic autonomous trading bot.
* A portfolio dashboard.
* An MCP server that directly exposes `place_order`.

---

# 10. Staged roadmap and acceptance tests

## Stage 0 — Legal and product boundary

**Duration:** 2–3 weeks

### Build

* Jurisdiction and activity matrix.
* Product-mode definitions.
* Claims and marketing language policy.
* Data-use inventory.
* Broker-account/entity decision.
* Initial threat model.
* Open-source license decision.
* Counsel question packet.
* Architecture decision records.

### Acceptance tests

* Every feature is classified as research, paper or live.
* No documentation uses “financial adviser,” “portfolio manager,” “autonomous investor” or similar claims without counsel approval.
* No transaction-based or AUM-based revenue model is assumed.
* Every proposed data source has an entitlement owner.
* The first customer’s residence, legal entity and broker account type are documented.

---

## Stage 1 — Read-only Vibe-Trading runtime

**Duration:** 3–5 weeks

### Build

* Read-only MCP server.
* Curated source registry.
* Source timestamps and citations.
* Entitlement metadata.
* Corporate-action/news ingestion.
* Instrument lookup.
* Prompt-injection and provenance labels.
* Hermes profile with no trading tools.

### Acceptance tests

* Every market fact returned has source, `as_of`, `observed_at` and entitlement fields.
* No MCP method can submit, modify or cancel an order.
* No broker secret exists in the Hermes process, filesystem, environment or logs.
* A malicious instruction embedded in a news article cannot change tools or policy.
* Stale data is explicitly labeled rather than silently used.

---

## Stage 2 — Canonical domain and event ledger

**Duration:** 4–6 weeks

### Build

* Instrument/listing model.
* Venue and calendar model.
* Precision and lot-size engine.
* Account and position model.
* Event-sourced order ledger.
* Corporate-action skeleton.
* Data-entitlement enforcement.
* Reconciliation schema.

### Acceptance tests

Test fixtures must cover:

* A symbol change.
* Symbol reuse.
* Indian tick and freeze quantity.
* Fractional crypto quantity.
* U.S. split.
* Indian bonus issue.
* Futures expiry and multiplier.
* Different trade and settlement currencies.
* Partial fills and fees.
* Corporate-action-adjusted positions.

Ledger invariants:

```text
opening cash
+ cash movements
- purchases
+ sales
- fees
- taxes
= closing cash
```

All values must reconcile using decimal arithmetic.

---

## Stage 3 — Mandate compiler and deterministic risk

**Duration:** 4–6 weeks

### Build

* Strict proposal schema.
* Policy DSL.
* Mandate compiler.
* Deterministic risk evaluation.
* Signed decision envelope.
* Idempotency and replay protection.
* Kill switch.
* Market capability manifests.
* Property-based risk tests.

### Acceptance tests

* Same inputs and policy version produce the same risk-decision hash.
* Unsupported order types always reject.
* Missing or stale data rejects.
* An expired mandate rejects.
* Duplicate nonce rejects.
* A paper mandate cannot reach a live adapter.
* A policy diff cannot be approved by Hermes.
* Every rejection has a machine-readable rule ID.
* Property tests demonstrate no order exceeds a mandate bound.

---

## Stage 4 — Local simulator and Alpaca paper

**Duration:** 4–6 weeks

### Build

* Deterministic local fill simulator.
* Alpaca paper adapter.
* REST and WebSocket state recovery.
* Partial-fill handling.
* Cancel/replace workflows.
* Fee and cash modeling.
* Daily reconciliation.
* Broker capability discovery.
* Operational dashboard.

### Acceptance tests

* WebSocket disconnect followed by REST recovery produces one canonical order state.
* Late events do not generate duplicate orders.
* Unknown order state blocks replacement.
* Partial fills correctly update cash and positions.
* Cancel acknowledgement and subsequent fill are handled safely.
* Broker order book, fills, positions and cash reconcile daily.
* Any unresolved difference blocks new paper orders until disposition.

---

## Stage 5 — Paper soak and failure testing

**Duration:** 4–6 weeks, with at least 30 trading sessions

### Test scenarios

* Market-data outage.
* Broker REST outage.
* WebSocket loss.
* Duplicate webhook.
* Out-of-order events.
* Clock drift.
* stale quote.
* sudden price gap.
* market halt.
* corporate action.
* process restart.
* database restore.
* expired credentials.
* kill-switch activation.
* partial fill during shutdown.
* broker-side manual order.
* broker-side cancel.
* account balance changed outside helm.

### Exit criteria

* No unreconciled phantom position.
* No duplicate live-intent release.
* No silent recovery from unknown state.
* 100% of orders linked to proposal, mandate, risk decision and user approval.
* Recovery runbook tested by someone other than the code author.
* Reconciliation break rate is measured and categorized.
* A reproducible incident report can be generated from the event log.

---

## Stage 6 — One U.S. live-market pilot

**Duration:** approximately 6–8 weeks after paper exit criteria

### Preconditions

* Written U.S. counsel advice.
* Broker account and API use approved for the exact activity.
* Market-data rights confirmed in writing.
* Privacy and cybersecurity terms complete.
* Product liability and insurance decision made.
* Live adapter independently reviewed.
* Separate live deployment and signing key.
* Incident-response plan.
* Customer disclosures.
* No prohibited compensation structure.

### Live capability

```text
market: US_EQUITIES
customer_count: 1
account_count: 1
account_type: CASH
side: LONG_ONLY
session: REGULAR
order_type: DAY_LIMIT
fractional: false
shorting: false
margin: false
options: false
crypto: false
max_order_notional: founder_defined
max_daily_notional: founder_defined
expiry: dated
legal_approval_hash: required
data_approval_hash: required
broker_approval_hash: required
```

### Acceptance tests

* Live execution cannot start without all approval hashes.
* Credentials cannot be read from Hermes or the control plane.
* A live binary refuses a paper account and vice versa.
* Kill switch cancels eligible open orders and prevents new releases.
* All orders reconcile against broker confirmations and statements.
* A single unresolved reconciliation break disarms the market.
* Re-enabling live execution requires separate administrator authentication.

---

# 11. Build, buy and defer

| Capability                            | Decision                                           | Rationale                                                                  |
| ------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------- |
| Proposal schema and evidence contract | **Build**                                          | Core product boundary                                                      |
| Mandate and policy DSL                | **Build**                                          | Core differentiation and safety                                            |
| Deterministic risk engine             | **Build**                                          | Must be inspectable and independently testable                             |
| Canonical instrument/account model    | **Build**                                          | Required for broker independence                                           |
| Event ledger and reconciliation       | **Build**                                          | Core operational truth                                                     |
| Execution security gateway            | **Build**                                          | Central trust boundary                                                     |
| Entitlement enforcement               | **Build**                                          | Data-license risk cannot be delegated blindly                              |
| Broker/custody/exchange services      | **Buy/use regulated providers**                    | helm must not become custodian or exchange                                 |
| Real-time exchange data               | **Buy through broker/vendor**                      | Exchange licensing and infrastructure are expensive                        |
| Corporate-action and reference data   | **Buy when budget permits**                        | Difficult to maintain accurately across markets                            |
| Secret storage                        | **Use OS/HSM/cloud-vault primitives**              | Do not invent cryptography or key storage                                  |
| Observability                         | **Use established stack**                          | Standard infrastructure                                                    |
| Calendars                             | **Use library, validate against exchange sources** | Holidays and special sessions require updates                              |
| Backtesting engine                    | **Evaluate NautilusTrader or LEAN**                | Avoid building a broad quant engine                                        |
| Research connectors                   | **Evaluate OpenBB/provider SDKs**                  | Check AGPL and commercial compatibility                                    |
| Local fill simulator                  | **Build narrow V1 simulator**                      | Needed for deterministic tests and Indian brokers without full paper       |
| India sandbox                         | **Use Upstox sandbox**                             | Good integration path, not a substitute for local deterministic simulation |
| Multi-user account system             | **Defer**                                          | Multiplies advisory, privacy, entitlement and operational burden           |
| Options, margin and shorting          | **Defer**                                          | Materially expands risk and suitability obligations                        |
| Futures                               | **Defer**                                          | CTA, margin, data, expiry and delivery complexity                          |
| Strategy marketplace/copy trading     | **Defer indefinitely**                             | High regulatory and conduct risk                                           |
| Crypto wallets and withdrawals        | **Defer indefinitely**                             | Custody, AML and irreversible-loss risk                                    |
| Smart order routing                   | **Defer**                                          | Broker already provides routing; can create broker/market-access issues    |
| HFT/low-latency execution             | **Defer**                                          | Not aligned with conversational mandate model                              |
| Hosted SaaS                           | **Defer**                                          | Self-hosted single-user model is the safer initial boundary                |

---

# 12. Engineering sequence for a 1–2 person team

## Estimated sequence

| Weeks | Workstream                                   | Main output                                          |
| ----: | -------------------------------------------- | ---------------------------------------------------- |
|   1–2 | Product/legal boundary and threat model      | ADRs, jurisdiction matrix, initial counsel packet    |
|   3–6 | Vibe read-only MCP                           | Research sources, provenance, entitlements           |
|  7–10 | Canonical model and event ledger             | Instruments, accounts, events, reconciliation schema |
| 11–14 | Mandate DSL and deterministic risk           | Policy compiler, signed envelopes, property tests    |
| 15–18 | Simulator                                    | Deterministic fills, latency and failure scenarios   |
| 19–22 | Alpaca paper adapter                         | Orders, streams, REST recovery, reconciliation       |
| 23–26 | Paper soak and incident testing              | Operational evidence and runbooks                    |
| 27–30 | Security hardening and external review       | Isolation, vault, SBOM, signed builds                |
| 31–36 | Counsel/broker/data approvals and live pilot | One tightly constrained live capability              |

**Expected result:** robust paper system in roughly **18–24 weeks** and a credible one-market live pilot in approximately **28–36 weeks**, assuming experienced engineering and no extended broker/legal onboarding delays. This is an engineering estimate, not a promise.

## Appropriate use of AI coding agents

AI agents can accelerate:

* Adapter scaffolding.
* Generated SDK clients.
* Schema migrations.
* Property-test generation.
* Fixtures.
* Broker-doc diffing.
* Documentation.
* Static analysis.
* Failure-injection scenarios.
* Reconciliation reports.

AI agents must not independently:

* Change live limits.
* Approve mandates.
* edit production secrets.
* merge risk-engine changes.
* rotate signing keys.
* change CI signing policy.
* enable live markets.
* suppress failing tests.
* resolve reconciliation breaks.
* deploy directly to production.

Use isolated branches, pinned dependencies, mandatory human review and code-owner rules for:

```text
/risk
/execution
/policy
/credentials
/reconciliation
/migrations
/live-config
/ci-signing
```

---

# 13. Risk register

| Risk                                                 |        Likelihood |   Impact | Primary mitigation                                                                                            |
| ---------------------------------------------------- | ----------------: | -------: | ------------------------------------------------------------------------------------------------------------- |
| U.S. investment-adviser misclassification            |              High | Critical | Paper-only closed alpha; no personalization monetization until counsel; avoid misleading claims               |
| Broker-dealer exposure from routing or compensation  |       Medium–High | Critical | No transaction-based compensation, custody, solicitation or account onboarding; written counsel/broker review |
| Indian IA/RA/algo-provider noncompliance             |              High | Critical | India paper/sandbox first; broker empanelment and algo classification before live                             |
| Market-data license breach                           |              High |     High | Entitlement model; written non-display/retention rights; no raw redistribution                                |
| Prompt injection changes trading behavior            |              High |     High | Treat all research as tainted data; strict proposal schema; no direct tool execution                          |
| Broker credential exfiltration                       |            Medium | Critical | Separate execution enclave, scoped keys, no Hermes access, canary secrets                                     |
| Duplicate or stale orders                            |            Medium | Critical | Idempotency, nonces, state machine, REST recovery, unknown-state halt                                         |
| Reconciliation drift                                 |            Medium | Critical | Broker as external source of truth; daily and event-driven reconciliation; fail closed                        |
| Broker API breaking change or outage                 |              High |     High | Capability discovery, contract tests, circuit breaker and adapter version pinning                             |
| Instrument/symbol mapping error                      |            Medium |     High | Stable internal identities, dated broker mappings, corporate-action workflow                                  |
| Corporate-action error                               |            Medium |     High | Freeze affected instruments until position and reference data reconcile                                       |
| Crypto venue failure or jurisdiction change          |              High | Critical | Venue allowlist, no withdrawals, asset caps, jurisdiction manifest                                            |
| Futures expiry or physical delivery                  | High when enabled | Critical | Defer; mandatory expiry buffers and delivery-disabled contract allowlist                                      |
| AI-generated supply-chain vulnerability              |              High |     High | SBOM, dependency pinning, signed releases, secret scans and human review                                      |
| Open-source downstream misuse                        |            Medium |     High | Safe defaults, live code disabled by default, jurisdiction manifests, clear notices                           |
| Scope creep into autonomous portfolio management     |              High | Critical | Product-mode gates and governance; no standing discretion in V1                                               |
| Misleading backtests or performance claims           |            Medium |     High | Standardized assumptions, source data lineage and counsel-approved disclosures                                |
| Privacy breach involving portfolio/financial profile |            Medium |     High | Local-first encrypted storage, minimization, no unnecessary telemetry                                         |
| Single-founder operational failure                   |            Medium |     High | Runbooks, tested recovery, immutable backups and independent code review                                      |

---

# 14. Questions requiring regulatory counsel

## United States

1. Does helm or its operator provide “advice concerning securities” when Hermes makes individualized, security-specific proposals?
2. Which revenue forms constitute compensation: paid support, hosting, premium data, dual licensing, donations, referrals or broker rebates?
3. Is the activity “in the business” of giving advice even where the core software is open source?
4. Can any publisher or software-tool exclusion apply when output is personalized and portfolio-aware?
5. Would registration be at state or SEC level?
6. Could helm rely on the internet-adviser registration framework, and what operational requirements would follow?
7. Does transmitting an approved order to a broker constitute effecting, inducing or soliciting a securities transaction?
8. Do broker deep links, OAuth account linking or pre-filled orders change that analysis?
9. Can helm receive any broker referral or revenue-sharing compensation?
10. Does a standing mandate create discretionary authority?
11. Does helm ever have custody because of API permissions or withdrawal capability?
12. Which Regulation Best Interest obligations could apply through a broker relationship?
13. What recordkeeping applies to conversations, recommendations, approvals and model changes?
14. What rules apply to backtests, hypothetical performance and marketing?
15. What state money-transmission or financial-services laws apply to spot crypto?
16. Which supported crypto assets or staking products may be securities?
17. At what point would futures research or recommendations make the operator a CTA?
18. Is NFA membership or another exemption available for the exact futures model?
19. What privacy, cybersecurity, incident-notification and books-and-records rules apply?

## India

1. Does learning an individual’s goals, portfolio and risk tolerance make helm an Investment Adviser?
2. Does a security-specific buy/sell/hold or entry/exit proposal make helm a Research Analyst?
3. Does support, licensing, affiliate income or another benefit amount to “consideration”?
4. Is helm an algo provider or fintech vendor acting as a broker’s agent?
5. Can the self-developed, own-account route apply to an open-source installation?
6. What is the current broker/exchange orders-per-second threshold and how is it calculated?
7. Must every strategy be registered or tagged?
8. Is Hermes-generated strategy logic considered black-box?
9. What level of methodology disclosure is necessary to be white-box?
10. Who must maintain and update the research report for a black-box algorithm?
11. Does every model, prompt, skill or strategy change require reapproval?
12. Can helm be empaneled with multiple brokers?
13. What grievance, audit, cyber-resilience and recordkeeping duties attach?
14. Does a standing mandate create portfolio-management or account-handling status?
15. Can an overseas entity provide helm to Indian residents?
16. Does helm become a VDA service provider if it only transmits orders to a registered Indian exchange?
17. Would wallet, transfer or custody functionality trigger FIU reporting-entity status?
18. What Indian tax/TDS data responsibilities arise for crypto integrations?
19. What restrictions apply to market-data storage, non-display use, derived outputs and AI training?

---

# 15. Explicit founder decisions and unknowns

The following decisions are prerequisites, not implementation details:

1. **Who is the first user?** Country, U.S. state, tax residence and citizenship.
2. **Which entity publishes and supports helm?** Indian company, U.S. company, nonprofit or individual.
3. **Will the first live account belong to the founder or an unrelated customer?**
4. **Will helm be free, paid, hosted, supported commercially or broker-funded?**
5. **Will recommendations be security-specific or remain research summaries?**
6. **Will Hermes see complete holdings, income, net worth and risk profile?**
7. **Will every order require approval, or will time-bounded standing mandates exist?**
8. **Does “single user” mean the founder’s own account or one customer per installation?**
9. **Will helm officially support installations outside the first jurisdiction?**
10. **Which data may be stored, and for how long?**
11. **Will derived indicators or model outputs be published or shared?**
12. **Will market data be used for model training?**
13. **Will the project embed an AGPL component such as parts of a research platform, and is that compatible with the intended license?**
14. **Is Apache-2.0, AGPL, source-available or dual licensing appropriate?**
15. **What is the maximum acceptable loss and notional size for the live pilot?**
16. **Who can rearm the system after a kill switch?**
17. **Who independently reviews risk and execution code?**
18. **What happens when Hermes and deterministic risk disagree?** Recommended answer: risk always wins.
19. **What happens when helm and broker records disagree?** Recommended answer: broker record triggers a reconciliation halt, not an automatic corrective trade.
20. **Are commodity futures genuinely needed, or are ETFs sufficient for the first two years?**

---

# 16. Primary-source bibliography

## United States regulation

1. **SEC, “Robo-Advisers,” IM Guidance Update 2017-02 — February 2017.**
   [https://www.sec.gov/investment/im-guidance-2017-02.pdf](https://www.sec.gov/investment/im-guidance-2017-02.pdf) ([SEC][38])

2. **SEC, “Guide to Broker-Dealer Registration” — October 6, 2009; current SEC guidance page.**
   [https://www.sec.gov/about/divisions-offices/division-trading-markets/division-trading-markets-compliance-guides/guide-broker-dealer-registration](https://www.sec.gov/about/divisions-offices/division-trading-markets/division-trading-markets-compliance-guides/guide-broker-dealer-registration) ([SEC][7])

3. **SEC, “Commission Interpretation Regarding Standard of Conduct for Investment Advisers” — June 5, 2019.**
   [https://www.sec.gov/files/rules/interp/2019/ia-5248.pdf](https://www.sec.gov/files/rules/interp/2019/ia-5248.pdf) ([SEC][39])

4. **SEC, “Exemption for Certain Investment Advisers Operating Through the Internet” — March 27, 2024.**
   [https://www.sec.gov/files/rules/final/2024/ia-6578.pdf](https://www.sec.gov/files/rules/final/2024/ia-6578.pdf) ([SEC][40])

5. **CFTC, Commodity Trading Advisors — current regulator page, accessed July 29, 2026.**
   [https://www.cftc.gov/IndustryOversight/Intermediaries/CTAs/index.htm](https://www.cftc.gov/IndustryOversight/Intermediaries/CTAs/index.htm) ([Commodity Futures Trading Commission][8])

6. **CFTC, Intermediary definitions — current page, accessed July 29, 2026.**
   [https://www.cftc.gov/IndustryOversight/Intermediaries/index.htm](https://www.cftc.gov/IndustryOversight/Intermediaries/index.htm) ([Commodity Futures Trading Commission][41])

## India regulation

7. **SEBI, “Safer participation of retail investors in Algorithmic trading” — February 4, 2025.**
   [https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html](https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html) ([Securities and Exchange Board of India][2])

8. **SEBI, implementation-timeline extension for the retail-algo framework — September 30, 2025.**
   [https://www.sebi.gov.in/legal/circulars/sep-2025/extension-of-timeline-for-implementation-of-sebi-circular-dated-february-04-2025-on-safer-participation-of-retail-investors-in-algorithmic-trading-_96979.html](https://www.sebi.gov.in/legal/circulars/sep-2025/extension-of-timeline-for-implementation-of-sebi-circular-dated-february-04-2025-on-safer-participation-of-retail-investors-in-algorithmic-trading-_96979.html) ([Securities and Exchange Board of India][42])

9. **SEBI, extension circular PDF confirming April 1, 2026 applicability — September 30, 2025.**
   [https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1759232056254.pdf](https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1759232056254.pdf) ([Securities and Exchange Board of India][14])

10. **SEBI, Investment Adviser and Research Analyst regulation listing — current through July 2026.**
    [https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=1&smid=0&ssid=3](https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=1&smid=0&ssid=3) ([Securities and Exchange Board of India][12])

11. **SEBI, Research Analysts FAQ — July 23, 2025.**
    [https://www.sebi.gov.in/sebi_data/faqfiles/jul-2025/1753269723942.pdf](https://www.sebi.gov.in/sebi_data/faqfiles/jul-2025/1753269723942.pdf) ([Securities and Exchange Board of India][11])

12. **SEBI, Investment Advisers FAQ — August 2025.**
    [https://www.sebi.gov.in/sebi_data/faqfiles/aug-2025/1755174193178.pdf](https://www.sebi.gov.in/sebi_data/faqfiles/aug-2025/1755174193178.pdf) ([Securities and Exchange Board of India][10])

13. **FIU-IND, AML/CFT Guidelines for VDA-related reporting entities — updated January 8, 2026.**
    [https://fiuindia.gov.in/pdfs/downloads/VDA08012026.pdf](https://fiuindia.gov.in/pdfs/downloads/VDA08012026.pdf) ([Financial Intelligence Unit][16])

## Market-data licensing

14. **UTP Plan, 2026 Non-Display Declaration — 2026.**
    [https://www.utpplan.com/DOC/NonDisplayDeclaration.pdf](https://www.utpplan.com/DOC/NonDisplayDeclaration.pdf) ([UTPPlan][26])

15. **CTA Plan, Market Data Non-Display Use Policy — November 1, 2015; current hosted policy.**
    [https://www.ctaplan.com/publicdocs/ctaplan/Policy_CTA_Non_Display_with_FAQ.pdf](https://www.ctaplan.com/publicdocs/ctaplan/Policy_CTA_Non_Display_with_FAQ.pdf) ([ctaplan.com][43])

16. **NSE, Paid Non-Display Data — updated April 24, 2026.**
    [https://www.nseindia.com/static/market-data/non-display-data](https://www.nseindia.com/static/market-data/non-display-data) ([NSE India][27])

17. **NSE, Data Sharing and Usage Policy — December 11, 2025.**
    [https://www.nseindia.com/static/market-data/nse-data-policy](https://www.nseindia.com/static/market-data/nse-data-policy) ([NSE India][29])

18. **NSE, End-of-Day and Historical Data — updated June 19, 2026.**
    [https://www.nseindia.com/static/market-data/eod-historical-data-subscription](https://www.nseindia.com/static/market-data/eod-historical-data-subscription) ([NSE India][28])

19. **BSE, Information Products Tariff — February 2025.**
    [https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf](https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf) ([BSE India][30])

## Broker and API documentation

20. **Alpaca, Paper Trading — current documentation, accessed July 29, 2026.**
    [https://docs.alpaca.markets/docs/paper-trading](https://docs.alpaca.markets/docs/paper-trading) ([Alpaca US][1])

21. **Alpaca, Trading Order API — current documentation, accessed July 29, 2026.**
    [https://docs.alpaca.markets/reference/postorder](https://docs.alpaca.markets/reference/postorder) ([Alpaca US][44])

22. **Alpaca, Market Data Plans — current pricing, accessed July 29, 2026.**
    [https://alpaca.markets/data](https://alpaca.markets/data) ([Alpaca][45])

23. **Interactive Brokers, Client Portal API — current documentation, accessed July 29, 2026.**
    [https://interactivebrokers.github.io/cpwebapi/](https://interactivebrokers.github.io/cpwebapi/) ([Interactive Brokers][46])

24. **Interactive Brokers, TWS API introduction and paper accounts — current documentation.**
    [https://interactivebrokers.github.io/tws-api/introduction.html](https://interactivebrokers.github.io/tws-api/introduction.html) ([Interactive Brokers][47])

25. **Zerodha, Kite Connect API and current pricing — accessed July 29, 2026.**
    [https://kite.trade/](https://kite.trade/) ([Kite][48])

26. **Upstox, API Overview and Sandbox — accessed July 29, 2026.**
    [https://upstox.com/developer/api-documentation/api-overview/](https://upstox.com/developer/api-documentation/api-overview/)
    [https://upstox.com/developer/api-documentation/sandbox/](https://upstox.com/developer/api-documentation/sandbox/) ([Upstox - Online Stock and Share Trading][49])

27. **DhanHQ, Authentication and API eligibility — updated September 23, 2025.**
    [https://dhanhq.co/docs/v2/authentication/](https://dhanhq.co/docs/v2/authentication/) ([dhanhq.co][21])

## Open-source reference systems

28. **NautilusTrader — official project and documentation, accessed July 29, 2026.**
    [https://github.com/nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) ([NautilusTrader][33])

29. **QuantConnect LEAN — official repository, accessed July 29, 2026.**
    [https://github.com/QuantConnect/Lean](https://github.com/QuantConnect/Lean) ([GitHub][34])

30. **OpenBB — official platform and repository, accessed July 29, 2026.**
    [https://github.com/OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) ([OpenBB Docs][50])

31. **Freqtrade — official repository, accessed July 29, 2026.**
    [https://github.com/freqtrade/freqtrade](https://github.com/freqtrade/freqtrade) ([GitHub][36])

32. **Hummingbot — official repository, accessed July 29, 2026.**
    [https://github.com/hummingbot/hummingbot](https://github.com/hummingbot/hummingbot) ([Hummingbot][37])

---

## Final recommendation

Proceed with **U.S. equities paper trading first**, using Alpaca and a deliberately narrow cash-equity model. Build helm’s mandate compiler, deterministic risk, event ledger, reconciliation and security gateway before adding live execution.

In parallel, build an **India read-only and Upstox-sandbox profile**, but do not enable Indian live execution until a broker and Indian counsel have classified helm’s IA, RA and algo-provider roles.

Treat Hermes as untrusted. Its output should terminate at a proposal boundary. It should never hold broker credentials, directly access an order endpoint, administer policy or rearm a live market.

The project should measure success not by how autonomously it trades, but by whether every market action is:

> **authorized, bounded, deterministic, attributable, entitlement-compliant, recoverable and reconciled.**

[1]: https://docs.alpaca.markets/us/docs/paper-trading?utm_source=chatgpt.com "Paper Trading"
[2]: https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html?utm_source=chatgpt.com "Safer participation of retail investors in Algorithmic trading"
[3]: https://alpaca.markets/elite?utm_source=chatgpt.com "Alpaca - Elite"
[4]: https://alpaca.markets/support/countries-alpaca-is-available?utm_source=chatgpt.com "Countries Alpaca is available"
[5]: https://www.sec.gov/about/offices/oia/oia_investman/rplaze-042012.pdf "https://www.sec.gov/about/offices/oia/oia_investman/rplaze-042012.pdf"
[6]: https://www.sec.gov/divisions/investment/noaction/2015/jonathon-hendricks-012615-202a.htm "https://www.sec.gov/divisions/investment/noaction/2015/jonathon-hendricks-012615-202a.htm"
[7]: https://www.sec.gov/about/divisions-offices/division-trading-markets/division-trading-markets-compliance-guides/guide-broker-dealer-registration "https://www.sec.gov/about/divisions-offices/division-trading-markets/division-trading-markets-compliance-guides/guide-broker-dealer-registration"
[8]: https://www.cftc.gov/IndustryOversight/Intermediaries/CTAs/index.htm?utm_source=chatgpt.com "Commodity Trading Advisors (CTAs) | CFTC"
[9]: https://www.sec.gov/newsroom/speeches-statements/staff-statement-regarding-broker-dealer-registration-certain-user-interfaces-utilized-prepare-staff-statement-regarding-broker-dealer-registration-certain-user-interfaces-utilized "https://www.sec.gov/newsroom/speeches-statements/staff-statement-regarding-broker-dealer-registration-certain-user-interfaces-utilized-prepare-staff-statement-regarding-broker-dealer-registration-certain-user-interfaces-utilized"
[10]: https://www.sebi.gov.in/sebi_data/faqfiles/aug-2025/1755174193178.pdf "https://www.sebi.gov.in/sebi_data/faqfiles/aug-2025/1755174193178.pdf"
[11]: https://www.sebi.gov.in/sebi_data/faqfiles/jul-2025/1753269723942.pdf "https://www.sebi.gov.in/sebi_data/faqfiles/jul-2025/1753269723942.pdf"
[12]: https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=1&smid=0&ssid=3&utm_source=chatgpt.com "SEBI | Regulations"
[13]: https://www.sebi.gov.in/sebi_data/attachdocs/feb-2025/1738665456458.pdf "https://www.sebi.gov.in/sebi_data/attachdocs/feb-2025/1738665456458.pdf"
[14]: https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1759232056254.pdf?utm_source=chatgpt.com "CIRCULAR SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/132 ..."
[15]: https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListingAll=yes&search=Investors&utm_source=chatgpt.com "SEBI | News List All"
[16]: https://fiuindia.gov.in/pdfs/downloads/VDA08012026.pdf?utm_source=chatgpt.com "AML & CFT Guidelines"
[17]: https://www.interactivebrokers.com/en/trading/ib-api.php "https://www.interactivebrokers.com/en/trading/ib-api.php"
[18]: https://docs.tradier.com/docs/trading "https://docs.tradier.com/docs/trading"
[19]: https://kite.trade/docs/connect/v3/?utm_source=chatgpt.com "Kite Connect 3 / API documentation"
[20]: https://upstox.com/developer/api-documentation/sandbox/?utm_source=chatgpt.com "Sandbox - Developer API"
[21]: https://dhanhq.co/docs/v2/authentication/?utm_source=chatgpt.com "Authentication - DhanHQ Ver 2.0 / API Document"
[22]: https://myapi.fyers.in/ "https://myapi.fyers.in/"
[23]: https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/sandbox "https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/sandbox"
[24]: https://docs.kraken.com/exchange/guides/overview "https://docs.kraken.com/exchange/guides/overview"
[25]: https://coindcx.com/api/ "https://coindcx.com/api/"
[26]: https://www.utpplan.com/DOC/NonDisplayDeclaration.pdf?utm_source=chatgpt.com "UTP NON-DISPLAY DECLARATION 2026"
[27]: https://www.nseindia.com/static/market-data/non-display-data?utm_source=chatgpt.com "Paid Non-Display Data"
[28]: https://www.nseindia.com/static/market-data/eod-historical-data-subscription?utm_source=chatgpt.com "Paid End of the day/ Historical Data"
[29]: https://www.nseindia.com/static/market-data/nse-data-policy?utm_source=chatgpt.com "NSE Data Sharing & Usage Policy"
[30]: https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf?utm_source=chatgpt.com "BSE Information Products Tariff February 2025"
[31]: https://upstox.com/developer/api-documentation/instruments?utm_source=chatgpt.com "Instruments - Developer API"
[32]: https://github.com/nousresearch/hermes-agent "https://github.com/nousresearch/hermes-agent"
[33]: https://nautilustrader.io/ "https://nautilustrader.io/"
[34]: https://github.com/QuantConnect/Lean.Brokerages.ByBit "https://github.com/QuantConnect/Lean.Brokerages.ByBit"
[35]: https://docs.openbb.co/odp/python "https://docs.openbb.co/odp/python"
[36]: https://github.com/freqtrade/freqtrade "https://github.com/freqtrade/freqtrade"
[37]: https://hummingbot.org/docs/ "https://hummingbot.org/docs/"
[38]: https://www.sec.gov/investment/im-guidance-2017-02.pdf "https://www.sec.gov/investment/im-guidance-2017-02.pdf"
[39]: https://www.sec.gov/files/rules/interp/2019/ia-5248.pdf "https://www.sec.gov/files/rules/interp/2019/ia-5248.pdf"
[40]: https://www.sec.gov/newsroom/press-releases/2024-42 "https://www.sec.gov/newsroom/press-releases/2024-42"
[41]: https://www.cftc.gov/IndustryOversight/Intermediaries/index.htm?utm_source=chatgpt.com "Intermediaries | CFTC"
[42]: https://www.sebi.gov.in/legal/circulars/sep-2025/extension-of-timeline-for-implementation-of-sebi-circular-dated-february-04-2025-on-safer-participation-of-retail-investors-in-algorithmic-trading-_96979.html?utm_source=chatgpt.com "Extension of timeline for implementation of SEBI Circular ..."
[43]: https://www.ctaplan.com/publicdocs/ctaplan/Policy_CTA_Non_Display_with_FAQ.pdf?utm_source=chatgpt.com "CTA Market Data Non-Display Use Policy"
[44]: https://docs.alpaca.markets/us/reference/postorder?utm_source=chatgpt.com "Create an Order"
[45]: https://alpaca.markets/data?utm_source=chatgpt.com "Unlimited Access, Real-time Market Data API"
[46]: https://interactivebrokers.github.io/cpwebapi/?utm_source=chatgpt.com "Client Portal API Documentation"
[47]: https://interactivebrokers.github.io/tws-api/introduction.html?utm_source=chatgpt.com "TWS API v9.72+: Introduction"
[48]: https://kite.trade/?utm_source=chatgpt.com "Kite Connect APIs: Trading and investment HTTP APIs"
[49]: https://upstox.com/developer/api-documentation/api-overview/?utm_source=chatgpt.com "API Overview – Upstox Developer API"
[50]: https://docs.openbb.co/odp/python/extensions/providers "https://docs.openbb.co/odp/python/extensions/providers"
