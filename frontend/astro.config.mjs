// @ts-check
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import clerk from '@clerk/astro';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
    integrations: [
        clerk(),
        tailwind(),
    ],
    adapter: node({ mode: 'standalone' }),
    output: 'server',
});
