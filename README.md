# One Keycloak Realm, Separate Trust Boundaries: Securing Kafka and Its Schema Registry

A Kafka producer using a Registry-aware serializer makes at least two kinds of request: it talks to the broker and resolves schema material from Registry. Those requests have different audiences, permissions and failure modes. One Keycloak realm can simplify identity administration without making every token valid for every resource.

## Current talk entry point

```sh
Review talk/authorization-matrix.md; cluster tests remain pending
```

Authorization matrix prepared. Kubernetes API unavailable; no fresh token/ACL/registry-denial integration run. Existing manifests are unverified scaffolding, not a production security recipe.

Start with [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md), open `presentation.html`, and inspect [EVIDENCE.md](EVIDENCE.md) and [VERIFICATION.md](VERIFICATION.md). The prior repository overview is retained in `docs/historical-readme.md` as historical context, not a verified recipe for this talk.

The executable material and documentation distinguish observed behavior from design guidance. License: Apache-2.0.
