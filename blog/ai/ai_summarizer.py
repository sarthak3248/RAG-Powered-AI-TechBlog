from transformers import pipeline


class ArticleSummarizer:
    """
    Lazy-loaded summarization service.
    """

    _summarizer = None

    @classmethod
    def get_model(cls):

        if cls._summarizer is None:

            print("Loading summarization model...")

            cls._summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn"
            )

        return cls._summarizer

    @classmethod
    def summarize(cls, text):

        if not text:
            return ""

        summarizer = cls.get_model()

        # BART has a maximum input length, so we'll use the first part
        text = text[:3000]

        summary = summarizer(
            text,
            max_length=100,
            min_length=40,
            do_sample=False
        )

        return summary[0]["summary_text"]