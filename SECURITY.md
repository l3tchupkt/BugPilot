# Security Policy

## Supported Versions

Currently, the following versions of BugPilot are supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.3.x   | :white_check_mark: |
| < 1.3   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in BugPilot itself, please report it privately rather than opening a public GitHub issue.

Please use the **GitHub Security Advisories** feature for this repository to submit a private vulnerability report:

**Repository → Security → Advisories → Report a vulnerability**

If GitHub Security Advisories are unavailable, open a minimal issue requesting a private security contact without publicly disclosing the vulnerability details.

### Please Include

A useful report should contain:

* A clear description of the vulnerability.
* The affected BugPilot version or commit.
* The affected component, file, or functionality.
* Steps to reproduce the issue.
* A minimal proof of concept, where applicable.
* Expected behavior and actual behavior.
* Security impact and realistic attack scenarios.
* Any relevant logs, stack traces, screenshots, or test results.
* Suggested remediation, if known.

Please avoid including API keys, credentials, personal information, or other sensitive data in reports.

## Response Process

The maintainers will make a reasonable effort to:

1. Acknowledge valid reports.
2. Reproduce and validate the reported issue.
3. Determine the security impact and affected versions.
4. Develop and test an appropriate fix.
5. Coordinate disclosure when appropriate.
6. Publish a security advisory when the issue warrants public disclosure.

Response and remediation timelines may vary depending on severity, complexity, and maintainer availability.

## Responsible Disclosure

Please allow maintainers reasonable time to investigate and address a vulnerability before publicly disclosing technical details.

Do not intentionally access, modify, destroy, or exfiltrate data that does not belong to you while validating a vulnerability.

When testing BugPilot against third-party systems, researchers are responsible for obtaining appropriate authorization and complying with the target's rules, policies, and applicable laws.

## Security Research

BugPilot is designed for authorized penetration testing, security research, and defensive security assessment.

Researchers should only use BugPilot against systems they own or have explicit permission to test.

The BugPilot maintainers are not responsible for unauthorized or unlawful use of the software.

## Scope

This policy covers vulnerabilities in the BugPilot project, including:

* BugPilot CLI and Python code.
* Built-in security tools and integrations.
* Authentication and authorization mechanisms.
* API key and credential handling.
* Local file and process handling.
* Update mechanisms.
* Docker and deployment configurations shipped with the project.
* Dependencies where the vulnerability is introduced or materially exposed by BugPilot.

Third-party vulnerabilities that are merely detected or reported by BugPilot are **not vulnerabilities in BugPilot itself** and should be reported to the respective third-party project.

## Out of Scope

The following generally do not qualify as security vulnerabilities in BugPilot:

* Vulnerabilities in unrelated third-party software.
* Issues requiring an already-compromised development environment.
* Reports based solely on outdated dependencies without demonstrating security impact to BugPilot.
* Social engineering or phishing attacks against maintainers.
* Denial-of-service caused solely by intentionally malicious user input against an intentionally exposed testing environment.
* Misuse of BugPilot against systems without authorization.
* Findings that are purely informational without a meaningful security impact.

Out-of-scope reports may still be reviewed at the maintainers' discretion.

## Safe Harbor

BugPilot maintainers will not pursue legal action against security researchers who:

* Act in good faith.
* Test only systems they own or are explicitly authorized to test.
* Avoid unnecessary access to data belonging to others.
* Avoid degrading or disrupting production systems.
* Do not use discovered vulnerabilities for malicious purposes.
* Report vulnerabilities privately and allow reasonable time for remediation.

This safe harbor applies only to activities conducted within the scope of this policy and does not grant permission to test third-party systems.

## Disclosure

After a vulnerability has been fixed, the maintainers may publish a GitHub Security Advisory containing relevant technical and remediation information.

Researchers may be credited for their discovery unless they request anonymity.

The timing and contents of public disclosure will be coordinated where reasonably possible.

## Questions

For general questions, feature requests, or non-security bugs, please use the repository's regular GitHub Issues and Discussions.

For security vulnerabilities, use the private GitHub Security Advisory reporting mechanism described above.
