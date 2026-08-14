# API roles and business-logic reasoning

## Contents

- [Role, object and success models](#model-authorization-as-a-business-relationship)
- [Authorization comparisons](#design-authorization-comparisons)
- [Low-friction identities](#map-low-friction-identity-issuance-as-its-own-state-machine)
- [Inventory difference and write validation](#use-inventory-union-and-tested-set-difference)
- [Account, agent and promotion states](#reason-about-member-and-account-lifecycle)
- [Games and settlement](#reason-about-games-bets-and-settlement)
- [False positives and stopping](#recognize-gambling-specific-false-positives)

## Model authorization as a business relationship

For every material API operation, write:

```text
actor role -> function -> object -> owner/tenant -> current state -> expected decision -> observed result
```

A route or successful status is not the security claim. The claim is that a defined actor obtained an unexpected capability over a defined object or transition.

## Build the role model from current evidence

Common roles are hypotheses until the client, API, data model or workflow confirms them:

| Role family | Typical relationships to test |
|---|---|
| Visitor/demo | Public configuration, demo game/data, registration and unauthenticated entry |
| Member | Own profile, devices, wallet, cards, deposits, withdrawals, bets and promotions |
| Promoter/affiliate | Campaign links, registrations, statistics and attribution |
| Agent/sub-agent | Downline hierarchy, commissions, reports, member management and scoped operations |
| Merchant/tenant | Brand configuration, channels, member population and tenant-specific reports |
| Customer service | Member lookup, communication and limited account assistance |
| Finance | Deposit/withdrawal review, payout, reconciliation and manual adjustments |
| Risk control | Device/account flags, limits, review state and decision evidence |
| Operations/admin | Configuration, promotions, games, roles, exports and system actions |
| Game provider | Launch session, player mapping, wallet transfer, bet and settlement events |
| Payment/payout channel | Order creation, callback, status query and reconciliation |

Distinguish role identity from client UI. Hidden buttons and route guards may be presentation controls while the API makes the actual decision.

## Inventory business objects

Track stable object relationships:

- account and member profile;
- device/session/token;
- agent tree and referral binding;
- bank card and crypto address;
- wallet and ledger entry;
- deposit/payment order;
- withdrawal/payout order;
- promotion and turnover requirement;
- game session/provider account;
- bet, result, settlement and reversal;
- support conversation and risk review;
- upload, report and export;
- tenant, merchant, channel and configuration.

Object identifiers may be numeric, UUID-like, composite, encoded, indirect through current session, or mapped across providers. Establish how the server binds the identifier to role, tenant and state.

## Decompose API success

Reason through separate layers:

```text
transport -> route -> handler -> identity -> role/function -> object ownership
  -> business preconditions -> state transition -> returned data/effect
```

Examples:

- a parameter error establishes handler reachability;
- a token accepted by middleware establishes identity parsing;
- a record returned establishes data access only after public/demo/cache explanations are addressed;
- a success object establishes a business effect only when subsequent state or ledger evidence confirms it.

## Design authorization comparisons

Choose comparisons that answer a defined boundary:

### Identity comparison

Compare no identity, expired/invalid identity, and the supplied current identity when route and caching explanations matter.

### Object comparison

Compare an object clearly owned by the actor with another known object while keeping role, function and request shape stable. Predictions must be defined before execution.

### Role/function comparison

Compare a member operation with an agent, finance or admin capability only where current evidence identifies the expected role boundary.

### Tenant/hierarchy comparison

For agent and white-label systems, distinguish:

- own member versus another agent's member;
- direct downline versus deeper hierarchy;
- same tenant versus another tenant;
- own campaign/channel versus another channel;
- aggregate statistic versus member-level detail.

### State comparison

Compare operations across legitimate and illegitimate states, such as pending versus completed, reviewed versus approved, unsettled versus settled, active versus frozen, or unmet versus met turnover requirements.

Change one meaningful variable at a time. Preserve both sides of the comparison.

## Map low-friction identity issuance as its own state machine

Visitor, demo, guest, trial and newly registered identities may receive different tokens and capabilities from a normal member. Derive the actual transitions:

```text
anonymous -> bootstrap identity -> demo/trial identity -> registered member
          -> verified or funded member -> restricted/frozen member
```

Record who can obtain each identity, which verification occurred, token audience/tenant/device binding, expiry and refresh behavior, and the first business capability each state unlocks. A trial token reaching a member handler is only a finding when the expected role/object/state boundary and resulting data or effect are demonstrated.

When a primary login has a strong challenge, preserve that boundary and inspect documented or client-referenced registration, demo and guest flows that participate in the same product. This answers whether the platform intentionally exposes a lower-trust identity path without treating the login gate as the whole attack surface.

## Use inventory union and tested-set difference

Maintain separate sets for:

- paths referenced by current client call sites;
- paths observed at runtime;
- routes that reach a handler;
- routes that accept the current identity;
- routes with validated object access or business effects.

The difference between these sets chooses follow-up tests and prevents a long endpoint list from being mistaken for an exposed capability. Normalize HTTP method, version prefix, base path, host and tenant context before comparing.

## Validate write surfaces in stages

For feedback, support, reply, upload, profile and configuration operations, distinguish:

```text
request accepted -> value persisted -> value retrieved -> value interpreted
  -> privileged consumer reached -> durable business or security effect
```

A success envelope proves only the stage directly observed. When content interpretation matters, use a small comparison matrix that distinguishes rejection, normalization, stripping, encoding, storage and later rendering. Preserve the accepted input and downstream representation separately; do not infer a privileged effect from submission success alone.

## Interpret technical controls in business context

Generic web and API controls matter through the capability they protect:

| Technical observation | Gambling-platform question |
|---|---|
| Session/token handling | Which member, device, tenant and role does the server bind to the request? |
| CORS or browser policy | Does the browser gain access to an authenticated business capability, or only public configuration? |
| WebSocket/SSE subscription | Which member, table/game, order or agent scope can the connection observe? |
| Upload or file reference | Who chooses the object key, content, tenant and later reader? |
| Export/report endpoint | Does aggregation expand into member-level, payment, betting or agent data? |
| Rate/risk response | Which action is limited: login, registration, order creation, withdrawal, game launch or lookup? |
| Admin-looking route | Which current identity and backend function are actually reachable? |
| Error/detail leakage | Does it expose current object existence, state, role structure or provider integration? |

Use generic vulnerability knowledge to form tests, then describe the finding in terms of the protected business relationship.

## Reason about member and account lifecycle

Potential state questions include:

```text
unregistered -> registered -> verified -> active -> restricted/frozen -> closed
session issued -> refreshed -> revoked/expired
unbound device -> trusted device -> changed/revoked device
```

Ask which evidence authorizes transitions, whether revocation propagates, and which operations remain available in each state. A client-side restriction is relevant only when tied to backend enforcement.

## Reason about agent and commission systems

Agent systems add hierarchy and aggregation boundaries:

- referral/agent binding creation and change;
- downline visibility and search;
- commission rules, periods and settlement;
- member-level versus aggregate reporting;
- role delegation and sub-account permissions;
- tenant/brand separation;
- exports and batch operations.

Shared totals may be intended while member-level personal, payment or betting data follows tighter boundaries. Establish the expected granularity before classifying a response.

## Reason about promotions and turnover

Model promotion objects and prerequisites:

- eligibility and enrollment;
- award creation;
- wallet or balance destination;
- turnover calculation and completion;
- expiration, cancellation and reuse;
- relationship to withdrawal eligibility;
- tenant, channel and member binding.

A displayed promotion is public configuration; an unexpected award, state transition, wallet effect or cross-member access is a different claim.

## Reason about games, bets and settlement

Separate platform and provider responsibilities:

```text
member/platform identity
  -> provider launch/session identity
  -> game/bet request
  -> provider result
  -> settlement/ledger event
  -> platform history and balance
```

Questions:

- How is the platform member mapped to the provider player?
- Is the wallet integrated, transferred, or provider-held?
- Which system is authoritative for balance and settlement?
- How are duplicate events, reversals, cancellations and delayed results handled?
- Which bet/history fields are public game metadata versus member-specific records?
- Which tenant or currency context is carried across the provider boundary?

A launch token or game URL is a lead until identity scope, expiry, intended audience and resulting capability are established.

## Recognize gambling-specific false positives

- Public odds, game lists, provider catalogs and announcement data may be intentionally public.
- Demo accounts or game simulations may return fixed sample data.
- Aggregate agent statistics may be intended while member-level records remain restricted.
- Third-party provider errors may be wrapped in platform success envelopes.
- A wallet field name does not prove access to a live balance.
- A payment order status response does not by itself prove cross-owner visibility.
- Admin-looking routes may belong to unused front-end bundles or shared white-label modules.

Validate semantics, identity, object ownership, state and resulting effect before assigning impact.

## Stop at the business boundary

A strong conclusion states:

- actor and role;
- function performed;
- object and expected owner/tenant;
- starting and resulting state;
- returned data or durable effect;
- scope established;
- competing explanations tested;
- exact untested boundary.
