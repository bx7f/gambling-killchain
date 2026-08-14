# Client and dynamic-configuration reasoning

## Contents

- [Artifact identity and bootstrap](#establish-client-identity-first)
- [Architecture and embedded material](#recognize-common-client-architectures)
- [Request trust](#reconstruct-request-trust-from-the-call-site)
- [Cryptographic properties and dispatch](#separate-secrecy-integrity-identity-and-authority)
- [Interface inventory](#build-an-interface-inventory-from-independent-sources)
- [Business pivots and runtime disagreement](#connect-client-observations-to-business-questions)

## Treat the client as executable evidence, not a string container

Client artifacts mix current code, dormant branches, vendor SDKs, test values, copied white-label modules, generated resources and remotely selected configuration. A useful observation includes its source location, call path, build identity and runtime relevance.

## Establish client identity first

Record:

- artifact hash, format and architecture;
- package/bundle identifier and version;
- signing/provisioning fingerprint;
- build channel and environment markers;
- framework and bundle type;
- embedded update/bootstrap metadata;
- acquisition source and time.

This lets later endpoint and family claims refer to a specific build rather than an app name or screenshot.

## Follow the bootstrap chain

A common reasoning chain is:

```text
embedded seed
  -> domain/config selector
  -> remote bootstrap document
  -> API, WebSocket, H5, game, payment, storage and update endpoints
  -> runtime feature/tenant selection
```

For each edge ask:

- where is the value read?
- what decoding, verification or fallback occurs?
- which build/environment condition selects it?
- what happens when it fails?
- is the result cached or refreshed?
- which downstream components consume it?

Preserve both the original encoded value and derived result as separate artifacts.

## Recognize common client architectures

### H5 and WebView shells

Look for boundaries among page origin, native bridge, local storage, deep links, file access, external navigation, downloads and device APIs. Determine which untrusted input can reach which native or authenticated capability.

### React Native, Hermes, Flutter and hybrid bundles

Separate native bootstrap, bundled application logic, downloaded updates and platform-specific bridges. Endpoint discovery is only the start; trace request construction, token retrieval, serialization and response handling.

### Native modules

Native libraries may hold pinning, signing, device identity, configuration decoding or provider integration. Use the smallest analysis that resolves the current missing edge.

## Interpret embedded material by purpose

| Material | Questions before assigning risk |
|---|---|
| Token/key/salt | Secret, identifier, public protocol constant, SDK credential, test value, or current server trust anchor? |
| API host/path | Current call site, fallback, vendor SDK, update service, or dead environment? |
| Certificate/pin | Which connection and failure path does it govern? |
| Storage URL | Public asset, upload origin, user content, update package, export, or log sink? |
| Feature/environment flag | Which runtime branch and tenant does it select? |
| Device identifier | Random, persistent, account-bound, spoof-sensitive, or risk-control input? |
| Update metadata | Who signs/selects the update and which code/resources can change? |

## Reconstruct request trust from the call site

Record the exact sequence for:

- identity/session acquisition;
- device and tenant identifiers;
- canonical serialization;
- timestamp/nonce handling;
- signature or encryption inputs;
- key/IV/nonce derivation;
- retry and refresh behavior;
- response verification and state update.

A reproduced algorithm becomes meaningful only when it matches a current request or known sample and its server-side trust role is understood.

## Separate secrecy, integrity, identity and authority

Client-side transformations are often described loosely as "encryption" or "signing." Decompose what the server actually receives:

| Property | Question |
|---|---|
| Encoding/obfuscation | Does the transform only change representation? |
| Confidentiality | Who besides the client and server can derive the plaintext? |
| Integrity | Which fields are covered, canonicalized and freshness-bound? |
| Client/app identification | Does a constant identify a build or tenant without identifying a user? |
| Session authentication | Which server-issued or independently held state binds the request to an identity? |
| Authorization | Which role, object, tenant and business state is checked after parsing? |

A client-embedded key, salt, token or derivation routine is available to every copy of that client. It may still support protocol compatibility or tamper friction, but it is not by itself proof of a distinct caller. Test whether the server adds independent session, device, freshness, tenant and object checks before claiming an authentication weakness.

## Model layered transformations and dispatch

Do not assume one algorithm or one host governs every request. A client may use:

```text
embedded/bootstrap transform
  -> anonymous or tenant configuration
  -> session-derived request transform
  -> CDN/API gateway dispatch
  -> origin service
```

Record a route matrix rather than flattening the behavior:

```text
method + logical path + selected host + required headers + identity state
  + transform/key source + response envelope + observed handler
```

Method-specific routing, host selection, version/app/tenant headers and CDN behavior can explain a working read beside a rejected write. Preserve the full request envelope and compare one routing variable at a time.

## Build an interface inventory from independent sources

Create sets from static call sites, bundled path tables, runtime captures, bootstrap/config documents, API descriptions and observed error routes. Normalize base paths and versions, then compare:

- referenced but never observed;
- observed but absent from the current bundle;
- reachable handlers still missing required identity or parameters;
- duplicate paths that differ by host, method, version or tenant.

This is an inventory and prioritization technique, not capability proof. A parameter error can establish route and handler reachability while leaving authentication, authorization and business effect unresolved.

## Connect client observations to business questions

Examples:

- agent-specific menu or route -> identify the role claim and corresponding backend enforcement;
- hidden admin URL -> verify current call path and identity boundary before classifying;
- bank-card or withdrawal model -> locate ownership, approval and state transitions;
- game launch builder -> locate provider token, member identity mapping and wallet mode;
- payment channel configuration -> locate order creation, callback binding and amount authority;
- upload bucket -> identify object naming, access identity and later retrieval path.

## Handle static/runtime disagreement

Static and runtime evidence may differ because of:

- remote feature flags;
- dynamic delivery or hot updates;
- environment/tenant selection;
- certificate or routing controls;
- obfuscation and reflection;
- dead code;
- server-side response selection.

Name the missing runtime observation and obtain the smallest capture that resolves it. Avoid expanding decompilation when the unresolved edge is a single runtime value.
