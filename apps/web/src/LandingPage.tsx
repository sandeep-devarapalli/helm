import {
  ArrowRight,
  Database,
  FileCheck2,
  GitBranch,
  LockKeyhole,
  MessageSquare,
  ShieldCheck,
} from "lucide-react";
import { Badge } from "@helm/ui";
import "./landing.css";

const repositoryUrl = "https://github.com/sandeep-devarapalli/helm";

const capabilities = [
  {
    icon: MessageSquare,
    title: "Persistent conversations",
    body: "Messages, run state, ordered events, and terminal replies survive refresh and restart.",
  },
  {
    icon: GitBranch,
    title: "Incomplete stays incomplete",
    body: "Projection gaps, uncertain outcomes, failures, and partial provenance remain visibly unresolved.",
  },
  {
    icon: FileCheck2,
    title: "Approval stays explicit",
    body: "Only approved presentation preferences reach future Hermes runs. Pending and rejected proposals remain inert.",
  },
];

const operatingLoop = [
  ["Ask", "Available", "Persist one workspace-scoped conversation."],
  ["Gather evidence", "Planned", "Add allowlisted research sources and provenance."],
  ["Validate", "Planned", "Run deterministic quality and policy checks."],
  ["Propose mandate", "Later gate", "Present a typed mandate for explicit commitment."],
  ["Authorised execution", "Later gate", "Execute only after authorized-principal commitment and deterministic risk checks."],
];

const markets = [
  ["U.S. equities", "Representative identity fixture", "Narrow cash-only, long-only paper adapter planned first."],
  ["Indian equities", "Representative identity fixture", "Research and sandbox support planned."],
  ["Crypto spot", "Representative asset + venue fixture", "Allowlisted, unleveraged spot paper profile planned."],
  ["Commodity ETF exposure", "Representative gold ETF fixture", "Allowlisted, unleveraged listed-ETF paper exposure planned; direct commodity futures deferred."],
];

function MiniWorkbench() {
  return (
    <div className="landing-workbench" aria-label="Illustrative Stage 1 Workbench state">
      <div className="workbench-topline">
        <span className="mini-wordmark">helm workbench</span>
        <span>stage-1 · fixture</span>
      </div>
      <div className="workbench-grid">
        <div className="conversation-preview">
          <div className="preview-heading">
            <span>Conversation</span>
            <span>Persisted</span>
          </div>
          <div className="preview-message user-message">
            <strong>You</strong>
            <p>Keep this evidence request resumable if the run stops early.</p>
          </div>
          <div className="preview-message hermes-message">
            <strong>Hermes</strong>
            <p>The conversation and run state are persisted. Research is not implemented in Stage 1.</p>
          </div>
          <div className="preview-event">
            <span className="event-dot" />
            <span>terminal reply recorded</span>
            <time>event 004</time>
          </div>
        </div>
        <div className="control-preview">
          <div className="preview-heading">
            <span>Control boundary</span>
            <span>Fail closed</span>
          </div>
          <dl>
            <div><dt>Conversation</dt><dd className="status-present">persisted</dd></div>
            <div><dt>Run projection</dt><dd className="status-present">resumable</dd></div>
            <div><dt>Tool provenance</dt><dd className="status-present">bounded</dd></div>
            <div><dt>Market values</dt><dd>fixture only</dd></div>
            <div><dt>Broker credentials</dt><dd className="status-blocked">none</dd></div>
            <div><dt>Order path</dt><dd className="status-blocked">none</dd></div>
          </dl>
        </div>
      </div>
      <div className="workbench-footer">
        <span>Workspace scoped</span>
        <span>Live capital blocked</span>
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
          <a href="#safety">Safety</a>
          <a href="#markets">Markets</a>
          <a href="#status">Status</a>
          <a href="#faq">FAQ</a>
        </nav>
        <a className="header-action" href="/app">Open workbench <ArrowRight size={15} /></a>
      </header>

      <main>
        <section className="landing-hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <span className="landing-eyebrow">Open-source · Stage 1 foundation</span>
            <h1 id="hero-title">A governed conversational foundation for AI trading.</h1>
            <p className="hero-lede">Talk to Hermes in a persistent, workspace-scoped conversation. helm records run state, keeps incomplete outcomes visible, and gives the agent no broker credentials or order path.</p>
            <div className="hero-actions">
              <a className="primary-link" href="#status">See what works today <ArrowRight size={16} /></a>
              <a className="secondary-link" href={repositoryUrl}>View on GitHub <ArrowRight size={16} /></a>
            </div>
            <div className="hero-status" aria-label="Current product status">
              <span><i />Market values are fixtures</span>
              <span>Paper-first</span>
              <span>No live orders</span>
            </div>
          </div>
          <MiniWorkbench />
        </section>

        <section className="landing-section product-section" id="product">
          <SectionIntro
            eyebrow="Product"
            title="One operating surface for Hermes."
            body="Stage 1 proves the conversation and control-plane foundation before adding research or trading capability."
          />
          <div className="capability-grid">
            {capabilities.map(({ icon: Icon, title, body }) => (
              <article className="capability" key={title}>
                <Icon size={19} />
                <h3>{title}</h3>
                <p>{body}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="landing-section loop-section" aria-labelledby="loop-title">
          <div className="loop-heading">
            <span className="landing-eyebrow">Operating model</span>
            <h2 id="loop-title">Every capability earns its gate.</h2>
          </div>
          <ol className="operating-steps">
            {operatingLoop.map(([title, status, body], index) => (
              <li key={title}>
                <div className="step-number" data-numeric>{String(index + 1).padStart(2, "0")}</div>
                <h3>{title}</h3>
                <Badge tone={status === "Available" ? "success" : "neutral"} mono>{status}</Badge>
                <p>{body}</p>
              </li>
            ))}
          </ol>
        </section>

        <section className="landing-section safety-section" id="safety">
          <div className="safety-copy">
            <span className="landing-eyebrow">Safety</span>
            <h2>Hermes reasons. Trading stays outside the agent.</h2>
            <p>Hermes has no broker credentials, policy-administration tools, direct order-submission tools, or kill-switch access. Stage 1 has no active mandate and no order path.</p>
            <div className="trust-line"><LockKeyhole size={17} />No broker credentials · No order tools · No live capability</div>
          </div>
          <div className="boundary-list">
            <div>
              <MessageSquare size={18} />
              <span><strong>Hermes</strong><small>Conversation and reasoning inside a narrow tool boundary.</small></span>
            </div>
            <div>
              <Database size={18} />
              <span><strong>helm today</strong><small>Persists workspace, run, event, provenance, and approved preference state.</small></span>
            </div>
            <div>
              <ShieldCheck size={18} />
              <span><strong>Trading authority</strong><small>Not present. Mandates, risk, brokers, orders, and fills remain later gates.</small></span>
            </div>
          </div>
          <p className="context-note">Current workspace conversation and preference state are context-scoped. By design, individual self-directed and institutional proprietary contexts will not share credentials, authority, accounts, positions, mandates, or audit state. Client advisory, managed accounts, pooled capital, and copy trading are not supported.</p>
        </section>

        <section className="landing-section markets-section" id="markets">
          <SectionIntro
            eyebrow="Markets"
            title="Multi-market foundations, not market access."
            body="helm separates currencies, venues, instruments, and venue-specific listings. Workbench prices are labeled fixtures; research, paper adapters, and live execution are not shipped."
          />
          <div className="market-table-wrap">
            <table>
              <thead>
                <tr><th>Market</th><th>Current foundation</th><th>Next verified gate</th></tr>
              </thead>
              <tbody>
                {markets.map(([market, foundation, gate]) => (
                  <tr key={market}>
                    <th scope="row">{market}</th>
                    <td><span className="foundation-state">{foundation}</span></td>
                    <td>{gate}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="coverage-note">Coverage is a roadmap, not an availability claim. Gold appears only as a structural ETF identity fixture; silver is not modeled or available.</p>
        </section>

        <section className="landing-section status-section" id="status">
          <SectionIntro
            eyebrow="Current status"
            title="A public foundation, not a trading release."
            body="Persistent Hermes conversations, resumable event projection, bounded provenance, approval-gated presentation preferences, and the market-identity spine are present."
          />
          <div className="status-ledger">
            <div>
              <span className="ledger-label">Present</span>
              <p>Conversation persistence · ordered run events · resumable SSE · bounded tool provenance · explicit preference approval · canonical market identity</p>
            </div>
            <div>
              <span className="ledger-label absent">Not implemented</span>
              <p>Research · backtests · mandates · broker integration · orders · fills · learning · paper or live trading</p>
            </div>
          </div>
        </section>

        <section className="landing-section faq-section" id="faq">
          <SectionIntro
            eyebrow="FAQ"
            title="Direct answers, before any capital."
            body="The current boundary is intentionally narrower than the long-term product."
          />
          <div className="faq-list">
            <details>
              <summary>What is helm?</summary>
              <p>helm is an open-source conversational operating system for AI trading. Users talk to Hermes; helm is building the surrounding deterministic control-plane boundary.</p>
            </details>
            <details>
              <summary>Can Hermes place trades?</summary>
              <p>No. Hermes has no broker credentials or order-submission tools, and Stage 1 has no order path.</p>
            </details>
            <details>
              <summary>Which markets can I trade today?</summary>
              <p>None through helm. U.S. equities paper is planned first; Indian equities, crypto spot, and commodity ETFs follow later roadmap gates.</p>
            </details>
            <details>
              <summary>Is helm investment advice?</summary>
              <p>No. AI output can be incomplete or wrong. Verify information independently and obtain qualified advice for your jurisdiction.</p>
            </details>
          </div>
        </section>

        <section className="landing-cta">
          <div>
            <span className="landing-eyebrow">Open foundation</span>
            <h2>Inspect the boundary before trusting the promise.</h2>
          </div>
          <div className="cta-links">
            <a className="primary-link" href={repositoryUrl}>View source <ArrowRight size={16} /></a>
            <a className="secondary-link" href="/app">Open workbench <ArrowRight size={16} /></a>
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
            <a href={`${repositoryUrl}/blob/main/docs/roadmap.md`}>Roadmap</a>
            <a href={`${repositoryUrl}/blob/main/THIRD_PARTY_NOTICES.md`}>Third-party notices</a>
          </nav>
        </div>
        <p>helm is experimental open-source software. Stage 1 is a public foundation, not a trading release; Workbench market values are fixtures and no order path exists. helm is not a broker or investment adviser. Nothing here is investment, legal, tax, or regulatory advice. Trading and investing involve risk of loss.</p>
        <p className="attribution">helm uses the upstream Hermes Agent and Vibe-Trading runtimes and is not affiliated with Nous Research or HKUDS.</p>
      </footer>
    </div>
  );
}
