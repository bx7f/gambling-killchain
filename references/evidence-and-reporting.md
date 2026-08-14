# Gambling audit evidence and reporting

## Contents

- [Atomic tests and claim schemas](#define-the-test-as-a-business-question)
- [Finding and impact validation](#validate-findings-as-arguments)
- [Fingerprint and prerequisite ladder](#separate-fingerprint-prerequisite-and-reproduced-capability)
- [Negative and decision-actionable evidence](#preserve-negative-results-as-boundary-evidence)
- [Three-layer result summary](#use-an-honest-three-layer-result-summary)
- [Data minimization and standards](#minimize-gambling-platform-data)
- [Report construction](#write-around-the-requested-decision)

## Define the test as a business question

A reviewable test records:

```text
test_id
business/security question
component, actor role, identity and tenant
business object and starting state
method and controlled variable
predictions for competing explanations
raw observation
resulting capability or exact boundary
evidence IDs and hashes
limitations
```

Separate discovery tests from capability validation and family/operator correlation.

## Keep domain claims structured

### Client/distribution claim

Record artifact/build identity, source location, runtime reachability, selected configuration, downstream relationship and current-time evidence.

### API/business claim

Record actor role, function, object, expected owner/tenant, starting state, observed data/effect, affected scope and comparison evidence.

### Money claim

Record authoritative system, order IDs, amount/currency/unit, starting/resulting states, ledger or external effect, repeatability and reconciliation evidence.

### Storage claim

Record identity, exact bucket/object capability, object provenance, content class, CDN/origin distinction and policy/condition limitations.

### Family/operator claim

Record claim type, independent current signals, contradictions, shared-service/white-label alternatives, time alignment and confidence rationale.

## Preserve evidence boundaries

A material artifact record should contain source, collection time, content hash, byte size, media type, storage path, related test and a short direct observation. Preserve raw bytes; store normalized, decoded, redacted or summarized derivatives separately.

A hash establishes integrity for the recorded bytes. Source truth, ownership, completeness and collection route require separate evidence.

## Validate findings as arguments

A validated finding answers:

- Which gambling-platform component was tested?
- Which actor, role, tenant and identity were involved?
- Which business object and state transition were involved?
- What capability or durable effect was reproduced?
- Why was it unexpected?
- What data, money, game, agent or operational scope was established?
- Which demo/public/vendor/cache/white-label explanations were tested?
- Which uncertainty remains?
- Which evidence supports every material statement?

## Calibrate impact by the demonstrated level

Distinguish:

1. route or handler reachability;
2. metadata/configuration visibility;
3. member or agent data visibility;
4. cross-object or cross-tenant access;
5. business-state influence;
6. wallet or ledger influence;
7. external payment/payout effect;
8. staff/admin operational control;
9. repeatable or scalable scope.

State the demonstrated level before attaching severity. Product name, status code, scanner rating and standards mapping supply context rather than impact proof.

## Separate fingerprint, prerequisite and reproduced capability

For framework, library and deployment observations, use this ladder:

```text
product/framework fingerprint
  -> version or affected-range hypothesis
  -> required deployment and configuration prerequisites
  -> current route/component reachability
  -> reproduced capability and business impact
```

Error text, package names, documentation pages and version strings can support the first two levels. They do not establish that the relevant module, packaging form, route, configuration or vulnerable code path is active. Report the exact confirmed level and name the missing prerequisite instead of collapsing a version match into exploitability.

## Preserve negative results as boundary evidence

For every material denial or filtered result, retain:

- identity/role and tenant;
- host, method, normalized route and request class;
- object and starting state;
- response code/business code and stable response fingerprint;
- relevant headers or protection layer;
- collection time and evidence ID;
- which hypothesis it weakened and which boundary it demonstrated.

Group equivalent results by a reproducible fingerprint rather than storing every duplicate response. Negative evidence is especially valuable for avoiding repeated tests and showing that a reported capability is narrower than the surrounding surface.

## Rank evidence by decision actionability

There is no universal asset ordering. A signing artifact, backend relationship, payment configuration, member record or operational account has value only relative to the requested decision. Score candidate evidence using:

| Dimension | Question |
|---|---|
| Directness | Does it directly prove the claimed component, identity, capability or relationship? |
| Authority | Is it the authoritative artifact/system for the claim? |
| Freshness | Is current use or distribution established at a recorded time? |
| Independence | Does it add a new evidence family rather than repeat one source? |
| Scope | Is the affected artifact, tenant, role, data or money boundary defined? |
| Executability | Can the intended reviewer take a bounded, named action from it? |
| Minimization | Can that action be supported without unnecessary personal or bulk data? |

Examples of bounded actions include reviewing a currently distributed signing identity, disabling a confirmed exposed object path, correcting an authorization decision, rotating a demonstrated client-trusted credential, or investigating a verified infrastructure relationship. State the supporting evidence chain and the exact owner of the next decision.

## Use an honest three-layer result summary

Present conclusions as:

1. **Confirmed capability or relationship** — reproduced with its business scope and evidence.
2. **Lead with unresolved prerequisites** — version, route, artifact or configuration match whose decisive condition remains named.
3. **Boundary held or hypothesis rejected** — controls and negative comparisons that constrained the claim.

This makes a compact report useful even when the most important result is a verified boundary or a decision-ready artifact rather than a long finding count.

## Minimize gambling-platform data

Prefer:

- counts instead of bulk rows;
- field names instead of full personal records;
- redacted member/order/card/address identifiers;
- hashes and object metadata instead of distributing content;
- one representative comparison instead of broad enumeration;
- time-bounded observations and explicit scope.

Separate raw evidence from the report artifact.

## Use standards as indexes

Map only where the current test objective directly applies and record version/access date:

- OWASP WSTG v4.2: https://owasp.org/www-project-web-security-testing-guide/v42/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- OWASP API Security Top 10 2023: https://owasp.org/API-Security/editions/2023/en/0x10-api-security-risks/
- OWASP MASVS/MASTG: https://mas.owasp.org/MASTG/
- MASTG atomic tests: https://mas.owasp.org/MASTG/tests/
- NIST SP 800-115: https://csrc.nist.gov/pubs/sp/800/115/final
- NIST SP 800-86: https://csrc.nist.gov/pubs/sp/800/86/final

Coverage mapping and finding severity answer different questions.

## Write around the requested decision

A useful report contains only relevant sections:

1. question and concise answer;
2. ecosystem components and scope;
3. confirmed observations;
4. validated findings;
5. role/object/state or money-flow diagrams where needed;
6. rejected and weakened explanations;
7. unresolved uncertainty and next discriminating test;
8. evidence index and manifest verification.

For provider or infrastructure reporting, identify provider-hosted resources, collection time, exact observed behavior, evidence hashes and the specific requested review. For a technical vulnerability report, prioritize reproduction, affected business relationship, impact, remediation and verification.
