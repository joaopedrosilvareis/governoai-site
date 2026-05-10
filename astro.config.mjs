import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://governoai.pt',
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
});
