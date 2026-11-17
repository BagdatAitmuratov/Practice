import { pgTable, text, integer, timestamp, primaryKey } from 'drizzle-orm/pg-core';
export const playerProgress = pgTable('player_progress', {
  userId: text('user_id').notNull(),
  gameId: integer('game_id').notNull(),
  completed: integer('completed').notNull().default(0),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
}, table => [primaryKey({columns: [table.userId, table.gameId]})]);
