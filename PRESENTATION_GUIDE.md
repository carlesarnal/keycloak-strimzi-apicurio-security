# Presentation guide

One Keycloak Realm, Separate Trust Boundaries: Securing Kafka and Its Schema Registry

## 0:00 — The serializer and broker have separate permission paths

Registry evaluates schema lookup and publication permissions. Kafka evaluates topic operations. Sharing a Keycloak realm does not merge their audiences, roles or ACLs.

Compare the Registry OIDC settings in compose.yaml with the Kafka principal mapping in server.properties.

## 4:00 — A token can be valid and an operation forbidden

An invalid Registry token returns 401. A valid reader token can fetch content, but publishing a version returns 403. Authentication and authorization are separate decisions.

Use the successful lookup as the control before showing the denied mutation in verify.py.

## 9:00 — Read-only means lookup succeeds and mutation fails

After the denied publication, version 1 still contains its original schema and version 2 returns 404. The test checks resource state as well as HTTP status.

Point to the before/after content comparison and the absent-version assertion.

## 15:00 — Verify the broker record, not just a log message

The authorized publisher's record is present. The reader receives TopicAuthorizationException, and its record is absent. A console producer's process exit is not a sufficient delivery assertion.

Show the topic read and the exact list of observed records in verify.py.

## 21:00 — An outdated auth flag left the negative control open

In the tested Registry 3.3.3 setup, the old auth setting left an invalid-token request returning 200. Enabling QUARKUS_OIDC_TENANT_ENABLED changed that result to 401.

Keep the finding scoped to this configuration and release. The positive request alone would not have caught it.

## 26:00 — Questions and buffer

Compose integration uses Strimzi Kafka image 0.45.0/Kafka 3.9.0 and OAuth libraries, not a Strimzi operator deployment. Plaintext and an internal anonymous admin listener are deliberate lab fixtures. Tokens and real credentials are not recorded. Fixed local-lab credentials are disposable. TLS, rotation and Kubernetes routing are not established by this test.

## Commands

```sh
python3 verify.py
```

## Observed result

Real Keycloak 26.0, Registry 3.3.3 and Strimzi Kafka OAuth integration passed. Invalid token: 401. Read-only schema lookup: success. Read-only mutation: 403, accepted content unchanged, new version absent. Authorized Kafka producer observed in broker; reader got TopicAuthorizationException and its record was absent.

For 25 minutes, shorten setup and keep one trace plus the failure result. A backup recording must show a real run, not synthetic output.
