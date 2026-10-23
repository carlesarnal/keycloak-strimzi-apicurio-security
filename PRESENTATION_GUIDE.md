# Presentation guide

One Keycloak Realm, Separate Trust Boundaries: Securing Kafka and Its Schema Registry

## Audience and central claim

A Kafka producer using a Registry-aware serializer makes at least two kinds of request: it talks to the broker and resolves schema material from Registry. Those requests have different audiences, permissions and failure modes. One Keycloak realm can simplify identity administration without making every token valid for every resource.

## 30-minute run of show

### 0:00 — One identity provider, separate decisions

Say: A Kafka producer using a Registry-aware serializer makes at least two kinds of request: it talks to the broker and resolves schema material from Registry. Those requests have different audiences, permissions and failure modes. One Keycloak realm can simplify identity administration without making every token valid for every resource.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 4:00 — Serializer lookup versus broker produce

Say: Use three cases: an invalid token, a valid identity lacking Kafka WRITE permission, and a valid read-only identity attempting a Registry mutation. Pair each with a successful control so a broken network or unavailable service cannot masquerade as authorization enforcement. For the denied mutation, inspect the artifact afterward to establish that content was unchanged.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 9:00 — Invalid token

Say: Record issuer and audience expectations, mapped principal, operation and denial details; never publish live tokens. Registry role mapping is not the same thing as a Kafka ACL. Expiry and signing-key refresh add operational concerns, while TLS protects transport rather than replacing authorization decisions.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 15:00 — Valid identity, denied operation

Say: The repository contains historical Kubernetes scaffolding and the new diagnostic matrix. Its service accounts, actual ACL commands and Registry permission mapping still require end-to-end verification. The local cluster was unavailable in this preparation run. This draft therefore explains a testing method and does not advertise a verified zero-trust deployment.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 21:00 — Successful controls and unchanged state

Say: Use the evidence boundary to choose the next action.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 26:00 — Questions and buffer

Ask what the demonstration establishes and what it leaves open. Do not add another feature if time is short.

## Setup and fallback

```sh
Review talk/authorization-matrix.md; cluster tests remain pending
```

Authorization matrix prepared. Kubernetes API unavailable; no fresh token/ACL/registry-denial integration run. Existing manifests are unverified scaffolding, not a production security recipe.

Prebuild/download dependencies. Keep a recording of an actual successful run; if unavailable, use the documented walkthrough and say it is not live execution. Never substitute fabricated success output.

## Questions to prepare

- What is the simplest alternative?
- Which failure was actually exercised?
- Which guarantee belongs to the application rather than the infrastructure?
- Which result changes with versions or workload?

## 25-minute adaptation

Use one central trace, shorten setup and reserve three minutes for questions. Move the secondary implementation example to backup.
