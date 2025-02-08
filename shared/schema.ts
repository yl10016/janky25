import { pgTable, text, serial, integer, timestamp, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const articles = pgTable("articles", {
  id: serial("id").primaryKey(),
  headline: text("headline").notNull(),
  summary: text("summary").notNull(),
  sourceUrl: text("source_url").notNull(),
  imageUrl: text("image_url").notNull(),
  facts: jsonb("facts").notNull().$type<string[]>(),
  publishedAt: timestamp("published_at").notNull(),
});

export const responses = pgTable("responses", {
  id: serial("id").primaryKey(),
  articleId: integer("article_id").notNull(),
  agreement: integer("agreement").notNull(),
  thoughts: text("thoughts").notNull(),
  aiResponse: text("ai_response"),
});

export const insertArticleSchema = createInsertSchema(articles).omit({ id: true });
export const insertResponseSchema = createInsertSchema(responses).omit({ id: true, aiResponse: true });

export type Article = typeof articles.$inferSelect;
export type InsertArticle = z.infer<typeof insertArticleSchema>;
export type Response = typeof responses.$inferSelect;
export type InsertResponse = z.infer<typeof insertResponseSchema>;
