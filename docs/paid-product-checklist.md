# Paid Product Checklist

Use this before publishing, repricing, or updating any paid pack.

The pack does not clear launch unless every required item below is true.

## 1. Boss-Approval Gate

- The product solves one narrow, expensive problem.
- The landing page explains the exact supported scope in one short paragraph.
- The landing page also says who should not buy it.
- A free scanner or preview path exists before purchase.
- There is at least one before/after demo with a machine-generated report.
- There is public proof on real repos, not only synthetic fixtures.
- The product saves enough engineering time that the listed price is cheaper
  than doing the same work manually.
- The buyer gets a versioned ZIP, install guide, limitations, and rollout
  checklist.
- The product does not require a hosted API, a Codex account, or human service
  work to get the advertised value.

## 2. Scope And Claim Gate

- Product name matches what the pack actually does.
- Product description says "supported subset" or equivalent narrow wording.
- Public copy does not promise full migration automation.
- Public copy does not promise guaranteed passing behavior.
- Unsupported cases are reported, not guessed through.
- Refund policy is based on published-scope mismatch, not vague satisfaction.

## 3. Leak-Prevention Gate

- Public GitHub repo contains only the free scanner, proof material, and docs.
- Paid apply engines are not tracked in the public repo.
- Paid ZIPs are built from private source folders, not from the public tree.
- Paid ZIPs are not attached to public GitHub releases.
- Paid ZIPs are not linked from public Pages, Cloudflare assets, or raw GitHub
  URLs.
- `git status` is clean before building the paid ZIP so stale files are not
  accidentally included.
- The version number inside the ZIP matches the product page.
- The ZIP includes install docs and manager docs, not only source code.
- The ZIP is smoke-tested after packaging.

## 4. Commerce Gate

- Lemon product type is allowed under Lemon policy.
- Lemon tax category matches the actual product.
- Product file uploaded to Lemon is the private ZIP, not a public artifact.
- Checkout button points to the correct hosted checkout URL.
- Confirmation and receipt buttons point to public guidance, not public code.
- Success and cancel pages work.
- Product price is consistent across site copy, Lemon, and docs.

## 5. Verification Gate

- The free scanner passes lint, typecheck, tests, and build checks.
- The private commercial pack passes its own tests and build smoke check.
- The packaged ZIP is extracted once and tested from the staged bundle.
- A sample paid-buyer flow is tested end to end before public launch.

## 6. Compliance Gate

- Seller identity is resolved and matches the launch plan.
- Product copy follows the current claims-and-safeguards doc.
- Terms, refund policy, privacy policy, and license terms are published.
- Dependencies used in the paid ZIP have licenses compatible with resale.
- There is no secret, token, or local path leak in the public repo or paid ZIP.
- The product name does not obviously collide with someone else's trademark.

## Launch Stop Conditions

Do not publish or update a paid pack if any of these are true:

- the paid ZIP came from the public repo
- the product page overclaims beyond the tested subset
- the staged ZIP has not been smoke-tested
- the free scanner and paid pack are materially inconsistent
- the buyer cannot tell what is free versus what is paid
