# Architecture
 
RedRing scans a technology stack, collects evidence, and reports what's wrong — optionally with an AI-generated explanation.
 
## Flow
 
```mermaid
flowchart TB
    A[REDRING] --> B[CLI - Typer]
    A --> C[Desktop - Flet]
    A --> D[Future API/Web]
 
    B --> E[User chooses a technology stack]
    C --> E
    D --> E
 
    E --> F["Engine.run('python')"]
    F --> G["ScannerRegistry.get_by_prefix('python')"]
    G --> H[Returns all registered Python scanners]
 
    H --> I[python.version]
    H --> J[python.path]
    H --> K[pip.version]
 
    I --> L[Returns ScanResult]
    J --> M[Returns ScanResult]
    K --> N[Returns ScanResult]
 
    L --> O[Engine collects every ScanResult]
    M --> O
    N --> O
 
    O --> P["list[ScanResult] returned to caller"]
    P --> Q[AI Explanation Layer]
 
    Q --> R[Read all scanner data]
    Q --> S[Find relationships]
    Q --> T[Explain in simple English]
 
    R --> U[AI returns DiagnosisReport]
    S --> U
    T --> U
 
    U --> V[Human explanation]
    U --> W[Suggestions]
    U --> X[Confidence level]
 
    V --> Y[Renderer - depends on UI]
    W --> Y
    X --> Y
 
    Y --> Z1[CLI Renderer]
    Y --> Z2[Desktop Renderer]
    Y --> Z3[JSON Renderer]
 
    Z1 --> AA1[Pretty terminal]
    Z2 --> AA2[Flet widgets]
    Z3 --> AA3[API / Export]
 
    AA1 --> AB[User sees report]
    AA2 --> AB
    AA3 --> AB
```
 
## Components
 
- **Scanners** — collect evidence for one capability (e.g. `python.version`). Pure data collection, no side effects. Auto-register via `ScannerRegistry`.
- **Engine** — orchestrates scanners for a given stack (`Engine.run("python")`) and collects their `ScanResult`s.
- **AI Explanation Layer** — takes all `ScanResult`s, reasons over them, and returns a `DiagnosisReport` (explanation + suggestions + confidence). Optional — core diagnostics work without it.
- **Renderers** — format the report for CLI, Desktop, or JSON/API output. Adding a new renderer doesn't touch scanners or the engine.
## Design principles
 
- Evidence-first: inspect before recommending
- Explain before fixing
- Modular: new scanners, renderers, or UIs plug in without touching existing code
- Safe by default: no automatic changes without confirmation
## Adding a scanner
 
See [CONTRIBUTING.md](CONTRIBUTING.md) for the scanner template and registration steps.
 
## Full design notes
 
For product goals, supported/planned tech stacks, and design rationale, see the [expanded architecture doc](https://redring.pages.dev/docs.html#docs-architecture) on the website.
