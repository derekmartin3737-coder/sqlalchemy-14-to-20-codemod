const { LegacyESLint, Linter } = require("eslint/use-at-your-own-risk");

async function lint() {
  const eslint = new LegacyESLint();
  const linter = new Linter({ configType: "eslintrc" });
  return { eslint, linter };
}

module.exports = { lint };
