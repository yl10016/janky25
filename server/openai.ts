import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function generateAIResponse(
  thoughts: string,
  articleSummary: string
): Promise<string> {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        {
          role: "system",
          content: 
            "You are an engaging discussion partner analyzing news articles. " +
            "Provide thoughtful responses that encourage critical thinking and discussion. " +
            "Keep responses concise (2-3 sentences) but insightful."
        },
        {
          role: "user",
          content: 
            `Article Summary: ${articleSummary}\n\n` +
            `User's Thoughts: ${thoughts}\n\n` +
            "Please provide a response that engages with the user's perspective while adding additional context or questions to consider."
        }
      ],
      max_tokens: 150,
    });

    return response.choices[0].message.content || "I apologize, but I couldn't generate a response at this time.";
  } catch (error) {
    console.error("OpenAI API error:", error);
    throw new Error("Failed to generate AI response");
  }
}