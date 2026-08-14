# Landing and distribution reasoning

## Contents

- [Distribution versus business plane](#separate-the-distribution-plane-from-the-business-plane)
- [Chain and decision points](#model-the-distribution-chain)
- [Artifact identity and signing](#connect-distribution-to-client-identity)
- [Third-party boundaries](#decide-whether-a-third-party-edge-deserves-depth)
- [Rotation, false positives and stopping](#reason-about-domain-rotation)

## Separate the distribution plane from the business plane

High-churn domains, nested redirects and static landing pages may exist mainly to select or distribute a current client. Treat them as a routing layer until they demonstrate ownership of identity, money, game, member or operational state.

The useful output of a distribution review is usually one of:

- a current byte-identical client artifact;
- the bootstrap/update source selected by that artifact;
- a current service relationship supported by a call site or response;
- an exact unresolved selector that blocks those conclusions.

After one of these is established, more mirror enumeration has lower value unless the user's question concerns reach, continuity or campaign structure.

## Model the distribution chain

A gambling entry point may be only one stage in a changing chain:

```text
promotion link
  -> landing/redirector
  -> domain selection or encoded next hop
  -> H5 entry or download page
  -> APK/IPA/profile package
  -> bootstrap/update endpoint
  -> current application services
```

Preserve the time and source of each hop. A domain observed today may be a transient selector, retired endpoint, CDN alias, campaign domain, or current service origin.

## Separate observation types

| Observation | What it suggests | What still needs confirmation |
|---|---|---|
| Encoded/obfuscated next URL | A redirect candidate | Decode provenance, selection logic, runtime use |
| Several alternate domains | Rotation, failover, campaigns, or mirrors | Selection source and current reachability |
| Download URL | Distribution relationship | Artifact hash, build identity, signing and update path |
| Mobile configuration/profile | Device enrollment or installation path | Payload contents, issuer, target app/site and current use |
| H5/WebView entry | Client shell or fallback | Runtime config and native bridge boundaries |
| Shared page resources | Common template or hosting | Uncommon code/config traits and independent signals |
| Customer-service/payment links | External or integrated service | Ownership, data flow and business role |

## Ask where decisions are made

For every redirect or download chain, locate the decision point:

- server-side redirect;
- JavaScript/configuration value;
- DNS or CDN behavior;
- geo/device/channel selection;
- embedded campaign parameter;
- remote configuration service;
- manual mirror list.

A current redirect response is stronger than an unused string. A call site plus runtime observation is stronger than a decoded value alone.

## Connect distribution to client identity

Record for each acquired artifact:

- content hash and byte size;
- package/bundle identifier and version;
- signing/provisioning fingerprint;
- channel/campaign parameters;
- source URL and collection time;
- embedded bootstrap/update relationship;
- relationship to other builds.

Two downloads with different filenames may be byte-identical. Two packages with the same interface may have different signing, configuration, or operator relationships.

## Treat signing and provisioning as an evidence chain

For signed mobile distribution, separate:

```text
profile/certificate material
  -> cryptographic identity and validity period
  -> package actually signed by that identity
  -> current distribution relationship
  -> provider or organization record
  -> bounded review or revocation request
```

Preserve the original package and provisioning material. Record package hash, signing fingerprint, team/organization identifiers, serial/validity information and verification method. A subject name alone may be reused, stale, repackaged or unrelated to current distribution; an actively distributed package with a verified signature is stronger.

## Decide whether a third-party edge deserves depth

Support, payment, analytics, signing and distribution services may be external control planes. Before investing in them, ask:

- Does the platform pass member, payment, operator or control data across the edge?
- Is the observed identifier tenant-specific or a commodity SDK value?
- Can the service answer the user's question more directly than the platform component?
- Does current evidence establish platform use rather than a dormant integration?

Stop at the provider boundary when it only establishes a shared vendor. Continue when the edge carries material data, configuration or operational control.

## Reason about domain rotation

Plausible explanations include:

- resilience against blocking;
- campaign or affiliate tracking;
- regional routing;
- CDN or hosting migration;
- tenant-specific branding;
- staged deployment;
- stale fallback configuration.

High-value discriminators include common bootstrap sources, uncommon response structure, identical signed artifacts, matching configuration hashes, current redirect relationships, and synchronized change over time.

## Avoid distribution false positives

- A public download does not establish backend access.
- A shared landing template may be sold or copied widely.
- An analytics/support identifier may belong to a service provider.
- A certificate or domain overlap needs collection time and tenancy context.
- A decoded URL is a lead until the code path or response selects it.
- A static CDN asset may be intentionally public while user uploads or origin APIs follow different controls.

## Useful stopping points

Stop the distribution branch when it has established the current artifact, current service relationship, or exact unresolved hop needed by the user's question. Broad mirror enumeration adds little after the causal edge is proven.
