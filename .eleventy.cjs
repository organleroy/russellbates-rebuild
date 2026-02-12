module.exports = function (eleventyConfig) {
  // Copy static assets through to _site
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });

  // Dev server port
  eleventyConfig.setServerOptions({ port: 8080 });

  // Nunjucks date filter used by base.njk
  eleventyConfig.addFilter("date", (value, format = "YYYY") => {
    const d = value ? new Date(value) : new Date();
    if (format === "YYYY") return String(d.getFullYear());
    // fallback: ISO date
    return d.toISOString().slice(0, 10);
  });

  return {
    pathPrefix: process.env.PATH_PREFIX || "/",
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
    },
  };
};