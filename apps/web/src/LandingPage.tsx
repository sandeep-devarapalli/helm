import {
  ArrowRight,
  FileCheck2,
  GitBranch,
  LockKeyhole,
  MessageSquare,
  ShieldCheck,
} from "lucide-react";
import "./landing.css";

const repositoryUrl = "https://github.com/sandeep-devarapalli/helm";
const roadmapUrl = `${repositoryUrl}/blob/main/docs/roadmap.md`;

const benefits = [
  {
    icon: MessageSquare,
    title: "Find and compare opportunities",
    body: "Investigate companies, assets, risks, and alternatives without losing the question that started the work.",
  },
  {
    icon: GitBranch,
    title: "Test before you trust",
    body: "Turn an idea into explicit rules and examine the assumptions, costs, weak evidence, and counter-case.",
  },
  {
    icon: FileCheck2,
    title: "Keep control of the decision",
    body: "Set eligible assets, exposure, duration, and loss limits before any plan can move toward execution.",
  },
];

const useCases = [
  ["Research an investment", "Compare a company with its peers, examine the thesis and catalysts, and see the strongest counter-argument with its sources."],
  ["Test a trading rule", "Describe a stock or crypto strategy in plain language, then evaluate it with explicit costs, slippage, and risk limits."],
  ["Evaluate an allocation idea", "Examine a user-defined mix of U.S. equities, Indian equities, crypto, and listed commodity ETFs in one portfolio and risk view."],
  ["Monitor a thesis", "Define what would invalidate a position and understand why a price, earnings, volatility, or evidence alert appears."],
];

const operatingLoop = [
  ["Ask naturally", "Describe an investment question, portfolio objective, or trading rule in plain language."],
  ["Inspect evidence", "Review the thesis, arguments against it, sources, update dates, assumptions, and uncertainty."],
  ["Test the idea", "Translate the thesis into reproducible rules with costs and risk measures attached."],
  ["Approve boundaries", "Choose the assets, exposure, duration, loss limits, and conditions that stop the plan."],
  ["Run and review", "Allow only approved actions, then compare what happened with the original decision."],
];

const markets = [
  ["U.S. stocks and ETFs", "Compare companies and test ideas that buy—not short—stocks and ETFs without margin.", "Narrow paper trading first"],
  ["Indian equities", "Research NSE/BSE companies, sectors, and cash-based investing strategies.", "Research → local simulation → broker sandbox"],
  ["Crypto spot", "Evaluate 24/7 markets while keeping allocations small and avoiding leverage.", "Research and paper trading"],
  ["Listed commodity ETFs", "Compare the structure, fees, liquidity, tracking, and risks of planned gold and silver ETF exposure.", "Commodity-ETF paper later; direct futures deferred"],
];

function MiniWorkbench() {
  return (
    <div className="landing-workbench" aria-label="Illustrative target helm workflow">
      <div className="workbench-topline">
        <span className="mini-wordmark">helm workbench</span>
        <span>illustrative workflow · no live order</span>
      </div>
      <div className="workbench-grid">
        <div className="conversation-preview">
          <div className="preview-heading">
            <span>Investment question</span>
            <span>One workspace</span>
          </div>
          <div className="preview-message user-message">
            <strong>You</strong>
            <p>Compare how AAPL, RELIANCE, BTC/USD, and a listed gold ETF behaved in high-volatility periods. Show the strongest counter-case.</p>
          </div>
          <div className="preview-message hermes-message">
            <strong>Hermes</strong>
            <p>Planned workflow: compare return drivers, downside, valuation, liquidity, and currency exposure without recommending an allocation.</p>
          </div>
          <div className="preview-event">
            <span className="event-dot" />
            <span>evidence and opposing case required</span>
            <time>review next</time>
          </div>
        </div>
        <div className="control-preview">
          <div className="preview-heading">
            <span>Research brief</span>
            <span>Approval required</span>
          </div>
          <dl>
            <div><dt>Universe</dt><dd>4 instruments</dd></div>
            <div><dt>Objective</dt><dd>compare resilience</dd></div>
            <div><dt>Crypto cap</dt><dd>user-defined</dd></div>
            <div><dt>Evidence</dt><dd className="status-present">sources + date checked</dd></div>
            <div><dt>What could go wrong</dt><dd className="status-present">required</dd></div>
            <div><dt>Permission to trade</dt><dd className="status-blocked">none</dd></div>
          </dl>
        </div>
      </div>
      <div className="workbench-footer">
        <span>Planned evidence trail</span>
        <span>No order permitted</span>
      </div>
    </div>
  );
}

function SectionIntro({ eyebrow, title, body }: { eyebrow: string; title: string; body: string }) {
  return (
    <div className="section-intro">
      <span className="landing-eyebrow">{eyebrow}</span>
      <h2>{title}</h2>
      <p>{body}</p>
    </div>
  );
}

export function LandingPage() {
  return (
    <div className="landing-page">
      <header className="landing-header">
        <a className="landing-wordmark" href="/" aria-label="helm home">helm</a>
        <nav aria-label="Landing page">
          <a href="#product">Product</a>
          <a href="#use-cases">Use cases</a>
          <a href="#markets">Markets</a>
          <a href="#safety">Safety</a>
          <a href="#availability">Availability</a>
        </nav>
        <a className="header-action" href="/app">Open Workbench <ArrowRight size={15} /></a>
      </header>

      <main>
        <section className="landing-hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <span className="landing-eyebrow">Conversational AI for investing and trading</span>
            <h1 id="hero-title">One place to research an idea, test the strategy, and keep control.</h1>
            <p className="hero-lede">helm is being built for individual investors and professional teams managing their own capital. Explore U.S. and Indian stocks, crypto, and listed commodity ETFs; test a strategy; and set exactly what would be allowed to trade.</p>
            <div className="hero-actions">
              <a className="primary-link" href="#how-it-works">See how it works <ArrowRight size={16} /></a>
              <a className="secondary-link" href="/app">Explore current Workbench <ArrowRight size={16} /></a>
            </div>
            <div className="hero-status" aria-label="Current product availability">
              <span><i />Early product preview</span>
              <span>U.S. paper trading planned first</span>
              <span>No live trading today</span>
            </div>
          </div>
          <MiniWorkbench />
        </section>

        <section className="landing-section product-section" id="product">
          <SectionIntro
            eyebrow="Why helm"
            title="Keep the evidence, strategy, limits, and approval together."
            body="AI chats can suggest ideas and brokers can place orders. helm is designed to keep the missing work between them—and the eventual outcome—in one decision record you can inspect."
          />
          <div className="capability-grid">
            {benefits.map(({ icon: Icon, title, body }) => (
              <article className="capability" key={title}>
                <Icon size={19} />
                <h3>{title}</h3>
                <p>{body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section use-cases-section" id="use-cases">
          <SectionIntro
            eyebrow="What helm is being built to support"
            title="From a single stock question to a multi-market strategy with clear rules."
            body="helm is designed around the questions investors actually ask, whether you invest for yourself or make decisions with a professional team."
          />
          <div className="use-case-grid">
            {useCases.map(([title, body], index) => (
              <article className="use-case" key={title}>
                <span data-numeric>{String(index + 1).padStart(2, "0")}</span>
                <div><h3>{title}</h3><p>{body}</p></div>
              </article>
            ))}
          </div>
          <p className="section-qualifier">These are the workflows helm is designed to support. Current availability is disclosed below.</p>
        </section>

        <section className="landing-section markets-section" id="markets">
          <SectionIntro
            eyebrow="Markets and investment choices"
            title="One disciplined workflow across the assets investors already consider."
            body="U.S. stocks, Indian equities, crypto, and commodity ETFs each trade differently. helm is designed to apply the right currency, market hours, and risk rules to each one."
          />
          <div className="market-table-wrap">
            <table>
              <thead>
                <tr><th>Market</th><th>What helm is designed to help with</th><th>First planned mode</th></tr>
              </thead>
              <tbody>
                {markets.map(([market, benefit, mode]) => (
                  <tr key={market}>
                    <th scope="row">{market}</th>
                    <td>{benefit}</td>
                    <td><span className="planned-state">{mode}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="coverage-note">Target coverage, not current market access. The Workbench uses sample market data today; research, paper execution, and live trading are not available. Near-term scope excludes options contracts, margin, short selling, and leveraged products.</p>
        </section>

        <section className="landing-section loop-section" id="how-it-works" aria-labelledby="loop-title">
          <div className="loop-heading">
            <span className="landing-eyebrow">How the product is designed to work</span>
            <h2 id="loop-title">You keep the judgment. helm keeps the process accountable.</h2>
            <p>The current preview supports the conversation. Evidence-backed research, strategy testing, approvals, execution, and reconciliation are on the roadmap.</p>
          </div>
          <ol className="operating-steps">
            {operatingLoop.map(([title, body], index) => (
              <li key={title}>
                <div className="step-number" data-numeric>{String(index + 1).padStart(2, "0")}</div>
                <h3>{title}</h3>
                <p>{body}</p>
              </li>
            ))}
          </ol>
        </section>

        <section className="landing-section safety-section" id="safety">
          <div className="safety-copy">
            <span className="landing-eyebrow">AI without unchecked authority</span>
            <h2>Hermes will propose. It will not control execution.</h2>
            <p>helm separates intelligence from authority. Hermes is designed to help investigate and structure a decision. helm’s rule-based controls will enforce the limits you approve.</p>
            <div className="trust-line"><LockKeyhole size={17} />No approval means no order · Live trading remains disabled</div>
          </div>
          <div className="boundary-list">
            <div>
              <MessageSquare size={18} />
              <span><strong>Hermes reasoning</strong><small>Designed to structure the thesis, what could go wrong, evidence, uncertainty, and proposed action.</small></span>
            </div>
            <div>
              <FileCheck2 size={18} />
              <span><strong>Your authority</strong><small>You define what can trade, how much, at what price, during which hours, and for how long.</small></span>
            </div>
            <div>
              <ShieldCheck size={18} />
              <span><strong>helm controls</strong><small>Designed to use rules the AI cannot change and keep every decision, exception, and outcome reviewable.</small></span>
            </div>
          </div>
          <p className="context-note">helm is designed for individual investors and professional teams managing their own capital. Client advisory, managed accounts, pooled capital, and copy trading are not supported.</p>
        </section>

        <section className="landing-section status-section" id="availability">
          <SectionIntro
            eyebrow="Product transparency"
            title="Explore the direction while the trading product is being built."
            body="The current preview demonstrates the conversational foundation. The investment workflows above describe the product helm is building toward."
          />
          <div className="status-ledger">
            <div>
              <span className="ledger-label">Available now</span>
              <p>Saved workspace conversations · progress that survives refresh and restart · visible failures · sample market data · preferences changed only with approval</p>
            </div>
            <div>
              <span className="ledger-label planned">On the roadmap</span>
              <p>Sourced research · repeatable strategy testing · approved trading limits and risk controls · U.S. paper trading · broker integration</p>
            </div>
            <div>
              <span className="ledger-label absent">Not available today</span>
              <p>Live trading</p>
            </div>
            <div>
              <span className="ledger-label absent">Not supported</span>
              <p>Trading without human approval · investment advice · managing client capital</p>
            </div>
          </div>
        </section>

        <section className="landing-section faq-section" id="faq">
          <SectionIntro
            eyebrow="FAQ"
            title="What to know before you explore."
            body="helm’s intended capabilities and its current preview are deliberately stated separately."
          />
          <div className="faq-list">
            <details>
              <summary>What is helm?</summary>
              <p>helm is an open-source conversational workspace being built for investment research, strategy validation, and controlled trading across multiple markets.</p>
            </details>
            <details>
              <summary>Who is helm for?</summary>
              <p>helm is designed for individual investors and professional teams managing their own capital. It does not support client advisory, managed accounts, pooled capital, or copy trading.</p>
            </details>
            <details>
              <summary>What can I use today?</summary>
              <p>You can explore the conversational Workbench and its product direction. Product-grade research, backtesting, paper trading, and live trading are not yet available.</p>
            </details>
            <details>
              <summary>Which markets are planned?</summary>
              <p>Planned coverage includes U.S. stocks and ETFs, Indian equities, crypto spot, and allowlisted listed commodity ETFs. U.S. stocks are the first market planned for paper trading. Other markets will follow only after separate testing and access reviews.</p>
            </details>
            <details>
              <summary>Can helm trade without my approval?</summary>
              <p>No. The intended design requires an explicit, active approval with defined limits. Hermes cannot access broker credentials, approve its own proposal, or override helm’s rule-based risk checks.</p>
            </details>
            <details>
              <summary>Is helm a broker, custodian, fund, or investment adviser?</summary>
              <p>No. helm is software. Any future market access depends on separately approved brokers, venues, custodians, data rights, and jurisdiction-specific eligibility. AI output can be incomplete or wrong.</p>
            </details>
          </div>
        </section>

        <section className="landing-cta">
          <div>
            <span className="landing-eyebrow">Open product preview</span>
            <h2>Start with the decision, not the order ticket.</h2>
            <p>Explore the conversational Workbench and see the design for bringing the question, evidence, strategy, limits, and approval into one workspace.</p>
          </div>
          <div className="cta-links">
            <a className="primary-link" href="/app">Explore current Workbench <ArrowRight size={16} /></a>
            <a className="secondary-link" href={roadmapUrl}>View product roadmap <ArrowRight size={16} /></a>
          </div>
        </section>
      </main>

      <footer className="landing-footer">
        <div className="footer-topline">
          <span className="landing-wordmark">helm</span>
          <nav aria-label="Project links">
            <a href={repositoryUrl}>GitHub</a>
            <a href={`${repositoryUrl}/blob/main/docs/architecture/overview.md`}>Architecture</a>
            <a href={`${repositoryUrl}/blob/main/docs/architecture/trust-boundaries.md`}>Trust boundaries</a>
            <a href={roadmapUrl}>Roadmap</a>
            <a href={`${repositoryUrl}/blob/main/THIRD_PARTY_NOTICES.md`}>Third-party notices</a>
          </nav>
        </div>
        <p>helm is experimental open-source software. The current Workbench uses sample market data and cannot place trades. helm is not a broker, exchange, custodian, fund, or investment adviser. Nothing here is investment, legal, tax, or regulatory advice. Trading and investing involve risk of loss.</p>
        <p className="attribution">helm uses the upstream Hermes Agent and Vibe-Trading runtimes and is not affiliated with Nous Research or HKUDS.</p>
      </footer>
    </div>
  );
}
