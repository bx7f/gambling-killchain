# Payment, wallet and callback reasoning

## Contents

- [Ledger and money domains](#start-with-the-ledger-not-the-screen)
- [Channel configuration](#separate-channel-configuration-from-current-money-movement)
- [Deposit and withdrawal states](#model-deposit-and-payment-orders)
- [Callback trust](#analyze-callbacks-as-trust-transitions)
- [Wallet and precision models](#reason-about-wallet-transfers-and-game-providers)
- [Idempotency and reconciliation](#analyze-idempotency-and-race-conditions-conceptually)
- [Impact calibration](#calibrate-money-findings-carefully)

## Start with the ledger, not the screen

Money-related UI and API fields may represent available balance, locked balance, promotional balance, provider balance, pending amount, display conversion, or cached summary. Identify the authoritative ledger and the event that changes it.

Use a flow model:

```text
actor -> order/request -> channel/provider -> callback/status event
  -> platform state transition -> ledger entries -> reconciliation
```

For every amount-bearing observation record currency, unit, precision, sign, source system, order identity, member/merchant binding and state.

## Distinguish money domains

Common domains include:

- main/platform wallet;
- game-provider wallet or transfer wallet;
- promotional/bonus balance;
- locked/turnover-restricted balance;
- deposit/payment order;
- withdrawal request;
- payout/代付 order;
- agent commission;
- manual adjustment;
- reversal, refund or correction;
- displayed exchange or virtual-currency value.

A number with a money-like field name remains an observation until its ledger meaning and authority are established.

## Separate channel configuration from current money movement

Payment and payout configuration can establish a current integration lead: channel identifiers, supported currencies, limits, account-rule schemas, callback families or provider-specific response shapes. It does not by itself establish transaction volume, beneficiary identity, successful settlement or current operator control.

For an action-oriented conclusion, connect configuration to the smallest adequate current evidence:

```text
tenant/member context -> order or rule selection -> channel relationship
  -> current state/status evidence -> ledger or reconciliation meaning
```

Keep sensitive payment identifiers minimized and distinguish platform-owned fields from third-party channel metadata.

## Model deposit and payment orders

A typical lifecycle may include:

```text
created -> channel selected -> pending payment -> channel confirmed
  -> credited -> reconciled
             \-> failed / expired / cancelled / corrected
```

Current implementations vary; derive the actual states from requests, responses, client handling, database/export evidence or callbacks.

Questions:

- Who chooses member, merchant, channel, currency and amount?
- Which values are trusted from the client and which are recomputed?
- How are platform order ID and channel order ID bound?
- Which event authorizes credit?
- How are duplicate, delayed, reordered or contradictory events handled?
- What makes an order final, reversible or manually correctable?
- Which tenant/channel credentials and callback routes apply?

## Model withdrawal and payout

Separate the member request from downstream payout execution:

```text
withdrawal requested
  -> eligibility/turnover/risk checks
  -> review/approval
  -> payout order submitted
  -> channel result/callback
  -> completed, failed, returned or manually resolved
```

Track:

- member and wallet ownership;
- destination bank card or crypto address;
- amount, fee, currency and precision;
- turnover and risk-control prerequisites;
- reviewer/approver role;
- payout channel and external order ID;
- retry and manual-resolution behavior;
- ledger holds, deductions and reversals.

A status change in one system may precede or follow the actual money movement. Seek the authoritative event and corresponding ledger entries.

## Analyze callbacks as trust transitions

For a current callback implementation identify:

- endpoint and tenant/channel selection;
- authentication or signature inputs;
- canonical field ordering and encoding;
- timestamp/nonce/replay handling;
- order lookup key;
- trusted amount, currency and status fields;
- idempotency key and duplicate behavior;
- response acknowledgment and provider retry behavior;
- state transition and ledger side effects;
- reconciliation path for disagreement.

The security question is which callback properties the platform independently binds to the original order before accepting a transition.

## Use controlled callback reasoning

Before testing, define predictions for safe comparisons such as:

- exact captured structure versus one malformed/nonmaterial field;
- known order versus nonexistent order;
- correct tenant/channel context versus mismatched context;
- first delivery versus duplicate delivery;
- expected state versus already-final state;
- platform status query versus channel status evidence.

Use the lowest-impact observation that resolves validation, binding, idempotency or state-machine uncertainty. Durable money effects require additional safeguards and evidence review.

## Reason about wallet transfers and game providers

Possible wallet models:

1. **Single/integrated wallet** — provider events affect the platform ledger directly.
2. **Transfer wallet** — funds move between platform and provider wallets.
3. **Provider-held balance** — the provider maintains an independent balance synchronized through platform operations.

Identify:

- player/account mapping;
- transfer order identity;
- debit/credit ordering;
- success authority;
- retry and duplicate handling;
- rollback/reversal;
- currency and precision conversion;
- reconciliation after timeout or disagreement.

A client display discrepancy is weaker than a ledger or provider/platform state mismatch.

## Reason about amount and precision

Keep these hypotheses separate:

- major units versus minor units;
- decimal versus integer storage;
- display rounding versus ledger precision;
- fiat versus virtual currency;
- positive/negative adjustment conventions;
- fee included versus fee added;
- exchange-rate snapshot versus current rate;
- tenant/provider-specific precision.

Use boundary values only where the current implementation and test scope justify them. Compare the submitted representation, server-normalized representation, channel representation and final ledger representation.

## Analyze idempotency and race conditions conceptually

Identify the intended uniqueness and serialization boundary:

- business order ID;
- provider event ID;
- member/action idempotency key;
- state compare-and-set or transaction boundary;
- distributed lock or queue key;
- ledger uniqueness constraint.

A concurrency hypothesis becomes a finding only after reproducible state or ledger evidence demonstrates a duplicate or inconsistent effect.

## Reconciliation is part of the security model

Ask how the platform detects and resolves:

- platform paid/channel unpaid;
- channel paid/platform pending;
- payout submitted but result unknown;
- callback and status-query disagreement;
- duplicated external orders;
- balance and ledger mismatch;
- manual correction without traceable approval.

Reconciliation reports, exports and admin actions may reveal business boundaries that front-end APIs hide.

## Calibrate money findings carefully

State separately:

- unexpected data visibility;
- ability to create an order;
- ability to change an order state;
- ability to influence amount/destination;
- durable ledger effect;
- external money movement;
- repeatability and affected scope.

This prevents a reachable payment endpoint or synthetic success response from being described as a financial impact that the evidence has not established.
