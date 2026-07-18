from blog.ai.retriver_service import Retriver
from blog.ai.prompt_builder import PromptBuilder
from blog.ai.llm_service import LLMService


class ChatbotService:

    @classmethod
    def answer(cls, question):

        # Retrieve relevant blog posts
        posts = Retriver.retrive(
            question,
            top_k=3
        )

        # Build RAG prompt
        prompt = PromptBuilder.build(
            question,
            posts
        )

        # Generate answer
        response = LLMService.generate(
            prompt
        )

        return response