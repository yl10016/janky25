import { useRoute } from "wouter";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import AgreementSlider from "@/components/agreement-slider";
import AIChat from "@/components/ai-chat";
import type { Article } from "@shared/schema";

export default function ArticlePage() {
  const [, params] = useRoute("/article/:id");
  const articleId = parseInt(params?.id || "0");

  const { data: article, isLoading, error } = useQuery<Article>({
    queryKey: [`/api/articles/${articleId}`],
  });

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardContent className="p-6 space-y-4">
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-48 w-full" />
            <Skeleton className="h-24 w-full" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardContent className="p-6">
            <h1 className="text-2xl font-bold text-red-500">Error loading article</h1>
            <p className="text-gray-600">Unable to load the article. Please try again later.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Card>
        <CardContent className="p-6">
          <h1 className="text-3xl font-bold mb-4">{article.headline}</h1>

          <img
            src={article.imageUrl}
            alt={article.headline}
            className="w-full h-64 object-cover rounded-lg mb-6"
          />

          <div className="prose max-w-none mb-6">
            <p className="text-lg">{article.summary}</p>

            <h2 className="text-xl font-semibold mt-4 mb-2">Key Facts</h2>
            <ul className="list-disc pl-5">
              {article.facts.map((fact, index) => (
                <li key={index} className="mb-1">{fact}</li>
              ))}
            </ul>

            <a
              href={article.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-4 text-primary hover:underline"
            >
              Read full article
            </a>
          </div>

          <div className="space-y-6">
            <AgreementSlider articleId={article.id} />
            <AIChat articleId={article.id} />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}