<!--
Copyright 2026 Cisco Systems, Inc. and its affiliates
SPDX-License-Identifier: Apache-2.0
-->

# Contributing

Contributions are welcome. Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
and use [SECURITY.md](SECURITY.md) to report security concerns.

## Issues

For a new extension, open an issue describing the use case, proposed Device
attributes, protocol references, and relationship to existing specifications.

For a defect, include the affected file or revision, expected and observed
behavior, and reproduction steps with synthetic input.

## Add a new extension

Choose a descriptive lowercase kebab-case name and copy the template from the
repository root:

```sh
cp -R templates/extension extensions/your-extension
```

1. Complete the extension README with its purpose, dependencies, attribute
   definitions, operation semantics, implementation constraints, and security
   considerations. Complete its IANA considerations with the registration
   fields, status `proposed`, and specification reference.
2. Update `scim-schema.json` with the extension URI and explicit attribute
   metadata, following the [validation schema](scripts/scim-schema-resource.schema.json).
3. Provide labeled examples using synthetic values and public example domains.
4. Add the extension to the [main README's index](README.md#extension-index).

## Pull requests

Keep each PR focused. Link the issue and relevant public specifications,
describe the resulting behavior, and include validation results. Update the
extension README, schema, and examples together.

Request review from the designated experts listed in the
[IANA SCIM registry](https://www.iana.org/assignments/scim). Resolve their
feedback and record approval of the final revision in the PR. Maintainers merge
new extensions after expert approval and passing CI. Changes to the reviewed
semantics require renewed expert review.

## IANA registration

After merge, the contributor or maintainer sends the completed registration
template to **scim@ietf.org** and **iana@iana.org**, following
[RFC 7643, Section 10.3](https://www.rfc-editor.org/rfc/rfc7643.html#section-10.3).

Include a public permalink to the merged extension README and its expert-review
PR and approval. Track review and registration progress in GitHub issues and PRs.
Keep status `proposed` while registration is pending.

Once the IANA entry is confirmed, verify its URI, name, and reference, and update
the extension README and main README index to `registered` in a PR.
