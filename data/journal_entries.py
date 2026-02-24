"""Educational journal entries for each LLM concept."""

JOURNAL_ENTRIES: dict[str, dict] = {
    "what_are_llms": {
        "title": "What Are Large Language Models?",
        "summary": (
            "LLMs are massive neural networks trained on enormous amounts of "
            "text data. They learn statistical patterns in language -- which "
            "words tend to follow which other words, how ideas connect, and "
            "how to generate coherent text. They don't 'understand' language "
            "the way humans do, but they're remarkably good at predicting "
            "what text should come next. Models like GPT-4, Claude, and "
            "Llama contain billions of parameters (adjustable numbers) that "
            "encode these patterns."
        ),
    },
    "transformer_architecture": {
        "title": "The Transformer Architecture",
        "summary": (
            "Transformers are the architecture behind modern LLMs, introduced "
            "in the 2017 paper 'Attention Is All You Need.' Unlike older "
            "designs (RNNs, LSTMs) that process text one word at a time, "
            "transformers process all tokens simultaneously using a mechanism "
            "called 'attention.' This parallelism makes them much faster to "
            "train and allows them to capture long-range dependencies in "
            "text. A transformer consists of stacked layers, each containing "
            "an attention mechanism and a feed-forward network."
        ),
    },
    "tokenization": {
        "title": "Tokenization",
        "summary": (
            "Before an LLM can process text, it must be broken into tokens "
            "-- the basic units the model works with. Tokens aren't always "
            "whole words: common words like 'the' are single tokens, but "
            "less common words get split into subword pieces (e.g., "
            "'unbelievable' becomes 'un' + 'believ' + 'able'). This "
            "approach, called Byte-Pair Encoding (BPE), balances vocabulary "
            "size with the ability to handle any text, including made-up "
            "words and code. A typical LLM vocabulary has around 50,000 "
            "tokens."
        ),
    },
    "embeddings": {
        "title": "Word Embeddings",
        "summary": (
            "Once text is tokenized, each token is converted into an "
            "embedding -- a vector (list of numbers) that captures its "
            "meaning. These vectors exist in a high-dimensional space "
            "(typically 768 to 12,288 dimensions) where similar concepts "
            "cluster together. The famous example: the vector for 'king' "
            "minus 'man' plus 'woman' approximately equals 'queen.' "
            "Embeddings allow the model to reason about meaning "
            "mathematically rather than treating words as arbitrary symbols."
        ),
    },
    "attention_mechanism": {
        "title": "The Attention Mechanism",
        "summary": (
            "Attention is how a transformer decides which parts of the "
            "input are relevant to each other. It works through three "
            "components: Queries (Q), Keys (K), and Values (V). Each token "
            "generates a Query ('what am I looking for?'), a Key ('what do "
            "I contain?'), and a Value ('here's my information'). The model "
            "compares each Query against all Keys to compute attention "
            "scores, then uses those scores to create a weighted mix of "
            "Values. This is how the model resolves pronouns, connects "
            "ideas across sentences, and builds understanding of context."
        ),
    },
    "pretraining": {
        "title": "Pre-Training",
        "summary": (
            "Pre-training is the first and most expensive phase of creating "
            "an LLM. The model reads billions of words from books, websites, "
            "code, and other text, learning to predict the next token in a "
            "sequence. This simple objective -- next-token prediction -- "
            "turns out to teach the model grammar, facts, reasoning, and "
            "even some degree of common sense. Pre-training requires "
            "enormous computational resources (thousands of GPUs running "
            "for weeks). The resulting model is a 'foundation model' that "
            "knows a lot but isn't yet good at following instructions."
        ),
    },
    "finetuning": {
        "title": "Fine-Tuning",
        "summary": (
            "After pre-training, models are fine-tuned on specific, curated "
            "datasets to improve their behavior. Instruction tuning teaches "
            "the model to follow user requests by training on examples of "
            "instructions paired with good responses. This transforms a raw "
            "foundation model (which just predicts text) into an assistant "
            "that can answer questions, write code, summarize documents, "
            "and more. Fine-tuning uses much less data and compute than "
            "pre-training but has a dramatic effect on usefulness."
        ),
    },
    "rlhf_alignment": {
        "title": "RLHF and Alignment",
        "summary": (
            "Reinforcement Learning from Human Feedback (RLHF) is used to "
            "align LLMs with human preferences. Human raters compare pairs "
            "of model outputs and indicate which is better. These "
            "preferences train a 'reward model' that scores outputs, which "
            "then guides the LLM to produce responses that are helpful, "
            "harmless, and honest. This is how models learn to refuse "
            "dangerous requests, acknowledge uncertainty, and balance "
            "helpfulness with safety. Alignment remains an active and "
            "important area of AI safety research."
        ),
    },
    "text_generation": {
        "title": "Text Generation and Sampling",
        "summary": (
            "When an LLM generates text, it predicts a probability "
            "distribution over all possible next tokens, then samples "
            "from that distribution. Key parameters control this process: "
            "Temperature scales the probabilities (low = conservative, "
            "high = creative/chaotic). Top-K limits sampling to the K most "
            "likely tokens. Top-P (nucleus sampling) limits sampling to "
            "tokens whose cumulative probability reaches P. These settings "
            "let you balance between predictable/repetitive output and "
            "creative/unpredictable output."
        ),
    },
    "hallucinations_limitations": {
        "title": "Hallucinations and Limitations",
        "summary": (
            "LLMs can generate text that sounds confident and plausible but "
            "is factually wrong -- these are called 'hallucinations.' Common "
            "types include fabricated citations, invented statistics, wrong "
            "attributions, and confidently stated falsehoods. LLMs also "
            "have limited context windows (they can only process so much "
            "text at once), no access to real-time information, no true "
            "understanding of the world, and biases inherited from their "
            "training data. Critical thinking and verification are essential "
            "when using LLM outputs."
        ),
    },
    "ethics": {
        "title": "Ethical Considerations",
        "summary": (
            "LLMs raise important ethical questions: Who is responsible "
            "when an LLM produces harmful content? How do we address biases "
            "in training data that perpetuate stereotypes? What are the "
            "implications for jobs, education, and creativity? How do we "
            "prevent misuse while enabling beneficial applications? These "
            "questions don't have easy answers, but they're crucial to "
            "consider as LLMs become more integrated into society. "
            "Responsible AI development requires diverse perspectives, "
            "transparency, and ongoing evaluation."
        ),
    },
}
