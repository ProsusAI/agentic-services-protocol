# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in ASP — whether in schemas, tooling, generated code, or documentation infrastructure — please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, email: **secops@prosus.com**

Include:

- A description of the vulnerability
- Steps to reproduce or a proof-of-concept
- The affected component (schemas, generated types, build tooling, docs site, etc.)
- Any potential impact you've identified

## What to expect

| Step | Timeline |
|---|---|
| Acknowledgement of your report | Within 3 business days |
| Initial assessment and severity triage | Within 7 business days |
| Fix development and review | Depends on severity |
| Public disclosure (coordinated with reporter) | After fix is released |

We will work with you to understand the issue and coordinate disclosure. We ask that you give us a reasonable window to address the vulnerability before making it public.

## Scope

This policy covers:

- JSON schemas in `source/schemas/` and `spec/schemas/`
- Generated SDK types (`generated/`)
- Build and validation tooling (`generate_schemas.py`, `validate_specs.py`, etc.)
- Documentation site and its build pipeline
- Any published packages or artifacts

## Recognition

We're happy to credit reporters in our CHANGELOG and release notes (unless you prefer to remain anonymous). Let us know your preference when you report.
