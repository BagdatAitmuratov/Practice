import { eq, sql } from 'drizzle-orm';
import { db } from '../../db/index.ts';
import { playerProgress } from '../../db/schema.ts';

export const config = { path: '/api/*' };
const json = (body: unknown, status = 200) => Response.json(body, {status, headers: {'Cache-Control': 'no-store'}});

export default async function handler(request: Request) {
  const path = new URL(request.url).pathname;
  // Netlify Dev currently forwards frontend requests to Server too; production serves dist first.
  if (!path.startsWith('/api/') && process.env.NETLIFY_DEV) {
    const target = new URL(request.url); target.protocol = 'http:'; target.host = 'localhost:5173';
    return fetch(target, {headers: {accept: request.headers.get('accept') || '*/*'}});
  }
  if (path !== '/api/progress') return json({error:'Not found'},404);
  if (!['GET','PUT'].includes(request.method)) return json({error:'Method not allowed'},405);
  const origin = request.headers.get('origin');
  if (request.method === 'PUT' && origin !== new URL(request.url).origin) return json({error:'Origin not allowed'},403);
  // Identity verifies the JWT remotely. Never trust a decoded client JWT or a submitted user ID.
  const cookie = request.headers.get('cookie')?.split(';').map(c=>c.trim()).find(c=>c.startsWith('nf_jwt='));
  if (!cookie) return json({error:'Unauthorized'},401);
  let token: string;
  try { token = decodeURIComponent(cookie.slice(7)); } catch { return json({error:'Unauthorized'},401); }
  try {
    const identityOrigin = process.env.URL || 'https://bagaait.netlify.app';
    const auth = await fetch(`${identityOrigin}/.netlify/identity/user`, {headers: {Authorization:`Bearer ${token}`}, signal: AbortSignal.timeout(8000)});
    if (!auth.ok) return json({error:'Unauthorized'},401);
    const user = await auth.json();
    if (!user.id) return json({error:'Unauthorized'},401);
    if (request.method === 'GET') {
      const rows = await db.select().from(playerProgress).where(eq(playerProgress.userId,user.id));
      return json(Object.fromEntries(rows.map(row=>[row.gameId,{completed:row.completed}])));
    }
    if (Number(request.headers.get('content-length')||0)>4096) return json({error:'Payload too large'},413);
    const raw = await request.text();
    if(raw.length>4096) return json({error:'Payload too large'},413);
    let body: unknown;
    try { body=JSON.parse(raw); } catch { return json({error:'Invalid JSON'},400); }
    if (!body || typeof body !== 'object' || Array.isArray(body)) return json({error:'Invalid progress'},400);
    const entries=Object.entries(body);
    if(entries.length>9 || entries.some(([id,p])=>!/^\d$/.test(id)||+id>8||!p||typeof p!=='object'||!Number.isInteger(p.completed)||p.completed<0||p.completed>1000)) return json({error:'Invalid progress'},400);
    if(entries.length) await db.insert(playerProgress).values(entries.map(([id,p])=>({userId:user.id,gameId:+id,completed:p.completed}))).onConflictDoUpdate({
      target:[playerProgress.userId,playerProgress.gameId],
      set:{completed:sql`greatest(${playerProgress.completed}, excluded.completed)`,updatedAt:new Date()},
    });
    return json({saved:true});
  } catch { return json({error:'Progress temporarily unavailable'},503); }
}
