import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import type { Response } from "@shared/schema";

interface AIChatProps {
  articleId: number;
}

export default function AIChat({ articleId }: AIChatProps) {
  const [thoughts, setThoughts] = useState("");
  const [agreement, setAgreement] = useState(3);
  const { toast } = useToast();

  const { mutate: submitResponse, isPending } = useMutation({
    mutationFn: async () => {
      const res = await apiRequest("POST", "/api/responses", {
        articleId,
        agreement,
        thoughts,
      });
      return res.json() as Promise<Response>;
    },
    onSuccess: (data) => {
      setThoughts("");
      toast({
        title: "Response received!",
        description: data.aiResponse,
      });
    },
    onError: () => {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to submit your response. Please try again.",
      });
    },
  });

  return (
    <div className="space-y-4">
      <Label className="text-lg font-semibold">Share your thoughts</Label>
      <Textarea
        placeholder="What do you think about this article?"
        value={thoughts}
        onChange={(e) => setThoughts(e.target.value)}
        className="min-h-[100px]"
      />
      <Button
        onClick={() => submitResponse()}
        disabled={!thoughts.trim() || isPending}
        className="w-full"
      >
        {isPending ? "Getting AI Response..." : "Send and Get AI Response"}
      </Button>
    </div>
  );
}
