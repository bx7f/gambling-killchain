# Gambling platform ecosystem reasoning

## Contents

- [Five analysis lenses](#use-five-lenses-at-once)
- [Audit objectives](#keep-the-main-audit-objectives-visible)
- [Connected platform planes](#read-the-platform-as-connected-planes)
- [Artifact starting points](#start-from-the-strongest-supplied-artifact)
- [Causal edges and alternatives](#trace-causal-edges)

## Use five lenses at once

For every material observation, identify:

1. **Component** — landing, client, config, API, wallet, game provider, payment, storage, admin, or infrastructure.
2. **Actor** — visitor, member, agent, merchant, staff role, provider, or automated channel.
3. **Object** — account, order, wallet, bet, file, configuration, or relationship.
4. **State** — where the object is in its lifecycle and which transition is attempted.
5. **Tenant/operator boundary** — which brand, white label, merchant, provider, environment, or operator should own it.

Most important findings occur where one of these boundaries is missing or incorrectly joined.

## Keep the main audit objectives visible

Gambling-platform evidence usually contributes to one of these decisions:

- whether a member, agent, staff role or tenant crosses an expected data boundary;
- whether an actor can create or advance a business object through an unexpected state;
- whether wallet, order, callback or settlement integrity is affected;
- whether platform and game/payment providers bind the same player, order, amount and state;
- whether uploaded, exported or operational data follows its intended storage boundary;
- whether a client/distribution mechanism establishes a current backend relationship;
- whether shared software or infrastructure supports a family, deployment or operator claim;
- whether a discovered condition is isolated or repeatable across members, tenants, channels or brands.

Use the user's requested decision to select among these objectives. Broad coverage is secondary to proving the relevant causal chain.

## Read the platform as connected planes

### Acquisition and distribution plane

Typical components:

- promotion domains and landing pages;
- redirectors and domain-selection services;
- download pages, enterprise profiles, mobile configuration and QR links;
- H5 entry points and customer-service links;
- static CDN and update channels.

Questions:

- Which component selects the next domain or client build?
- Which values are static, remotely configured, or time-varying?
- Does a shared distribution mechanism imply a shared software family, reseller, or operator?

### Client and configuration plane

Typical components:

- H5/WebView shell;
- native APK/IPA;
- React Native, Flutter or Hermes bundles;
- bootstrap configuration;
- remote feature flags and update metadata;
- request signing and device identity.

Questions:

- Which backend relationships are reachable in this build?
- Which endpoints come from current runtime configuration?
- Which embedded values belong to third-party SDKs, test environments, or dead code?

### Identity and business plane

Typical components:

- member authentication and device sessions;
- agent, merchant and staff identities;
- profile, bank-card and wallet records;
- promotion, turnover and risk-control logic;
- game launch, bet and settlement records.

Questions:

- Which role owns, creates, approves, views, or transitions each object?
- Which tenant or hierarchy boundary should apply?
- Which state transition carries money, data, or operational authority?

### Money and provider plane

Typical components:

- platform wallet and provider wallet;
- deposit and payment orders;
- withdrawal and payout orders;
- channel callbacks and reconciliation;
- game-provider launch tokens and balance transfers.

Questions:

- Which system is authoritative for amount and state?
- Which identifiers bind user, order, merchant and channel?
- How are retries, duplicate callbacks, reversal and manual adjustment represented?

### Data and operations plane

Typical components:

- object storage and CDN;
- uploaded identity/payment material;
- exports, logs and backups;
- customer-service, finance, risk-control and admin systems;
- shared deployment and white-label infrastructure.

Questions:

- Which data class is exposed by each object or export?
- Is a public edge resource distinct from origin permission?
- Does infrastructure overlap support software similarity, shared tenancy, or operator identity?

## Start from the strongest supplied artifact

| Starting evidence | Highest-value first questions |
|---|---|
| Landing page | Where do redirects, downloads and runtime domains originate? |
| APK/IPA/bundle | Which current call sites establish backend, update, payment or storage relationships? |
| HAR or captured request | Which identity, object, state and expected authorization does it represent? |
| API response | Which layer succeeded: route, handler, identity, business operation, or data access? |
| Payment record | Which order identifiers, amount source, state transitions and callbacks bind the systems? |
| Storage URL | Is it CDN delivery, bucket origin, uploaded user content, export, or public asset? |
| Domain/certificate set | Which overlaps are uncommon, current and independent? |

## Trace causal edges

Use an explicit graph:

```text
promotion -> distribution -> client build -> runtime config -> request
request -> identity -> business object -> state transition -> data/money effect
artifact/infrastructure traits -> software family -> deployment relation -> operator claim
```

Test missing edges before exploring adjacent components. A client hostname alone does not establish runtime use; a valid handler alone does not establish access; a shared CDN alone does not establish common operation.

## Common competing explanations

Keep relevant alternatives alive:

- dead or dormant client code;
- test/staging configuration shipped in production;
- third-party game, payment, analytics, support or update service;
- reseller or white-label reuse;
- shared hosting/CDN tenancy;
- public game metadata or demo data;
- stale rotating domain;
- copied/repacked client;
- cached response or routing fallback;
- current common operator.

Choose tests that distinguish these explanations rather than merely collecting more matching strings.
