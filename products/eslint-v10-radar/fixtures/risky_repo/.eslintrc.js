module.exports = {
  extends: ["eslint:recommended"],
  rules: process.env.CI ? { "no-console": "error" } : {}
};
