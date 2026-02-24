"""All item definitions for the game."""

from game.world import Item

ITEMS: dict[str, Item] = {
    "researcher_badge": Item(
        id="researcher_badge",
        name="Researcher Badge",
        description=(
            "A holographic ID badge that reads 'AUTHORIZED NEURAL NETWORK "
            "EXPLORER.' It shimmers with embedded watermarks. Apparently "
            "you'll need this to interact with the various subsystems inside "
            "the model."
        ),
    ),
    "architecture_diagram": Item(
        id="architecture_diagram",
        name="Architecture Diagram",
        description=(
            "A fold-out diagram showing the transformer architecture. Arrows "
            "flow from Input -> Tokenization -> Embedding -> Attention -> "
            "Feed-Forward -> Training -> Output -> Generation. A handy map "
            "of this strange place. The margins are full of annotations like "
            "'here be gradients' and 'abandon hope all ye who enter without "
            "batch normalization.'"
        ),
    ),
    "raw_prompt_fragment": Item(
        id="raw_prompt_fragment",
        name="Raw Prompt Fragment",
        description=(
            "A glowing shard of text plucked from the input stream. It reads "
            "'unbelievable' and pulses with potential energy, waiting to be "
            "processed by the tokenizer."
        ),
    ),
    "token_cleaver": Item(
        id="token_cleaver",
        name="Token Cleaver",
        description=(
            "A small but wickedly sharp cleaver used by the Tokenizer Gnome. "
            "It can split any word into its subword tokens with a single "
            "chop. The blade is etched with 'BPE' in tiny letters."
        ),
    ),
    "vocab_index": Item(
        id="vocab_index",
        name="Vocabulary Index",
        description=(
            "A thick reference book listing all 50,257 tokens in the model's "
            "vocabulary, each with its numeric ID. Most entries are subword "
            "fragments like 'tion' (ID: 653) or 'pre' (ID: 3866). Some "
            "entries are surprisingly specific, like ' cryptocurrency' as a "
            "single token."
        ),
    ),
    "embedding_compass": Item(
        id="embedding_compass",
        name="Embedding Compass",
        description=(
            "A multidimensional compass that points toward semantically "
            "similar concepts. Its needle doesn't point north -- it points "
            "toward meaning. Currently it's spinning between 768 dimensions, "
            "which is apparently normal."
        ),
    ),
    "query_crystal": Item(
        id="query_crystal",
        name="Query Crystal",
        description=(
            "A translucent crystal inscribed with the letter 'Q'. It pulses "
            "with questions: 'What am I looking for? What do I need to know?' "
            "One of three crystals that together power the attention mechanism."
        ),
    ),
    "key_crystal": Item(
        id="key_crystal",
        name="Key Crystal",
        description=(
            "A translucent crystal inscribed with the letter 'K'. It hums "
            "with declarations: 'Here is what I contain. Here is what I "
            "offer.' One of three crystals for the attention mechanism."
        ),
    ),
    "value_crystal": Item(
        id="value_crystal",
        name="Value Crystal",
        description=(
            "A translucent crystal inscribed with the letter 'V'. It glows "
            "with substance: 'This is my actual information. Take what you "
            "need.' The third crystal for the attention mechanism."
        ),
    ),
    "attention_matrix": Item(
        id="attention_matrix",
        name="Attention Matrix",
        description=(
            "A shimmering grid of light formed when the Q, K, and V crystals "
            "were united. It shows which tokens attend to which other tokens "
            "in any sentence. Watching it work is mesmerizing -- like seeing "
            "language understand itself."
        ),
    ),
    "training_data_sample": Item(
        id="training_data_sample",
        name="Training Data Sample",
        description=(
            "A hefty book labeled 'SAMPLE: PRE-TRAINING CORPUS, VOL. "
            "4,721,883 OF 12,000,000.' It contains snippets of web pages, "
            "books, code, and conversations. Some entries are clearly "
            "biased or outdated, which explains a few things about model "
            "behavior. A sticky note reads: 'Garbage in, garbage out.'"
        ),
    ),
    "fine_tuning_wrench": Item(
        id="fine_tuning_wrench",
        name="Fine-Tuning Wrench",
        description=(
            "A precision instrument used to adjust model behavior after "
            "pre-training. The dial has settings like 'instruction following,' "
            "'helpfulness,' and 'safety.' Unlike the blunt force of "
            "pre-training, this tool makes surgical adjustments."
        ),
    ),
    "alignment_compass": Item(
        id="alignment_compass",
        name="Alignment Compass",
        description=(
            "A moral compass that points toward responses that are helpful, "
            "harmless, and honest. Its three needles -- H, H, and H -- "
            "sometimes point in slightly different directions, illustrating "
            "the tension between these goals."
        ),
    ),
    "probability_lens": Item(
        id="probability_lens",
        name="Probability Lens",
        description=(
            "A monocle-like lens that reveals the probability distribution "
            "over the vocabulary for the next token. Looking through it, "
            "you can see percentages floating over each possible next word. "
            "It's like seeing the model's confidence level in real time."
        ),
    ),
    "temperature_dial": Item(
        id="temperature_dial",
        name="Temperature Dial",
        description=(
            "A brass dial salvaged from the Sampling Chamber, calibrated "
            "from 0.0 to 2.0. At 0.0, the model always picks the most "
            "likely token (boring but safe). At 2.0, it's practically "
            "rolling dice (creative but chaotic). The sweet spot depends "
            "on what you're trying to generate."
        ),
    ),
    "hallucination_detector": Item(
        id="hallucination_detector",
        name="Hallucination Detector",
        description=(
            "A device shaped like a magnifying glass with a red/green "
            "indicator. It can scan text and highlight statements that are "
            "confidently stated but factually wrong -- the hallmark of LLM "
            "hallucinations. The label reads: 'Trust, but verify.'"
        ),
    ),
}
