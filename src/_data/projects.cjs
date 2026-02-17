/**
 * projects.cjs — normalize project data for Eleventy
 *
 * Canonical data model (in src/content/projects.json):
 *   - subtitle : descriptive line (e.g. “starring …”)
 *   - agency   : agency / production credit line
 *
 * Backward compatibility:
 *   - subhed is an alias for subtitle (older templates)
 *   - blurb  is an alias for agency   (older templates)
 *
 * IMPORTANT: Do not add new "blurb" fields to projects.json.
 * "blurb" exists only so legacy templates don’t break.
 */

const path = require("path");
const fs = require("fs");

const projectsPath = path.join(__dirname, "..", "content", "projects.json");
const rawProjects = JSON.parse(fs.readFileSync(projectsPath, "utf8"));

function parseBrandSpot(title) {
  // Expected: Brand "Spot Title" (supports straight or curly quotes)
  if (!title || typeof title !== "string") return { brand: "", spot: "" };

  const t = title.trim();

  // brand = anything up to the first quote
  // spot  = anything inside quotes
  // supports: "..." or “...”
  const m = t.match(/^(.*?)\s*["“](.*?)["”]\s*$/);
  if (m) {
    const brand = (m[1] || "").trim();
    const spot = (m[2] || "").trim();
    return { brand, spot };
  }

  // Fallback: Brand = first token; Spot = remainder
  const parts = t.split(/\s+/);
  const brand = parts[0] || "";
  const spot = t.slice(brand.length).trim();
  return { brand, spot };
}

function quoteSpot(spot) {
  const s = (spot || "").trim();
  return s ? `"${s}"` : "";
}

module.exports = rawProjects.map((p) => {
  const { brand, spot } = parseBrandSpot(p.title);

  // Canonical fields (preferred)
  const subtitle = (p.subtitle ?? "") || "";
  const agency = (p.agency ?? "") || "";

  // Backward compatibility aliases (for templates that still reference them)
  const subhed = (p.subhed ?? subtitle) || "";
  const blurb = (p.blurb ?? agency) || "";

  return {
    ...p,
    brand,
    spot,
    spotQuoted: quoteSpot(spot),

    // Ensure canonical fields are always present as strings
    subtitle,
    agency,

    // Compatibility aliases
    subhed,
    blurb,
  };
});