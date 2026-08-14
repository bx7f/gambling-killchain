# Storage, infrastructure and software-family reasoning

## Contents

- [Storage role and capabilities](#place-storage-in-the-business-flow)
- [Object provenance and sensitivity](#follow-object-provenance)
- [Distribution catalogs](#treat-distribution-storage-as-a-catalog-then-validate-each-edge)
- [Infrastructure claims](#connect-infrastructure-observations-carefully)
- [White-label and family hypotheses](#recognize-white-label-structure)
- [Signal independence](#test-signal-independence)
- [Provider semantics](#use-current-provider-semantics)

## Place storage in the business flow

A bucket, object URL or CDN hostname has meaning only through its role:

- public client assets and update packages;
- landing-page resources;
- game/provider media;
- member avatars or uploaded documents;
- bank-card, identity or payment material;
- customer-service attachments;
- reports and exports;
- logs, backups and configuration;
- temporary upload/download exchange;
- white-label tenant assets.

Trace how the client or API creates, names, authorizes, retrieves and expires the object.

## Keep storage capabilities independent

| Capability | Direct question |
|---|---|
| Resource distinction | Was bucket/object existence separated from endpoint, routing or region mismatch? |
| Listing | Can the tested identity enumerate keys? |
| Object metadata/read | Can it inspect or retrieve one known object? |
| ACL/policy/config read | Can it retrieve configuration metadata? |
| Upload/write/delete | Does evidence establish a mutation capability under defined conditions? |
| Signed/presigned access | Which identity, object, method and expiry are bound? |
| CDN delivery | Does the edge serve content without proving origin permission? |

A denied list can coexist with a readable known object. A public list can coexist with denied object reads. Policy text requires structural evaluation of principals, actions, resources, conditions and explicit denies.

## Follow object provenance

For a material object record:

- source API/client call site;
- tenant/member/order relationship;
- key naming and predictability;
- upload identity and constraints;
- content-type and metadata handling;
- retrieval identity;
- signed URL scope and expiry;
- CDN/origin relationship;
- retention, overwrite and deletion behavior;
- data sensitivity.

An object key match may reveal a naming family, but access impact depends on the tested identity and retrieval path.

## Distinguish public assets from sensitive objects

Intentionally public material may include app packages, static bundles, logos, game media, public announcements and promotion assets. Higher-sensitivity candidates may include identity documents, bank-card material, customer-service attachments, exports, transaction records, configuration, logs and backups.

Classify from content purpose, path provenance and application relationship rather than filename alone. Use minimized samples, hashes, field names and counts in reports.

## Treat distribution storage as a catalog, then validate each edge

An exposed package repository or configuration catalog can reveal artifact hashes, brand/tenant naming, build history, update relationships and signing diversity. Convert it into a relationship table:

```text
object -> artifact hash -> package identity -> signing identity
  -> bootstrap/config schema -> tenant/brand -> collection time
```

Counts and repeated naming patterns describe the repository. They do not establish that every object is current, operational or controlled by one operator. Validate current distribution or runtime selection for representative artifacts before expanding a family claim.

## Connect infrastructure observations carefully

Possible observations:

- DNS answers and historical changes;
- TLS certificate fingerprints and SANs;
- CDN, ASN, hosting and region;
- HTTP headers and response structure;
- storage endpoint and bucket naming;
- download/update infrastructure;
- analytics, support, error-reporting and push services;
- shared admin, agent or API path sets;
- signing certificates and artifact hashes.

Name the claim type before weighing the signals:

```text
content similarity
  -> shared codebase/software family
  -> shared deployment or provider tenant
  -> coordinated operation
  -> operator identity
```

Evidence weakens as the claim moves right unless new independent signals support the transition.

## Recognize white-label structure

White-label platforms can share:

- client code and resource layout;
- bootstrap/config schema;
- API path conventions;
- request signing and response envelopes;
- game/payment/support integrations;
- admin and agent products;
- deployment templates and storage patterns.

They may still differ in tenant, merchant, brand, payment channels, signing certificates, infrastructure ownership and operation. A shared codebase supports a software-family claim more readily than a common-operator claim.

## Maintain family knowledge as hypotheses

Useful recurring traits include:

- package/resource structure;
- signing/provisioning fingerprints;
- uncommon configuration keys or schema;
- endpoint-set combinations;
- request derivation shape;
- response/business-state vocabulary;
- update and redirect mechanisms;
- storage naming/resource structure;
- admin/agent/client relationships;
- provider integration combinations.

Store traits with:

```text
trait type and redacted/hash value
first seen and last verified
source evidence IDs
current confidence and expiry
known contradictions
commodity/shared-service explanation
best current confirmation test
```

Bundled or historical traits generate leads. Current-case confirmation supplies evidence.

High-value horizontal pivots are relationships already present in current artifacts: bootstrap hosts, update channels, storage endpoints, uncommon configuration fields, tenant codes, signing identities and provider combinations. Test each discovered asset independently. A guessed bucket, inferred tenant or test/staging label remains a lead until a current artifact or response selects it.

## Test signal independence

Ask:

- Do several matches come from the same copied client or SDK?
- Could one CDN, support, analytics, payment or game provider explain them?
- Are observations current at the same time?
- Is the trait uncommon within the relevant ecosystem?
- Does a contradiction separate tenant/operator despite shared software?
- Could repackaging or reselling explain the artifact relationship?

Prefer pairwise claims with supporting observations, contradictions and alternatives over one global attribution narrative.

## Use current provider semantics

When interpreting storage operations or preparing provider reports, consult current primary documentation and record access time. Stable starting points include:

- AWS S3 IAM operation mapping: https://docs.aws.amazon.com/AmazonS3/latest/userguide/security_iam_service-with-iam.html
- AWS S3 HeadObject: https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadObject.html
- Alibaba OSS GetObject: https://help.aliyun.com/en/oss/developer-reference/getobject

Provider documentation explains operation semantics; current observations establish the resource state.
