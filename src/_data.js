import projects from "./content/projects.json" assert { type: "json" };

export default {
  projects,
  // map slug -> project for fast lookups in templates
  projectBySlug: Object.fromEntries(projects.map(p => [p.slug, p])),
  featuredHomeSlugs: projects.filter(p => p.featured_home).map(p => p.slug)
};
