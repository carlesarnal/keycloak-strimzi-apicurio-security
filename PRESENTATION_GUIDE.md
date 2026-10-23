# Presentation guide

One Keycloak Realm, Separate Trust Boundaries: Securing Kafka and Its Schema Registry

## 0:00 — The serializer and broker have separate permission paths

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 4:00 — A token can be valid and an operation forbidden

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 9:00 — Read-only means lookup succeeds and mutation fails

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 15:00 — Verify the broker record, not just a log message

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 21:00 — An outdated auth flag left the negative control open

Use the corresponding assertion or result record, explain what changes, and ask which boundary the observation proves.

## 26:00 — Questions and buffer

Compose integration uses Strimzi Kafka image 0.45.0/Kafka 3.9.0 and OAuth libraries, not a Strimzi operator deployment. Plaintext and an internal anonymous admin listener are deliberate lab fixtures. Tokens and real credentials are not recorded. Fixed local-lab credentials are disposable. TLS, rotation and Kubernetes routing are not established by this test.

## Commands

```sh
python3 verify.py
```

## Observed result

Real Keycloak 26.0, Registry 3.3.3 and Strimzi Kafka OAuth integration passed. Invalid token: 401. Read-only schema lookup: success. Read-only mutation: 403, accepted content unchanged, new version absent. Authorized Kafka producer observed in broker; reader got TopicAuthorizationException and its record was absent.

For 25 minutes, shorten setup and keep one trace plus the failure result. A backup recording must show a real run, not synthetic output.
