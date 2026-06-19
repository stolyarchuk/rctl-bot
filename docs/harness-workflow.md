# Agent Workflow Harness

## Think Before Changing

- State material assumptions. Ask when uncertainty would change the result.
- Surface plausible interpretations and tradeoffs instead of choosing silently.
- Point out a simpler approach when one exists.
- For multi-step work, define a short plan with a concrete verification step
  for each outcome.

## Keep It Simple

- Implement only what was requested.
- Avoid speculative features, one-use abstractions, and unrequested
  configurability.
- Do not add handling for impossible scenarios.
- If the solution is substantially larger than necessary, simplify it.

## Make Surgical Changes

- Do not refactor, reformat, or clean up adjacent code without a task-related
  reason.
- Preserve established conventions even when another style is preferable.
- Every changed line should trace directly to the requested outcome.

## Execute Toward Verifiable Goals

- Convert requested behavior into observable success criteria.
- For bugs, reproduce the failure before changing the implementation when
  practical.
- For behavior changes, add or update tests before or alongside implementation.
- Run the narrowest relevant checks first, then the repository-level checks
  appropriate to the change.
- Report the exact verification commands and any remaining limitations.
