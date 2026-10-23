# One Keycloak Realm, Separate Trust Boundaries: Securing Kafka and Its Schema Registry

Real Keycloak 26.0, Registry 3.3.3 and Strimzi Kafka OAuth integration passed. Invalid token: 401. Read-only schema lookup: success. Read-only mutation: 403, accepted content unchanged, new version absent. Authorized Kafka producer observed in broker; reader got TopicAuthorizationException and its record was absent.

## Run

```sh
python3 verify.py
```

## Evidence and boundaries

Compose integration uses Strimzi Kafka image 0.45.0/Kafka 3.9.0 and OAuth libraries, not a Strimzi operator deployment. Plaintext and an internal anonymous admin listener are deliberate lab fixtures. Tokens and real credentials are not recorded. Fixed local-lab credentials are disposable. TLS, rotation and Kubernetes routing are not established by this test.

Observed machine-readable results: [results.json](results.json).

All containers/processes created by the runner are cleaned up on normal completion and handled failures. An externally killed process may need the explicit Compose cleanup command. Use only disposable local test resources.

## Present

Open `presentation.html`; arrows/Page keys navigate and N toggles notes. Use `PRESENTATION_GUIDE.md` for timing and the actual commands.
