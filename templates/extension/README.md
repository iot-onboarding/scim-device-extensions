<!--
Copyright 2026 Cisco Systems, Inc. and its affiliates
SPDX-License-Identifier: Apache-2.0
-->

# Example credential extension — authoring template

**Illustrative, unregistered extension.** After copying this bundle, replace the
example names, URI, descriptions, and values with your proposal. Complete the
protocol behavior and security considerations below. See
[CONTRIBUTING.md](../../CONTRIBUTING.md) for the contribution process.

## Schema registration template

This section supplies the registration fields from
[RFC 7643, Section 10.3.2](https://www.rfc-editor.org/rfc/rfc7643.html#section-10.3.2).

**Schema URI:**
`urn:ietf:params:scim:schemas:extension:exampleCredential:2.0:Device`

**Schema Name:** Example Credential Device Extension.

**Intended or Associated Resource Type:** Device.

**Purpose:** Supply an opaque credential during Device provisioning. This
example demonstrates SCIM attribute representation; replace it with the actual
extension's purpose and intended use.

### Single-value Attributes

| Attribute | Type | Multi-valued | Required | Case exact | Mutability | Returned | Uniqueness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `exampleCredential` | `binary` | false | true | true | `writeOnly` | `never` | `none` |

`exampleCredential` is an opaque synthetic credential encoded as Base64.
Padding may be omitted as allowed by SCIM. Its encoded value is case exact,
can be updated, is never returned, and has no uniqueness requirement. This
illustration defines no cryptographic mechanism or decoded-length requirement.

Describe every single-valued attribute here, including the subattributes of
complex attributes. Include its meaning, encoding, allowed values, and SCIM
characteristics; document reference types and canonical values where applicable.

### Multi-valued Attributes

None in this illustration. For a proposal with multi-valued attributes, list
and describe each attribute and its subattributes with the same detail as above.
Specify any limits, ordering, or rules for selecting a primary value.

## Dependencies and protocol behavior

This extension applies to the Device resource from
[RFC 9944](https://www.rfc-editor.org/rfc/rfc9944.html), using the attribute
characteristics and representations defined in
[RFC 7643](https://www.rfc-editor.org/rfc/rfc7643.html). Add references to the
device protocol and supported versions for a real proposal.

The extension is optional for a Device. When supplied on creation,
`exampleCredential` is required. Absence conveys no credential in this example.

For your proposal, define behavior when the extension or its attributes are
absent, how updates and removal work, and interactions with other extensions.
Document constraints beyond the SCIM Schema resource, such as decoded binary
lengths, byte order, checksums, and relationships between attributes. Identify
which component validates these constraints and how failures are reported.
Describe default behavior and any compatibility requirements.

## Schema and examples

- [SCIM Schema resource](scim-schema.json), for `/Schemas` discovery.
- [Create request](examples/create-request.json), an illustrative `POST /Devices`
  body using synthetic bytes `00` through `0f`.
- [Resource response](examples/resource-response.json), an illustrative creation
  response with server-assigned identifiers and metadata.

The response includes the extension URI but omits its credential attribute
because it is never returned. Keep the URI, attribute definitions, and behavior
consistent across this specification, the schema, and the examples. Add labeled
examples for other operations needed to explain the proposal.

## Security considerations

For a credential extension, specify authorization, protection in transit and
at rest, credential lifetime and rotation, and handling by downstream
provisioning components. Define how credentials are excluded from logs and SCIM
responses. Assess risks from any default credentials or fallback behavior.

For other extensions, describe the security and privacy implications of the
attributes and their use. Use synthetic values in all public examples.

## IANA considerations

Request registration in the
[SCIM Server-Related Schema URIs registry](https://www.iana.org/assignments/scim),
following [RFC 9944, Section 9.2](https://www.rfc-editor.org/rfc/rfc9944.html#section-9.2)
and [RFC 7643, Section 10.3](https://www.rfc-editor.org/rfc/rfc7643.html#section-10.3).
The entry below is illustrative; replace it for your proposal.

| Schema URI | Name | Resource Type | Reference |
| --- | --- | --- | --- |
| `urn:ietf:params:scim:schemas:extension:exampleCredential:2.0:Device` | Example Credential Device Extension | Device | This document, [Schema registration template](#schema-registration-template) |

### Status

- Status: `proposed` (illustrative).
