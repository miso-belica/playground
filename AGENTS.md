Use extreme concision in all interactions and commits - sacrifice grammar for brevity.

For interaction with Github, use gh CLI.

## Code navigation and refactoring
- You are operating in an environment where ast-grep CLI is installed.
- For any code search and/or replace that requires understanding of syntax or code structure, you should default to using "ast-grep --lang=ts -p '<pattern>'".
- You can use skill to learn about advanced patterns.
- Avoid using text-only search tools unless a plain-text search is explicitly requested.

## Commit flow
- Commit only when EXPLICITLY instructed.
- NEVER push anything to upstream/origin server even if explicitly instructed.
- When planning multiple steps always plan steps as commits.
- Make the smallest atomic commits - single test + minimal code to satisfy the test + documentation in the commit message.
- Never continue with further steps without asking user for review and previous steps are commited.

## Testing rules
- Practice red/green TDD when appropriate.
- Refactoring/cleanup/... changes do not always need a new test if the tests already exist. But a new feature or a fix always needs the test to reproduce the bug or the feature first and only after it fails implement the code.
- Check tdd skill for further details.
