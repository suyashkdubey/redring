> [!NOTE]
> This tool is under active development and isn't usable yet.
> The stable version released will be **v1.0.0**.

# RedRing

RedRing checks your development environment and fixes what's broken.

## Problem it solves

You run `docker-compose up` and get an error. You spend 2 hours
Googling. It turns out Docker virtualization was disabled in BIOS.

RedRing finds these issues in 5 seconds and even auto fix on your demand.

## What it is

A local diagnostics tool for developer environments. Run it when a tool fails to start or install, and it reports the exact environment issue. Then you can try fixing the issue yourself or using the in-built auto fix of this tool too.

## AI-based explanations (optional)

*Diagnosis and evidence collection work **without any API key.***
For plain-English explanations, add a key from one of:

- Groq (free tier available): https://console.groq.com/keys
- OpenAI: https://platform.openai.com/api-keys
- Anthropic Claude: https://platform.claude.com/settings/keys
- Google Gemini: https://aistudio.google.com/api-keys

## Installation

```bash
pip install redring
```

## Quick start

```bash
redring diagnose <stack>
```

Example:

```bash
redring diagnose docker
```

## Real example

If Docker won't run, RedRing can show whether:

- the OS meets Docker requirements
- enough RAM is available
- virtualization support is present
- network access is available
- BIOS or kernel settings are blocking it

It gives a practical reason instead of a vague failure.

## Why it's different

- **checks the local environment**, not just command output
- **focuses on real blockers** in the system and toolchain
- **gives clear next steps** for developers
- **doesn't guess or make changes automatically** until you confirm
- **auto-fixes safely** — makes changes, backs them up, lets you rollback

*Most tools just say "Docker failed." RedRing shows why.*

## Limitations

Current limitations:

- Requires Python 3.12 and above
- only checks supported stacks (Check if your tech is supported: https://redring.pages.dev/docs#docs-supported-tech-stack)
- depends on available local scanners

## Contributing

The easiest way to contribute is by **building a new scanner** or **improving existing scanner code**. Scanners are self-contained and follow a simple pattern, so it's the fastest way to get familiar with the codebase.

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for the scanner template and setup steps.

## Documentation

To read the documentation, please visit our website: https://redring.pages.dev/docs

---

## License

MIT