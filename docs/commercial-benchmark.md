# Commercial Benchmark

This is the go / no-go bar for every product in this repo.

## Core Question

Could a working engineer take this to their boss and make a credible case for
spending real budget on it right now?

If the answer is not clearly yes, the product is not commercially ready yet.

## Required Bar

- The product solves one expensive, narrow, recurring problem.
- The problem statement is legible to a non-author buyer.
- The supported scope is explicit and narrow.
- The unsupported scope is explicit and fail-closed.
- The demo shows before, command, after, and report output.
- The product works on real public repos or real public files, not only local
  fixtures.
- The product reduces real engineering time, risk, or rollout cost.
- The buyer can explain the value in one sentence:
  - "This removes X hours of migration risk/work from our repo and tells us
    exactly what is still left."
- The pricing is small relative to the engineering time it saves.
- The refund / claims / limitations language is narrow enough to be trusted.

## Evidence Needed Before Sale

- at least 3 public proof cases for the supported path
- at least 2 blocked proof cases showing correct fail-closed behavior
- one clean apply run on copied public input, not just dry-run
- one machine-generated report artifact fit for a buyer demo
- one README section called `Who This Is For`
- one README section called `Do Not Buy This If`

## Automatic No-Sale Triggers

Do not treat a product as ready for paid launch if any of these are true:

- only fixture tests exist
- the product has not touched public real-world input
- the product still crashes on normal CLI usage
- the product claims more than its tests and proof cover
- the paid layer is mostly hope, future work, or vague "edge cases"
- the main value still depends on seller labor

## Product Review Question Set

Before launch, answer all of these:

- What exact repo or file shape does this support?
- What exact repo or file shape does this refuse?
- What visible artifact proves success?
- What visible artifact proves honest failure?
- What is the sentence a buyer would say to justify budget?
- Why is this better than docs plus grep plus one engineer-day?
- What would make a careful engineering manager say no?

## Current Read on the First Three Products

- `sa20-pack`
  - Ready for a serious internal budget conversation: yes, for the supported
    subset
- `flatconfig-lift`
  - Ready for a serious internal budget conversation: yes, for static JSON and
    YAML config sources
- `pydantic-v2-porter`
  - Ready for a serious internal budget conversation: yes, for the supported
    validator, settings, and config subset

## Rule Going Forward

No future product graduates from "interesting build" to "sellable product"
until it clears this benchmark.
