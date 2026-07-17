
class PromptBuilder:
    
    @staticmethod
    def build(question, posts):
        
        context = ""
        
        for i, post in enumerate(posts, start=1):
            
            context += (
                f"\nArticle {i}\n",
                f"Title: {post.title}\n",
                f"Content: \n{post.content}\n\n"
            )
            
        prompt = f"""
        You are an AI assistant for an AI TechBlog.

        Instructions:
        - Answer using the blog articles whenever they contain the answer.
        - If the blog articles don't answer the question, use your general knowledge.
        - Be clear, accurate, and concise.
        - Never invent information about blog articles.

        Blog Context:
        {context}

        User Question:
        {question}

        Answer:
        """    
        
        return prompt.strip()
    
    