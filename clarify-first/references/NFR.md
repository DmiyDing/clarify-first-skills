# Clarify First — Non-Functional Requirements (NFR) Checklist

> **Version**: 1.2.0  
> **Last Updated**: 2026-02-12  
> **Compatibility**: Matches clarify-first/SKILL.md v1.2.0

When the user says "make it good/production-ready," check these:

## 1. Scale & Performance
*   **Latency**: Target response time (e.g., < 100ms p95).
*   **Throughput**: Requests per second (RPS) expected.
*   **Data Volume**: GBs vs TBs? Row counts?

## 2. Reliability & Resilience
*   **Availability**: SLA (99.9% vs 99.99%).
*   **Recovery**: RTO (Recovery Time Objective) / RPO (Recovery Point Objective).
*   **Fallbacks**: What if the database/API is down?

## 3. Security & Compliance
*   **Auth**: JWT, OAuth2, Session?
*   **Access Control**: RBAC, ABAC?
*   **Data Privacy**: GDPR, HIPAA (PII handling).
*   **Encryption**: At rest? In transit (TLS)?

## 4. Maintainability
*   **Testing**: Unit vs Integration coverage requirements.
*   **Docs**: OpenAPI, TSDoc, README?
*   **Code Quality**: Linting rules? Formatting standards?

## 5. Compatibility
*   **Browsers**: Chrome/Edge only vs IE11?
*   **Mobile**: Responsive design? Native?
*   **OS**: Linux/Windows/MacOS?

## 6. Observability (Ops)
*   **Metrics**: Prometheus/Datadog (CPU, Memory, Request Rate).
*   **Tracing**: Distributed tracing (OpenTelemetry) for microservices?
*   **Alerting**: Error rate thresholds? Latency spikes?
*   **Logs**: Centralized logging (ELK/Splunk)? Retention policy?