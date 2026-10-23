# Evidence and claim boundaries

Authorization matrix prepared. Kubernetes API unavailable; no fresh token/ACL/registry-denial integration run. Existing manifests are unverified scaffolding, not a production security recipe.

## Follow both connections

A Kafka producer using a Registry-aware serializer makes at least two kinds of request: it talks to the broker and resolves schema material from Registry. Those requests have different audiences, permissions and failure modes. One Keycloak realm can simplify identity administration without making every token valid for every resource.

## Build a denial matrix

Use three cases: an invalid token, a valid identity lacking Kafka WRITE permission, and a valid read-only identity attempting a Registry mutation. Pair each with a successful control so a broken network or unavailable service cannot masquerade as authorization enforcement. For the denied mutation, inspect the artifact afterward to establish that content was unchanged.

## Inspect the enforcing component

Record issuer and audience expectations, mapped principal, operation and denial details; never publish live tokens. Registry role mapping is not the same thing as a Kafka ACL. Expiry and signing-key refresh add operational concerns, while TLS protects transport rather than replacing authorization decisions.

## Current verification boundary

The repository contains historical Kubernetes scaffolding and the new diagnostic matrix. Its service accounts, actual ACL commands and Registry permission mapping still require end-to-end verification. The local cluster was unavailable in this preparation run. This draft therefore explains a testing method and does not advertise a verified zero-trust deployment.
