# Verify the identity boundary, not just token acquisition

| Request | Credential condition | Required observation | Positive control |
|---|---|---|---|
| Registry lookup | Invalid signature/issuer/audience | Rejected before resource access | Valid token for this registry |
| Kafka produce | Valid principal, no WRITE ACL | Authorization denial | Same producer with intended topic grant |
| Registry mutation | Valid identity with read-only role | Mutation denied; content unchanged | Authorized publisher, same artifact |

Record token issuer/audience (never the token), mapped principal, operation,
enforcing component, server error and the successful control. A token from the
same realm is not necessarily intended for both resources.

## Current implementation gaps

The existing Kubernetes manifests and scripts are scaffolding. The local cluster
was unavailable when preparing this package. None of these three end-to-end
denial cases is marked passed. Verify service-account configuration, Strimzi
version/API, role mapping, real ACL creation and TLS before claiming a complete lab.

## Rehearsal acceptance

One denied request is not enough: show that the service is otherwise reachable,
the intended identity succeeds, and the denied mutation changed no artifact.
Use unique test resources and remove only those resources after the exercise.
