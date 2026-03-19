# Document Database
# In production: replace with real DB queries (PostgreSQL + pgvector for RAG, etc.)
# Each document has:
#   - allowed_roles: list of roles that can see this document
#   - access: "public" or "sensitive" (for UI badge display)
#   - content: full text (in production, load from DB or file storage)

DOCUMENTS = [
    {
        "id": 1,
        "name": "Employee Handbook",
        "icon": "📋",
        "access": "public",
        "allowed_roles": ["admin", "hr", "public"],
        "summary": "General company policies, work hours, leave, and code of conduct.",
        "content": """Employee Handbook v3.2 — NovaTech Corp

Welcome to NovaTech. We're a software company building developer tools for modern teams.

Work Hours: Standard hours are 9 AM–6 PM in your local timezone. Flexible arrangements can be approved by your manager.

Leave Policy: Full-time employees receive 20 days of paid leave per year, plus public holidays. Unused leave can be carried over up to 10 days.

Code of Conduct: All employees must maintain professional conduct, protect company IP, and treat colleagues with respect. Violations may result in disciplinary action.

Remote Work: Employees may work remotely up to 3 days per week after completing 3 months of employment.

Equipment: A company laptop and standard accessories are provided. Report any equipment issues to IT within 24 hours.

Performance Reviews: Conducted annually every January. Mid-year check-ins are optional but encouraged.""",
    },
    {
        "id": 2,
        "name": "Product Roadmap 2025",
        "icon": "🗺️",
        "access": "public",
        "allowed_roles": ["admin", "hr", "public"],
        "summary": "Planned product features and milestones for 2025.",
        "content": """Product Roadmap 2025 — NovaTech Corp

Q1 2025:
- Launch NovaDeploy v2.0 with one-click Kubernetes deployments
- Mobile app beta for iOS and Android
- Integration with GitHub Actions and GitLab CI

Q2 2025:
- AI-assisted code review feature (NovaReview)
- Self-hosted enterprise edition
- SOC2 Type II certification

Q3 2025:
- Marketplace for third-party plugins
- Analytics dashboard for team productivity metrics
- Multi-region deployment support

Q4 2025:
- NovaAI copilot for documentation generation
- Enterprise SSO (SAML/OIDC)
- Target: 10,000 paying customers by year-end""",
    },
    {
        "id": 3,
        "name": "Marketing Guidelines",
        "icon": "🎨",
        "access": "public",
        "allowed_roles": ["admin", "hr", "public"],
        "summary": "Brand voice, colors, typography, and social media rules.",
        "content": """Brand & Marketing Guidelines — NovaTech Corp

Brand Voice: NovaTech speaks like a knowledgeable colleague — clear, honest, and a little playful. We avoid jargon and never oversell.

Logo Usage:
- Always use the approved SVG logo files
- Minimum size: 120px wide in digital, 1 inch in print
- Never stretch, recolor, or add effects to the logo

Color Palette:
- Primary: Indigo #5B6AF0
- Secondary: Slate #1A1E27
- Accent: Gold #F0A53C
- Success: Teal #3ECF8E

Typography:
- Headlines: DM Sans 600
- Body: DM Sans 400
- Code: DM Mono

Social Media:
- Post 3–5x/week on LinkedIn and Twitter
- Product updates use the "NovaDeploy" hashtag
- All posts must be approved by the marketing manager before scheduling

Press & Media: All media inquiries must be routed through pr@novatech.io.""",
    },
    {
        "id": 4,
        "name": "Salary Bands & Compensation",
        "icon": "💰",
        "access": "sensitive",
        "allowed_roles": ["admin", "hr"],
        "summary": "Salary ranges by role and level, equity structure, and review budget.",
        "content": """Compensation Framework — CONFIDENTIAL

Engineering:
- Junior Engineer (L1): $80,000 – $100,000
- Mid Engineer (L2): $105,000 – $130,000
- Senior Engineer (L3): $135,000 – $165,000
- Staff Engineer (L4): $170,000 – $210,000
- Principal (L5): $215,000 – $270,000

Product & Design:
- Associate PM: $85,000 – $105,000
- PM: $110,000 – $140,000
- Senior PM: $145,000 – $175,000
- Director of Product: $180,000 – $230,000

Sales:
- AE Base: $70,000 – $90,000 + OTE 1.5x
- Senior AE: $90,000 – $115,000 + OTE 1.5x
- VP Sales: $160,000 – $200,000 + OTE

Equity: Standard grants are 0.01%–0.5% depending on level, vesting over 4 years with 1-year cliff.

Annual Review: Performance reviews occur in January. Budget for raises is typically 3–6% of total payroll.""",
    },
    {
        "id": 5,
        "name": "Investor Relations Q3",
        "icon": "📊",
        "access": "sensitive",
        "allowed_roles": ["admin"],
        "summary": "Q3 financials, ARR, burn rate, and Series B details.",
        "content": """Investor Relations Package — Q3 2024 — STRICTLY CONFIDENTIAL

Financial Highlights:
- ARR: $12.4M (up 87% YoY)
- MRR: $1.03M
- Net Revenue Retention: 128%
- Gross Margin: 76%
- Burn Rate: $820K/month
- Runway: 22 months at current burn

Key Metrics:
- Total Customers: 2,847
- Enterprise Customers (>$50K ACV): 38
- Churn Rate: 2.1% monthly (improving)
- CAC: $4,200 | LTV: $31,500 | LTV:CAC = 7.5x

Upcoming Milestones:
- Series B target: $30M at $120M pre-money valuation
- Lead investor term sheet expected Q1 2025
- Secondary sale planned for early employees

Pipeline: $8.2M qualified pipeline, $1.4M in final stages.

Do NOT share externally or with employees below VP level.""",
    },
    {
        "id": 6,
        "name": "Security Incident Log",
        "icon": "🛡️",
        "access": "sensitive",
        "allowed_roles": ["admin"],
        "summary": "Log of security incidents, resolutions, and open CVEs.",
        "content": """Security Incident Log — CONFIDENTIAL — IT & Security Team Only

INC-2024-087 (Severity: High)
Date: September 14, 2024
Description: Unauthorized access attempt on production API gateway. MFA blocked the attempt. Account locked, password reset forced.
Resolution: Enhanced rate limiting deployed, all engineer credentials audited.

INC-2024-091 (Severity: Medium)
Date: October 3, 2024
Description: S3 bucket misconfiguration exposed non-sensitive build artifacts publicly for ~4 hours.
Resolution: Automated bucket policy scanner added to CI pipeline. No customer data exposed.

INC-2024-103 (Severity: Low)
Date: November 8, 2024
Description: Employee phishing simulation — 12% click rate on simulated phishing email.
Resolution: Mandatory security awareness training scheduled for December.

Open Vulnerabilities:
- CVE-2024-3819: Pending patch on dev servers (due Dec 15)
- Outdated OpenSSL on 3 legacy microservices (ticket NOV-4421)""",
    },
]
