import type { APIRoute } from 'astro';
import { SITE_URL } from '../config';

export const GET: APIRoute = () => {
  const robots = `User-agent: *
Allow: /

Sitemap: ${SITE_URL}/sitemap.xml
`;
  return new Response(robots, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
};
