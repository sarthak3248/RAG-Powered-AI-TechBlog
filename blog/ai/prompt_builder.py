
class PromptBuilder:
    
    @staticmethod
    def build(question, posts, history=None):
        
        context = ""
        
        conversation = ""

        if history:

            conversation = "\nPrevious Conversation:\n\n"

            for item in history:

                conversation += (
                    f"User: {item['user']}\n"
                    f"Assistant: {item['assistant']}\n\n"
                )
        
        for i, post in enumerate(posts, start=1):
            
            context += (
                f"\nArticle {i}\n"
                f"Title: {post.title}\n"
                f"Content: \n{post.content}\n\n"
            )
            
        prompt = f"""
        You are an AI assistant for an AI TechBlog.

        Instructions:
        - Answer using the blog articles whenever they contain the answer.
        - If the blog articles don't answer the question, use your general knowledge.
        - If the user asks a follow-up question, use the previous conversation to understand the context.
        - Be clear, accurate, and concise.
        - Never invent information about blog articles.

        {conversation}

        Blog Context:
        {context}

        Current User Question:
        {question}

        Answer:
        """
        
        return prompt.strip()
    
    