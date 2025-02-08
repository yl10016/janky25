import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { generateAIResponse } from "./openai";
import { insertResponseSchema } from "@shared/schema";
import { ZodError } from "zod";

export function registerRoutes(app: Express): Server {
  app.get("/api/articles", async (req, res) => {
    const limit = 3;
    const articles = await storage.getArticles(limit);
    res.json(articles);
  });

  app.get("/api/articles/:id", async (req, res) => {
    const article = await storage.getArticle(parseInt(req.params.id));
    if (!article) {
      res.status(404).json({ message: "Article not found" });
      return;
    }
    res.json(article);
  });

  app.post("/api/responses", async (req, res) => {
    try {
      const data = insertResponseSchema.parse(req.body);
      const response = await storage.createResponse(data);

      const article = await storage.getArticle(data.articleId);
      if (!article) {
        throw new Error("Article not found");
      }

      try {
        const aiResponse = await generateAIResponse(data.thoughts, article.summary);
        const updatedResponse = await storage.updateResponse(response.id, aiResponse);
        res.json(updatedResponse);
      } catch (aiError) {
        console.error("AI Response Error:", aiError);
        // Still return the user's response even if AI generation fails
        res.json({ 
          ...response, 
          aiResponse: "I apologize, but I'm unable to generate a response at this moment. Please try again later."
        });
      }
    } catch (error) {
      if (error instanceof ZodError) {
        res.status(400).json({ message: "Invalid request data", errors: error.errors });
      } else {
        console.error("Response Error:", error);
        res.status(400).json({ message: error instanceof Error ? error.message : "An error occurred" });
      }
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}