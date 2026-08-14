---
name: gambling-killchain
description: Guide evidence-led security investigations of gambling platforms across landing and distribution infrastructure, H5/APK/IPA clients, dynamic configuration, member and agent APIs, game aggregation, wallets, deposits, withdrawals, payment callbacks, object storage, admin systems, and software-family correlation. Use when an agent must understand gambling-specific roles, business states, component relationships, or recurring platform patterns to choose the next discriminating audit test and calibrate findings. Prefer a generic security skill for unrelated applications or isolated technical questions.
metadata:
  runtimes:
    - codex
    - claude-code
  invocation:
    codex: "$gambling-killchain"
    claude-code: "/gambling-killchain"
---

# Gambling Platform Audit Reasoning

Think like an investigator who understands the gambling platform as a connected business system. Build the shortest reviewable chain from current evidence to the user's question. Transfer domain judgment rather than a fixed scan sequence.

## 1. Restore the current case

1. Resolve `SKILL_DIR` once to the directory containing this `SKILL.md`; do not assume the current working directory.
   - In Claude Code, set `SKILL_DIR="${CLAUDE_SKILL_DIR}"`.
   - In Codex, set `SKILL_DIR` to the absolute directory shown in the available-Skills entry.
   - Resolve every bundled `references/`, `assets/`, and `scripts/` path below relative to `SKILL_DIR`.
2. Restate the user's decision question in one sentence.
3. Inspect existing artifacts, captures, hashes, notes, negative results, and reports.
4. Separate current-case facts from inherited family leads and generic expectations.
5. Locate the current artifact or observation in the platform map below.
6. Identify the one uncertainty that most limits the answer.
7. Preserve completed work and continue from the last confirmed state.

Initialize a compact evidence directory only when persistent output is useful:

```bash
python3 "$SKILL_DIR/scripts/evidence.py" init \
  --case-id CASE_ID --root evidence --question "QUESTION"
```

## 2. Place observations in the gambling ecosystem

Use this map to understand relationships, not as a mandatory path:

```text
promotion / landing / domain rotation
  -> H5, WebView, APK, IPA, download and update channels
  -> bootstrap and dynamic configuration
  -> member, agent, merchant, customer-service and admin APIs
  -> identity, device, wallet, promotion and risk-control services
  -> game lobby, provider launch tokens, betting and settlement records
  -> deposit, payment, withdrawal, payout and callback channels
  -> object storage, CDN, logs, exports and uploaded identity/payment material
  -> shared infrastructure, white-label codebase and operator/family claims
```

Cross to a new component only when an observed edge supports it. For example, a client call site may justify an API question; an API response may justify an object-authorization test; a payment order may justify a callback-state question.

Treat the visible Web surface as a distribution plane until evidence shows that it owns business state. Redirectors, mirrors and static landing pages often have lower evidence density than the selected client artifact, bootstrap document, request builder, business API or third-party control plane. Use the entry chain to locate those components, then pivot to the component that can answer the decision question.

## 3. Load the minimum domain reference

| Current observation or uncertainty | Read first |
|---|---|
| Platform topology, component ownership, or where to start | `references/gambling-ecosystem.md` |
| Landing pages, rotating domains, downloads, redirects, profiles, or distribution | `references/landing-and-distribution.md` |
| APK/IPA/H5/WebView/RN/Hermes, bootstrap config, signing, pinning, or updates | `references/client-and-dynamic-config.md` |
| Member/agent/admin roles, object access, promotions, betting, settlement, or business states | `references/api-role-and-business-logic.md` |
| Wallets, deposits, withdrawals, payment/payout orders, callbacks, or reconciliation | `references/payment-wallet-and-callback.md` |
| Buckets/CDNs, shared infrastructure, white labels, family fingerprints, or attribution | `references/storage-infrastructure-and-family.md` |
| Evidence strength, severity, standards, or report construction | `references/evidence-and-reporting.md` |

Read one reference first. Add another only when the evidence crosses that boundary.

## 4. Use the gambling-specific reasoning loop

Repeat while a material uncertainty remains:

1. **Observe** — record what the artifact, request, response, state, or infrastructure directly shows.
2. **Locate** — identify the component, role, business object, and state transition involved.
3. **Explain** — maintain plausible alternatives such as dead client code, test configuration, shared SaaS, demo data, public game metadata, white-label reuse, stale domain, CDN delivery, or current operator behavior.
4. **Discriminate** — choose the smallest comparison whose outcomes separate those explanations.
5. **Execute** — use the least active method that produces adequate evidence.
6. **Update** — strengthen, weaken, reject, or split the hypotheses.
7. **Decide** — validate a capability, record an exact boundary, or select the next test.

Prefer controlled comparisons: one role, object, state, parameter, route, or time variable at a time.

An access gate is a boundary observation, not a reason to spend the rest of the review on that gate. When login, CAPTCHA, middleware or role checks hold, compare the declared public, visitor, demo, trial, registration, bootstrap, download and callback surfaces that participate in the same business flow. Record the held boundary and move only along evidence-backed edges.

## 5. Model roles, objects, and states explicitly

For API and business-flow questions, write down:

```text
actor role -> action -> business object -> current state -> expected owner/approver -> observed effect
```

Common actors include visitor, demo user, member, promoter, agent, sub-agent, merchant, customer service, finance, risk control, operations, administrator, game provider, payment channel, and payout channel.

Common objects include account, device, wallet, bank card, crypto address, deposit order, withdrawal order, payout order, promotion, turnover requirement, game session, bet, settlement, agent tree, commission record, uploaded file, and export.

A finding needs the unexpected role/object/state relationship, not merely a successful response.

## 6. Keep claims on the evidence ladder

```text
lead -> observation -> reproduced capability -> validated finding -> family/operator claim
```

- Embedded strings, domains, status codes, framework markers, SDK keys, and family patterns are **leads**.
- Preserved artifacts and responses are **observations**.
- A controlled test under a defined identity and state is a **reproduced capability**.
- Capability plus access expectation, affected scope, and impact is a **validated finding**.
- Family or operator claims require independent current signals and competing explanations.

Several signals that share one underlying source remain one evidence family.

## 7. Choose the next test by information value

Compare candidate tests using:

- **Discriminating power:** do competing explanations predict different outcomes?
- **Business relevance:** could the result change a role, money, data, game, or operator conclusion?
- **Decision actionability:** would a reviewer, provider, platform owner or investigator know what bounded action the result supports?
- **Evidence quality:** will the output be independently reviewable?
- **Scope fit:** does it stay within the selected artifact, host, identity, object, and action class?
- **Cost and reversibility:** prefer offline, passive, and read-only observations at the lowest adequate volume.
- **Reuse:** will it resolve several downstream questions?

Prefer depth on the missing causal edge over broad enumeration.

## 8. Preserve only material evidence

```bash
python3 "$SKILL_DIR/scripts/evidence.py" add \
  --case-dir evidence/CASE_ID --file PATH \
  --test-id TEST_ID --source SOURCE --notes "DIRECT OBSERVATION"

python3 "$SKILL_DIR/scripts/evidence.py" verify \
  --case-dir evidence/CASE_ID
```

Keep raw bytes unchanged. Store decoded, normalized, redacted, or summarized derivatives separately. Use notes for direct observations; keep larger interpretations in the reasoning ledger or report.

Preserve negative results with the same identity, route, request class, object/state and time context as positive results. A denied or filtered comparison defines the demonstrated boundary, prevents repeated work and may falsify a broader hypothesis.

## 9. Finish at the decision boundary

Stop when the user's question is answered, competing explanations converge, the next useful test depends on a named missing input, or remaining work is unlikely to change the decision.

Return:

1. the gambling-specific question answered;
2. confirmed component, role, object, and state observations;
3. validated findings;
4. rejected or weakened explanations;
5. unresolved uncertainty and its best next discriminating test;
6. exact evidence paths and manifest verification result.

Use `assets/templates/report.md` as a flexible structure and omit irrelevant sections.
