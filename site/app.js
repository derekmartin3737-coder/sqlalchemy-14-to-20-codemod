(function () {
  const config = window.SA20_SITE_CONFIG || {};
  const placeholderPattern =
    /REPLACE_|YOUR_|example\.com|CHANGE_ME|PUBLIC_REPO_URL/;

  function isPlaceholder(value) {
    return !value || placeholderPattern.test(value);
  }

  function setHref(selector, value, fallbackText) {
    document.querySelectorAll(selector).forEach((element) => {
      if (!(element instanceof HTMLAnchorElement)) {
        return;
      }

      if (isPlaceholder(value)) {
        element.href = "#";
        element.classList.add("disabled");
        if (fallbackText) {
          element.textContent = fallbackText;
        }
        return;
      }

      const currentHref = element.getAttribute("href") || "";
      if (value.startsWith("/go/") && currentHref.startsWith(`${value}/`)) {
        element.href = currentHref;
        return;
      }

      element.href = value;
    });
  }

  function blobUrl(path) {
    if (isPlaceholder(config.repoUrl)) {
      return "#";
    }

    const trimmed = config.repoUrl.replace(/\/$/, "");
    return `${trimmed}/blob/main/${path}`;
  }

  function applyDocLinks() {
    document.querySelectorAll("[data-doc-path]").forEach((element) => {
      if (!(element instanceof HTMLAnchorElement)) {
        return;
      }

      const docPath = element.getAttribute("data-doc-path");
      if (!docPath) {
        return;
      }

      const target = blobUrl(docPath);
      if (target === "#") {
        element.href = "#";
        element.classList.add("disabled");
      } else {
        element.href = target;
      }
    });
  }

  function applyText(selector, value, fallback) {
    document.querySelectorAll(selector).forEach((element) => {
      element.textContent = isPlaceholder(value) ? fallback : value;
    });
  }

  function applyContactLinks() {
    document.querySelectorAll("[data-contact-link]").forEach((element) => {
      if (!(element instanceof HTMLAnchorElement)) {
        return;
      }

      if (isPlaceholder(config.contactEmail)) {
        element.href = "#";
        element.classList.add("disabled");
      } else {
        element.href = `mailto:${config.contactEmail}`;
      }
    });
  }

  function showWarning(missingKeys) {
    const warning = document.getElementById("launch-warning");
    if (!warning || missingKeys.length === 0) {
      return;
    }

    warning.style.display = "block";
    warning.innerHTML =
      `<strong>Site configuration is incomplete.</strong> Update <code>site/config.js</code> for these required public values: ` +
      missingKeys.join(", ");
  }

  function loadCloudflareAnalytics() {
    if (isPlaceholder(config.cloudflareAnalyticsToken)) {
      return;
    }

    const script = document.createElement("script");
    script.src = "https://static.cloudflareinsights.com/beacon.min.js";
    script.defer = true;
    script.setAttribute(
      "data-cf-beacon",
      JSON.stringify({ token: config.cloudflareAnalyticsToken }),
    );
    document.head.appendChild(script);
  }

  const freeStartUrl = isPlaceholder(config.freeStartUrl)
    ? blobUrl("docs/quickstart.md")
    : config.freeStartUrl;

  const missing = [];
  ["sellerName", "contactEmail", "repoUrl"].forEach((key) => {
    if (isPlaceholder(config[key])) {
      missing.push(key);
    }
  });

  setHref("[data-repo-link]", config.repoUrl, "Add public repo URL");
  setHref("[data-free-link]", freeStartUrl, "Add repo or quickstart URL");
  setHref("[data-pack-link]", config.paidPackUrl, "Checkout coming soon");
  setHref(
    "[data-bundle-link]",
    config.presetBundleUrl,
    "Preset bundle coming soon",
  );
  setHref(
    "[data-pydantic-link]",
    config.pydanticPackUrl,
    "Pydantic pack coming soon",
  );

  applyText("[data-seller-name]", config.sellerName, "the seller");
  applyText("[data-contact-email]", config.contactEmail, "contact email");
  applyDocLinks();
  applyContactLinks();
  showWarning(missing);
  loadCloudflareAnalytics();
})();
