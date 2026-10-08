// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

import react from '@astrojs/react';

export default defineConfig({
  site: 'https://www.amelectricals.co.in',
  trailingSlash: 'always',
  server: {
    port: process.env.PORT ? Number(process.env.PORT) : 4323,
    host: true,
  },
  build: {
    format: 'directory',
    inlineStylesheets: 'auto',
  },
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [sitemap({
    changefreq: 'weekly',
    priority: 0.7,
    lastmod: new Date(),
  }), mdx(), react()],
  prefetch: {
    prefetchAll: false,
    defaultStrategy: 'hover',
  },
});