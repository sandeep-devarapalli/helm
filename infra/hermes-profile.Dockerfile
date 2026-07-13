FROM docker.io/nousresearch/hermes-agent:v2026.7.7.2@sha256:9c841866021c54c4596849f6135717e8a4d52ba510b7f52c50aef1de1a283973

COPY runtime/hermes-profile /profile
COPY infra/hermes-profile-install.sh /usr/local/bin/hermes-profile-install

ENTRYPOINT ["hermes-profile-install"]
