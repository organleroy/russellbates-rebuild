const path = require("path");
const fs = require("fs");

const projectsPath = path.join(__dirname, "..", "content", "projects.json");
const rawProjects = JSON.parse(fs.readFileSync(projectsPath, "utf8"));

function parseBrandSpot(title) {
  if (!title || typeof title !== "string") return { brand: "", spot: "" };

  const firstQuote = title.indexOf('"');
  if (firstQuote !== -1) {
    const brand = title.slice(0, firstQuote).trim();
    const rest = title.slice(firstQuote + 1);
    const lastQuote = rest.lastIndexOf('"');
    const spot = (lastQuote !== -1 ? rest.slice(0, lastQuote) : rest).trim();
    return { brand, spot };
  }

  const parts = title.trim().split(/\s+/);
  const brand = parts[0] || "";
  const spot = title.slice(brand.length).trim();
  return { brand, spot };
}

const projects = rawProjects.map((p) => {
  const { brand, spot } = parseBrandSpot(p.title);
  return { ...p, brand, spot };
});

module.exports = Object.fromEntries(projects.map((p) => [p.slug, p]));