<!--
Copyright 2026 Cisco Systems, Inc. and its affiliates
SPDX-License-Identifier: Apache-2.0
-->

# SCIM device extensions

This repository hosts specifications, SCIM Schema resources, examples, and
IANA registration information for **new SCIM device extensions**. Contributors
and implementers can use it to develop proposals and provide a public reference
for IANA registrations.

The data model follows [RFC 7643](https://www.rfc-editor.org/rfc/rfc7643.html)
and the Device resource defined by
[RFC 9944](https://www.rfc-editor.org/rfc/rfc9944.html).
This repository does not reproduce existing RFC registrations; their RFCs
remain their authoritative specifications.

## Find or propose an extension

Each extension has its own directory under `extensions/` containing:

- `README.md`: the public specification, implementation guidance, and IANA
  registration template, status, and specification references.
- `scim-schema.json`: a SCIM `/Schemas` resource describing its attributes.
- `examples/`: synthetic, operation-specific device examples.

Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the
[extension template](templates/extension/README.md). The template is
illustrative and is not a registration proposal.

## Extension index

This index lists new registration proposals hosted in this repository.

| Extension specification | Schema URI | Status |
| --- | --- | --- |
| [Zigbee Install Code](extensions/zigbee-install-code/README.md) | `urn:ietf:params:scim:schemas:extension:zigbeeInstallCode:2.0:Device` | `proposed` |
| [Zigbee Link Key](extensions/zigbee-link-key/README.md) | `urn:ietf:params:scim:schemas:extension:zigbeeLinkKey:2.0:Device` | `proposed` |

- `proposed`: awaiting IANA registration, including proposals reviewed and merged
  while IANA registration is pending.
- `registered`: confirmed in the live IANA registry.

Designated experts review new extension pull requests before merge. After
merge, the registration request can be sent to IANA using the merged
specification as the public reference. The status remains `proposed` until
IANA confirms registration. See the
[registration process](CONTRIBUTING.md#iana-registration).

## How do I contribute?

All are welcome, under the condition that no intellectual property limitations are introduced.
The LICENSE in this distribution applies. Please also see CONTRIBUTING.md.
