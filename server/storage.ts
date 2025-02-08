import { Article, InsertArticle, Response, InsertResponse } from "@shared/schema";

export interface IStorage {
  getArticles(limit: number): Promise<Article[]>;
  getArticle(id: number): Promise<Article | undefined>;
  createArticle(article: InsertArticle): Promise<Article>;
  createResponse(response: InsertResponse): Promise<Response>;
  updateResponse(id: number, aiResponse: string): Promise<Response>;
}

export class MemStorage implements IStorage {
  private articles: Map<number, Article>;
  private responses: Map<number, Response>;
  private articleId: number;
  private responseId: number;

  constructor() {
    this.articles = new Map();
    this.responses = new Map();
    this.articleId = 1;
    this.responseId = 1;
    this.seedData();
  }

  private seedData() {
    const mockArticles: InsertArticle[] = [
      {
        headline: "AI Breakthrough in Medical Research",
        summary: "Scientists have developed a new AI system that can predict disease progression with 95% accuracy.",
        sourceUrl: "https://example.com/ai-medical",
        imageUrl: "https://images.unsplash.com/photo-1581092787765-e3feb951d987",
        facts: ["95% prediction accuracy", "Tested on 10,000 patients", "Reduces diagnosis time by 60%"],
        publishedAt: new Date(),
      },
      {
        headline: "Global Climate Summit Reaches Historic Agreement",
        summary: "World leaders commit to ambitious carbon reduction targets in landmark climate deal.",
        sourceUrl: "https://example.com/climate-summit",
        imageUrl: "https://images.unsplash.com/photo-1560957123-e8e019c66980",
        facts: ["190 countries participated", "50% emission reduction by 2030", "1 trillion USD commitment"],
        publishedAt: new Date(),
      },
      {
        headline: "Revolutionary Battery Technology Unveiled",
        summary: "New battery design promises to double electric vehicle range while cutting costs.",
        sourceUrl: "https://example.com/battery-tech",
        imageUrl: "https://images.unsplash.com/photo-1495020689067-958852a7765e",
        facts: ["2x energy density", "40% cost reduction", "Sustainable materials used"],
        publishedAt: new Date(),
      }
    ];

    mockArticles.forEach(article => this.createArticle(article));
  }

  async getArticles(limit: number): Promise<Article[]> {
    return Array.from(this.articles.values())
      .sort((a, b) => b.publishedAt.getTime() - a.publishedAt.getTime())
      .slice(0, limit);
  }

  async getArticle(id: number): Promise<Article | undefined> {
    return this.articles.get(id);
  }

  async createArticle(article: InsertArticle): Promise<Article> {
    const id = this.articleId++;
    const newArticle = { ...article, id };
    this.articles.set(id, newArticle);
    return newArticle;
  }

  async createResponse(response: InsertResponse): Promise<Response> {
    const id = this.responseId++;
    const newResponse = { ...response, id, aiResponse: null };
    this.responses.set(id, newResponse);
    return newResponse;
  }

  async updateResponse(id: number, aiResponse: string): Promise<Response> {
    const response = this.responses.get(id);
    if (!response) throw new Error("Response not found");
    const updatedResponse = { ...response, aiResponse };
    this.responses.set(id, updatedResponse);
    return updatedResponse;
  }
}

export const storage = new MemStorage();
