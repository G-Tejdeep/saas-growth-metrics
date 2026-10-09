# SaaS Product Growth, Onboarding Funnel & Retention Analytics 

## 1. Executive Summary
This project simulates a data-driven Growth & Product Analytics environment for a B2B SaaS company operating across diverse industries (Fintech, Healthcare, E-commerce, EdTech, SaaS). The primary objective is to track, analyze, and optimize user onboarding conversion funnels and product activation loops using **Python, PostgreSQL, SQL, and DBeaver**. 

By processing 5,000 synthetic user records and sequential event logs, this portfolio project demonstrates core Business Analyst competencies: funnel drop-off analysis, product milestone tracking, cohort evaluation, and actionable business recommendation synthesis.

---

## 2. Technical Stack & Architecture
* **Operating System:** macOS
* **Language & Runtime:** Python 3.13 (Managed within virtual environment `venv`)
* **Database Engine:** PostgreSQL 16 (Local Service via Homebrew)
* **Data Generation & Orchestration Libraries:** `pandas`, `numpy`, `faker`, `SQLAlchemy`, `psycopg`
* **Data Exploration & Query Tool:** DBeaver (JDBC PostgreSQL Driver)
* **Version Control:** Git / GitHub

---

## 3. Database Schema Design
The relational database `saas_growth_analytics` is structured around two primary tables designed to model user acquisition and lifecycle event tracking:

### A. `users` Table
Stores account-level metadata for each registered customer.
* `user_id` (INT, Primary Key): Unique numeric identifier starting from 1001.
* `company_name` (VARCHAR): Fictional business entity name generated via Faker.
* `industry` (VARCHAR): Market segment categorization (`Fintech`, `Healthcare`, `E-commerce`, `EdTech`, `SaaS`).
* `signup_date` (TIMESTAMP): Exact account creation timestamp (January 1, 2026 – Present).
* `plan_tier` (`Free_Trial`, `Pro_Monthly`, `Enterprise_Annual`).
* `country` (VARCHAR): ISO country code representation.

### B. `events_log` Table
Stores sequential product interaction logs capturing user onboarding progression milestones.
* `event_id` (UUID, Primary Key): Unique transaction log identifier.
* `user_id` (INT, Foreign Key referencing `users`): Associated user reference.
* `event_name` (VARCHAR): Product milestone step (`signup_completed`, `profile_setup`, `team_invite_sent`, `integration_connected`, `first_campaign_launched`).
* `event_timestamp` (TIMESTAMP): Exact timestamp when the product event occurred.

---

## 4. Analytical SQL: Onboarding Funnel Analysis
To measure product activation performance, the following SQL query aggregates user milestone progression and calculates step-by-step conversion drop-offs.

```sql
-- SaaS Onboarding Funnel & Conversion Analysis
WITH user_funnel AS (
    SELECT 
        u.user_id,
        u.industry,
        MAX(CASE WHEN e.event_name = 'signup_completed' THEN 1 ELSE 0 END) AS step_1_signup,
        MAX(CASE WHEN e.event_name = 'profile_setup' THEN 1 ELSE 0 END) AS step_2_profile,
        MAX(CASE WHEN e.event_name = 'team_invite_sent' THEN 1 ELSE 0 END) AS step_3_invite,
        MAX(CASE WHEN e.event_name = 'integration_connected' THEN 1 ELSE 0 END) AS step_4_integration,
        MAX(CASE WHEN e.event_name = 'first_campaign_launched' THEN 1 ELSE 0 END) AS step_5_campaign
    FROM users u
    LEFT JOIN events_log e ON u.user_id = e.user_id
    GROUP BY u.user_id, u.industry
)
SELECT 
    COUNT(user_id) AS total_users,
    SUM(step_1_signup) AS reached_signup,
    SUM(step_2_profile) AS reached_profile,
    SUM(step_3_invite) AS reached_invite,
    SUM(step_4_integration) AS reached_integration,
    SUM(step_5_campaign) AS reached_campaign,
    ROUND(SUM(step_5_campaign) * 100.0 / NULLIF(SUM(step_1_signup), 0), 2) AS overall_conversion_rate_pct
FROM user_funnel;
```

---

## 5. Key Findings & Business Insights
Running the analytics query against our 5,000-user sample generated the following benchmark performance metrics:

| Funnel Metric / Milestone | User Count | Step-by-Step Retention / Drop-off |
| :--- | :--- | :--- |
| **Total Cohort / Signup Completed** | 5,000 | 100.0% (Baseline) |
| **Profile Setup** | 4,026 | 80.5% |
| **Team Invite Sent** | 1,988 | 49.4% |
| **Integration Connected** | 580 | 14.4% |
| **First Campaign Launched (Activation)** | 86 | **1.72%** (End-to-End Conversion) |

### Strategic Product Recommendations:
1. **Friction Reduction at Third-Party Integrations:** The steepest drop-off occurs between team invites and third-party integrations (dropping precipitously from ~49.4% down to 14.4%). Product and engineering teams should prioritize native pre-built connectors or guided setup wizards to minimize configuration friction.
2. **Accelerating Time-to-Value (TTV):** With an overall activation rate of 1.72% reaching the final campaign launch milestone, introducing proactive in-app tooltips, contextual checklists, and automated email re-engagement sequences for users stalling at step 3 can significantly lift trial-to-paid conversions.
