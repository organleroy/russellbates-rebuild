module.exports = function (eleventyConfig) {
  // Copy static assets through to _site
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });

  // Dev server port
  eleventyConfig.setServerOptions({ port: 8080 });

  return {
    pathPrefix: process.env.PATH_PREFIX || "/",
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
    },
  };
};