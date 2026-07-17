from transformers import pipeline


class LLMService:
    
    _generator = None
    
    @classmethod
    def get_model(cls):
        
        if cls._generator is None:
            
            print("Loading LLM...")
            
            cls._generator = pipeline("text2text-generation", model="google/flan-t5-base")
            
            print("LLM Loaded!!!")
            
        return cls._generator    
    
    @classmethod
    def generate(cls, prompt, max_tokens=256):
        
        model = cls.get_model()
        
        response = model(prompt, max_new_tokens=max_tokens, do_sample=True, temperature=0.3)
        
        return response[0]["generated_text"]
    
    