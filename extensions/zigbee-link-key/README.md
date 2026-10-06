<!--
Copyright 2026 Cisco Systems, Inc. and its affiliates
SPDX-License-Identifier: Apache-2.0
-->

# Zigbee Link Key extension

## Schema registration template

Registration fields follow
[RFC 7643, Section 10.3.2](https://www.rfc-editor.org/rfc/rfc7643.html#section-10.3.2).

**Schema URI:**
`urn:ietf:params:scim:schemas:extension:zigbeeLinkKey:2.0:Device`

**Schema Name:** Zigbee Link Key.

**Intended or Associated Resource Type:** Device.

**Purpose:** Provision an already-derived or otherwise obtained 128-bit Zigbee
link key when the receiver does not need an installation code.

### Single-value Attributes

| Attribute | Type | Multi-valued | Required | Case exact | Mutability | Returned | Uniqueness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `linkKey` | `binary` | false | true | true | `writeOnly` | `never` | `none` |

`linkKey` is a Zigbee link key whose decoded value is exactly 16 octets
(128 bits). Its SCIM JSON value is Base64 encoded; padding may be omitted as
allowed by SCIM. The bytes are supplied in key order without reversal or a CRC.

The attribute is required when this extension is supplied, can be replaced,
and is never returned, including when explicitly requested. No uniqueness
constraint is imposed by the SCIM service provider.

### Multi-valued Attributes

None. This extension has no complex attributes or subattributes.

## Dependencies and protocol behavior

This extension applies to the Device resource and is used with the Zigbee
extension defined in
[RFC 9944, Section 7.5](https://www.rfc-editor.org/rfc/rfc9944.html#section-7.5).
The Zigbee extension supplies the device EUI-64 and supported versions. Attribute
characteristics and binary representation follow
[RFC 7643](https://www.rfc-editor.org/rfc/rfc7643.html).

The extension is optional for a Device. On creation, supply `linkKey` together
with the Zigbee device information. The SCIM service provider must check the
Base64 representation and the 16-octet decoded length before delivering the key
to the Zigbee trust center for the intended device. The SCIM Schema resource
cannot express this decoded-length check. This extension transports key material
and does not change the key-establishment rules of the supported Zigbee version.

### Updates and validation failures

An authorized update can replace `linkKey` for future provisioning. This
operation does not itself rotate keys on a device already joined to a network.
Omitting the attribute from a PATCH leaves it unchanged. Removing the whole
extension or deleting the resource must also remove the provisioning credential from
downstream components, subject to deployment policy. A secret omitted from a
response does not indicate that the stored credential was removed.

Reject missing required values, malformed encodings, incorrect decoded lengths,
or incompatible device information with HTTP 400 and SCIM `scimType`
`invalidValue`, following
[RFC 7644, Section 3.12](https://www.rfc-editor.org/rfc/rfc7644.html#section-3.12).
Error details must not disclose the key. A valid length alone cannot establish
that a key is correct for the device.

### Alternative credentials and default behavior

Use this extension when the link key is already available. Use the
[Zigbee Install Code extension](../zigbee-install-code/README.md) when the
receiver needs to validate a code and derive the key. Supply only one of these
credential extensions for a Device; reject requests that result in both being
present with `invalidValue`. Switching between them requires removing the
previous credential extension in the same update.

When neither extension is present, the SCIM service provider assumes that
the device accepts the Zigbee default global Trust Center link key. Its exact
16-octet ASCII value is `ZigBeeAlliance09`. This is a well-known key, not a
device-specific secret. Deployment policy may reject that provisioning mode.
Invalid supplied credentials must not trigger fallback to the default key.

## Schema and examples

- [SCIM Schema resource](scim-schema.json), for `/Schemas` discovery.
- [Create request](examples/create-request.json), a `POST /Devices` body.
- [Resource response](examples/resource-response.json), a successful creation
  response with server-assigned identifiers and metadata.

The request uses the public example key
`FA8081CAAA41D5ADE9B5658799268B88`, encoded as `+oCByqpB1a3ptWWHmSaLiA==`,
and a synthetic device identity. The response retains the extension URI in
`schemas` and shows an empty extension object. It omits `linkKey` because the
attribute is `writeOnly` and `returned: never`. The empty object makes the
extension visible in this example; it does not mean the stored key is absent.

## Security considerations

Treat link keys as sensitive credentials. Authorize creation, replacement,
removal, and downstream provisioning for the specific device. Protect values
in transit with TLS and restrict access to stored keys, backups, and the trust
center. Exclude keys from responses, logs, telemetry, and error messages.

Obtain device-specific keys through a trusted process and bind them to the
intended device EUI-64. Limit retention to the provisioning need, revoke keys
when devices are removed, and use the Zigbee mechanism appropriate to the
deployment for subsequent key rotation. Key length validation does not
authenticate the source or prove device possession.

The default global key provides weaker protection because it is public;
deployments should prefer device-specific credentials. The public example
link key must not be used to provision a deployed device.

## IANA considerations

Request registration in the
[SCIM Server-Related Schema URIs registry](https://www.iana.org/assignments/scim),
following [RFC 9944, Section 9.2](https://www.rfc-editor.org/rfc/rfc9944.html#section-9.2)
and [RFC 7643, Section 10.3](https://www.rfc-editor.org/rfc/rfc7643.html#section-10.3).

| Schema URI | Name | Resource Type | Reference |
| --- | --- | --- | --- |
| `urn:ietf:params:scim:schemas:extension:zigbeeLinkKey:2.0:Device` | Zigbee Link Key | Device | This document, [Schema registration template](#schema-registration-template) |

### Status

- Status: `proposed`.
