# LLM Adventure: Learning Objectives

Upon completing the game, players will be able to:

## 1. What Large Language Models Are

- Describe an LLM as a neural network trained on large amounts of text to predict the next token in a sequence.
- Identify the core mechanism of LLMs as statistical pattern matching over language, rather than true comprehension.
- List the key components that make up a modern LLM (tokenizer, embeddings, attention mechanism, feed-forward layers, output generation).

## 2. Tokenization

- Explain why LLMs process tokens rather than whole words or individual characters.
- Distinguish subword tokenization (BPE) from character-level and whole-word approaches.
- Recognize that tokenization can produce surprising splits, especially for rare or novel words.
- Describe how a fixed vocabulary of ~50,000 subword tokens can represent any possible text.

## 3. Word Embeddings

- Explain what a word embedding is (a vector of numbers representing a token's meaning).
- Demonstrate how semantic similarity is captured by distance in embedding space (e.g., "king" and "queen" are close together).
- Apply the concept of vector arithmetic to word relationships (e.g., king - man + woman ≈ queen).
- Identify that the same word can have different contextual meanings reflected in its embedding (e.g., "python" as a language vs. a snake).

## 4. The Attention Mechanism

- Describe the roles of Query, Key, and Value vectors in the attention mechanism.
- Explain how attention allows the model to determine which tokens are relevant to each other regardless of distance in the text.
- Apply attention concepts to resolve pronoun references in a sentence (e.g., identifying that "it" refers to "cat" in context).
- Recognize that attention is probabilistic, assigning varying degrees of relevance rather than a single definitive link.
- Identify how multiple attention heads allow the model to capture different types of relationships simultaneously.

## 5. Transformer Architecture

- Describe the transformer as a stack of layers, each containing attention and feed-forward components.
- Explain how deeper layers build increasingly abstract representations (from syntax to semantics to reasoning).
- Contrast transformers with older architectures (RNNs, LSTMs) in terms of parallelism and handling of long-range dependencies.
- Identify the 2017 "Attention Is All You Need" paper as the origin of the transformer architecture.

## 6. Pre-Training

- Describe pre-training as learning to predict the next token across billions of text examples.
- Explain how the simple objective of next-token prediction gives rise to grammar, factual knowledge, and reasoning abilities.
- Identify the types of data used in pre-training (web pages, books, code, conversations) and the scale involved.
- Recognize that biases and inaccuracies in training data are inherited by the model.

## 7. Fine-Tuning

- Distinguish fine-tuning from pre-training in terms of purpose, data, and scale.
- Explain how instruction tuning transforms a raw text-prediction model into a useful assistant.
- Describe the before-and-after behavioral difference (e.g., a pre-trained model continues text while a fine-tuned model answers questions).
- Recognize that fine-tuning uses smaller, curated datasets of high-quality input-output examples.

## 8. RLHF and Alignment

- Describe Reinforcement Learning from Human Feedback as a process where human raters compare model outputs to guide improvement.
- Apply the three principles of alignment — helpful, harmless, and honest — to evaluate model responses.
- Evaluate pairs of model outputs to identify which better adheres to alignment principles.
- Recognize the tension between helpfulness and safety (e.g., overly cautious refusals vs. genuinely helpful responses).
- Explain the role of a reward model in scoring outputs based on learned human preferences.

## 9. Text Generation and Sampling

- Describe how an LLM generates text by predicting a probability distribution over possible next tokens.
- Explain the effect of temperature on output: low temperature produces conservative/repetitive text, high temperature produces creative/chaotic text.
- Distinguish between top-k and top-p (nucleus) sampling as methods for controlling the candidate token pool.
- Select appropriate generation parameters for a given use case (e.g., lower temperature for factual tasks, higher for creative tasks).

## 10. Hallucinations and Limitations

- Define hallucination as confident, plausible-sounding output that is factually incorrect.
- Identify common hallucination patterns: fabricated citations, invented statistics, wrong attributions, and confidently stated falsehoods.
- Classify specific statements as factual or hallucinated based on critical evaluation.
- Recognize that an LLM's confidence does not correlate with accuracy.
- List additional limitations: finite context windows, no real-time information access, no true understanding, and inherited biases.

## 11. Applications

- List major application areas for LLMs: code generation, creative writing, translation, summarization, analysis, education, and conversation.
- Recognize the versatility of LLMs as general-purpose language tools across diverse domains.

## 12. Ethical Considerations

- Identify key ethical questions raised by LLMs: responsibility for harmful outputs, bias mitigation, impact on employment and education, prevention of misuse, content labeling, and equitable access.
- Recognize that responsible AI development requires diverse perspectives, transparency, and ongoing evaluation.

## 13. Prompt Engineering

- Explain that clear, specific prompts with context and desired format produce better LLM outputs than vague or unstructured prompts.
- Recognize that iterating on prompts based on results is more effective than repeating the same prompt.
- Distinguish effective prompt strategies from ineffective ones (e.g., specificity over verbosity).
