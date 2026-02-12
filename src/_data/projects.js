const fs = require("fs");
const path = require("path");

module.exports = () => {
  const p = path.join(__dirname, "..", "content", "projects.json");
  const raw = fs.readFileSync(p, "utf-8");
  return JSON.parse(raw);
};