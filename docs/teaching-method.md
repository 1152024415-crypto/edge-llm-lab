# Teaching Method

This project is a learning lab, not just a benchmark repo. Every experiment should teach the deployment mechanism behind the result.

## Learning Loop

For each phase, record four layers:

1. What we ran: command, model, runtime, backend, precision, prompt, and result path.
2. What the framework did: runtime APIs called, model transformations, plugin selection, fallback, cache behavior, or graph compilation.
3. What the system did: OS devices, drivers, compiler/runtime libraries, memory movement, and hardware execution evidence when available.
4. How to debug it: where failures can occur and what evidence separates model, runtime, driver, operator, memory, and quality issues.

## Source Reading Rule

When a phase uses a framework feature, add a small source-reading note:

- public API entry point
- relevant runtime or plugin component
- key files or official docs to read
- what we verified locally
- what remains an inference until proven by source, logs, or profiler output

Keep source-reading notes concise. Prefer links to official docs and upstream source over long pasted excerpts.

## Explanation Standard

Each phase summary should answer:

- What did this prove?
- What did it not prove?
- Which layer produced the result: Python wrapper, OpenVINO Core, device plugin, OS driver, compiler, or hardware?
- What should we inspect next if the result is surprising?
