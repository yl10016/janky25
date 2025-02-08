import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Link } from "wouter";
import type { Article } from "@shared/schema";

interface NewsCardProps {
  article: Article;
}

export default function NewsCard({ article }: NewsCardProps) {
  return (
    <Link href={`/article/${article.id}`}>
      <Card className="cursor-pointer hover:shadow-lg transition-shadow">
        <CardHeader className="p-0">
          <img
            src={article.imageUrl}
            alt={article.headline}
            className="w-full h-48 object-cover rounded-t-lg"
          />
        </CardHeader>
        <CardContent className="p-4">
          <h2 className="text-xl font-semibold mb-2 line-clamp-2">
            {article.headline}
          </h2>
          <p className="text-muted-foreground line-clamp-3">
            {article.summary}
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}
