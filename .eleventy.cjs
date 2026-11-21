const markdownIt = require("markdown-it");
const markdownItAnchor = require("markdown-it-anchor");

const md = markdownIt({ html: true, linkify: true, typographer: false });
md.use(markdownItAnchor, {
  permalink: markdownItAnchor.permalink.linkInsideHeader({
    symbol: "#",
    placement: "before",
  }),
  slugify: (s) =>
    s
      .trim()
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s-]/gu, "")
      .replace(/\s+/g, "-"),
});

/** @param {import("@11ty/eleventy").UserConfig} eleventyConfig */
module.exports = function (eleventyConfig) {
  eleventyConfig.setLibrary("md", md);
  return {
    dir: {
      input: "eleventy/content",
      includes: "../_includes",
      layouts: "../_includes",
      output: "_site",
      data: "../_data",
    },
    markdownTemplateEngine: "liquid",
    htmlTemplateEngine: "njk",
    templateFormats: ["md", "njk", "html"],
  };
};