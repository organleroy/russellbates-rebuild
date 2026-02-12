export default function(eleventyConfig) {
  // Copy static assets through to _site
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });

  // Keep output URLs nice (/work/slug/)
  eleventyConfig.setServerOptions({ port: 8080 });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes"
    }
  };
}
