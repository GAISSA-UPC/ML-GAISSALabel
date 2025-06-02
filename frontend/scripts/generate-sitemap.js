#!/usr/bin/env node

/**
 * Sitemap Generator for GAISSA Tools
 * Generates sitemap.xml for better search engine crawlability
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const DOMAIN = 'https://gaissalabel.essi.upc.edu';
const OUTPUT_PATH = path.join(__dirname, '../public/sitemap.xml');

// Define your routes and their properties
const routes = [
    {
        path: '/',
        changefreq: 'weekly',
        priority: '1.0',
        lastmod: new Date().toISOString().split('T')[0]
    },
    {
        path: '/gaissalabel',
        changefreq: 'monthly',
        priority: '0.9',
        lastmod: new Date().toISOString().split('T')[0]
    },
    {
        path: '/about',
        changefreq: 'monthly',
        priority: '0.8',
        lastmod: new Date().toISOString().split('T')[0]
    },
    {
        path: '/gaissalabel/trainingForm',
        changefreq: 'monthly',
        priority: '0.7',
        lastmod: new Date().toISOString().split('T')[0]
    },
    {
        path: '/gaissalabel/trainingPre',
        changefreq: 'monthly',
        priority: '0.7',
        lastmod: new Date().toISOString().split('T')[0]
    },
    {
        path: '/gaissalabel/inferenceForm',
        changefreq: 'monthly',
        priority: '0.7',
        lastmod: new Date().toISOString().split('T')[0]
    },
    {
        path: '/gaissalabel/inferencePre',
        changefreq: 'monthly',
        priority: '0.7',
        lastmod: new Date().toISOString().split('T')[0]
    }
];

// Generate sitemap XML
function generateSitemap() {
    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${routes.map(route => `  <url>
    <loc>${DOMAIN}${route.path}</loc>
    <lastmod>${route.lastmod}</lastmod>
    <changefreq>${route.changefreq}</changefreq>
    <priority>${route.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

    return sitemap;
}

// Write sitemap to file
function writeSitemap() {
    try {
        const sitemapContent = generateSitemap();
        fs.writeFileSync(OUTPUT_PATH, sitemapContent, 'utf8');
        console.log(`✅ Sitemap generated successfully at: ${OUTPUT_PATH}`);
        console.log(`📊 Total URLs: ${routes.length}`);
    } catch (error) {
        console.error('❌ Error generating sitemap:', error);
        process.exit(1);
    }
}

// Run the generator
writeSitemap();
