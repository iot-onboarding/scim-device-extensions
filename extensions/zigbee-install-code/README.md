<!--
Copyright 2026 Cisco Systems, Inc. and its affiliates
SPDX-License-Identifier: Apache-2.0
-->

# Zigbee Install Code extension

## Schema registration template

Registration fields follow
[RFC 7643, Section 10.3.2](https://www.rfc-editor.org/rfc/rfc7643.html#section-10.3.2).

**Schema URI:**
`urn:ietf:params:scim:schemas:extension:zigbeeInstallCode:2.0:Device`

**Schema Name:** Zigbee Install Code.

**Intended or Associated Resource Type:** Device.

**Purpose:** Provision a Zigbee installation code so that the receiver can
validate it and derive the device-specific link key used for joining a network.

### Single-value Attributes

| Attribute | Type | Multi-valued | Required | Case exact | Mutability | Returned | Uniqueness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `installCode` | `binary` | false | true | true | `writeOnly` | `never` | `none` |

`installCode` is the installation code followed by its 16-bit CRC in
least-significant-byte-first order. Its SCIM JSON value is Base64 encoded;
padding may be omitted as allowed by SCIM. Supported decoded lengths are 8,
10, 14, or 18 octets: a 6-, 8-, 12-, or 16-octet code followed by the 2-octet CRC.
Zigbee 3.0 uses the 18-octet form; shorter forms are for supported legacy devices.

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

The extension is optional for a Device. On creation, supply `installCode`
together with the Zigbee device information. Before provisioning a credential,
the service provider must check the Base64 representation and the decoded length
against the supported Zigbee version. In this provisioning model, the Zigbee
trust center validates the CRC and derives the link key; implementations may
delegate those steps to a trusted provisioning component before delivering the
key to the trust center. The SCIM Schema resource cannot express the decoded
length or CRC checks.

### Updates and validation failures

An authorized update can replace `installCode` for future provisioning. This
operation does not itself rotate keys on a device already joined to a network.
Omitting the attribute from a PATCH leaves it unchanged. Removing the whole
extension or deleting the resource must also remove the provisioning credential from
downstream components, subject to deployment policy. A secret omitted from a
response does not indicate that the stored credential was removed.

Reject missing required values, malformed encodings, unsupported lengths,
invalid CRCs, or incompatible device information with HTTP 400 and SCIM
`scimType` `invalidValue`, following
[RFC 7644, Section 3.12](https://www.rfc-editor.org/rfc/rfc7644.html#section-3.12).
Error details must not disclose the installation code or derived key.

### Alternative credentials and default behavior

Use this extension when the receiver needs to derive a link key. Use the
[Zigbee Link Key extension](../zigbee-link-key/README.md) when the key is already
available. Supply only one of these credential extensions for a Device;
reject requests that result in both being present with `invalidValue`.
Switching between them requires removing the previous credential extension
in the same update.

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

The request uses the public installation-code example
`83FED3407A939723A5C639B26916D505C3B5` encoded as `g/7TQHqTlyOlxjmyaRbVBcO1`.
Its final bytes `C3B5` contain the little-endian CRC `0xB5C3`. The device identity
is synthetic. The response retains the extension URI in `schemas` and shows
an empty extension object. It omits `installCode` because the attribute is
`writeOnly` and `returned: never`. The empty object makes the extension visible
in this example; it does not mean the stored credential is absent.

## Security considerations

Treat installation codes and derived link keys as sensitive credentials.
Authorize creation, replacement, removal, and downstream provisioning for the
specific device. Protect values in transit with TLS and restrict access to
stored credentials, backups, and the trust center. Exclude them from responses,
logs, telemetry, and error messages.

Validate the CRC before deriving a key; the CRC detects transcription errors
and does not authenticate the sender. Bind the resulting key to the intended
device EUI-64. Limit retention to the provisioning need, revoke credentials
when devices are removed, and use the Zigbee mechanism appropriate to the
deployment for subsequent key rotation.

The default global key provides weaker protection because it is public;
deployments should prefer device-specific credentials. The public example
installation code must not be used to provision a deployed device.

## IANA considerations

Request registration in the
[SCIM Server-Related Schema URIs registry](https://www.iana.org/assignments/scim),
following [RFC 9944, Section 9.2](https://www.rfc-editor.org/rfc/rfc9944.html#section-9.2)
and [RFC 7643, Section 10.3](https://www.rfc-editor.org/rfc/rfc7643.html#section-10.3).

| Schema URI | Name | Resource Type | Reference |
| --- | --- | --- | --- |
| `urn:ietf:params:scim:schemas:extension:zigbeeInstallCode:2.0:Device` | Zigbee Install Code | Device | This document, [Schema registration template](#schema-registration-template) |

### Status

- Status: `proposed`.
