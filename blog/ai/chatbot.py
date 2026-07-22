from blog.ai.retriver_service import Retriver
from blog.ai.prompt_builder import PromptBuilder
from blog.ai.llm_service import LLMService


class ChatbotService:

    @staticmethod
    def answer(question, history=None):

        posts = Retriver.retrive(question)

        prompt = PromptBuilder.build(
            question,
            posts,
            history
        )

        return LLMService.generate(prompt)