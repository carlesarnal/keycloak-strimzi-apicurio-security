# Evidence

Real Keycloak 26.0, Registry 3.3.3 and Strimzi Kafka OAuth integration passed. Invalid token: 401. Read-only schema lookup: success. Read-only mutation: 403, accepted content unchanged, new version absent. Authorized Kafka producer observed in broker; reader got TopicAuthorizationException and its record was absent.

Compose integration uses Strimzi Kafka image 0.45.0/Kafka 3.9.0 and OAuth libraries, not a Strimzi operator deployment. Plaintext and an internal anonymous admin listener are deliberate lab fixtures. Tokens and real credentials are not recorded. Fixed local-lab credentials are disposable. TLS, rotation and Kubernetes routing are not established by this test.

See `results.json` and the runner assertions. Results describe the fixture and versions recorded here.
