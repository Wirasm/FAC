// @ts-check
import { defineConfig } from 'astro/config';
import node from '@astrojs/node'
import clerk from '@clerk/astro'

// https://astro.build/config
export default defineConfig({
    integrations: [clerk()],
    adapter: node({ mode: 'standalone' }),
    output: 'server',
});
