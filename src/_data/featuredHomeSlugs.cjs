const path = require("path");
const fs = require("fs");

const projectsPath = path.join(__dirname, "..", "content", "projects.json");
const projects = JSON.parse(fs.readFileSync(projectsPath, "utf8"));

module.exports = projects
  .filter((p) => p.featured_home)
  .map((p) => p.slug);