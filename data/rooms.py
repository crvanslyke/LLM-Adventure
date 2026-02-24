"""All 18 room definitions for the game world."""

from game.world import Room, Exit

ROOMS: dict[str, Room] = {

    # =========================================================================
    # ZONE 1: ENTRY
    # =========================================================================

    "lobby": Room(
        id="lobby",
        name="The Digitization Lobby",
        zone="Entry",
        description=(
            "A sterile white room where you materialized after being "
            "digitized. The walls hum with electromagnetic energy. A "
            "flickering neon sign reads 'WELCOME TO THE INTERIOR OF A LARGE "
            "LANGUAGE MODEL. MIND THE FLOATING POINT ERRORS.'\n\n"
            "A reception desk sits against the north wall with a dusty "
            "terminal on it. A brass plaque hangs on the east wall. The "
            "only exit leads south to a long hallway."
        ),
        exits=(
            Exit(direction="south", destination="orientation_hall"),
        ),
        items=("researcher_badge",),
        on_first_visit=(
            "You blink. The digitization worked. You're standing inside a "
            "neural network -- though it looks more like a retro sci-fi "
            "movie set than a mathematical abstraction. Dr. Chen's voice "
            "crackles through an invisible speaker: 'You're in. Explore, "
            "learn, and find the exit portal. Good luck.'"
        ),
        examine_targets={
            "sign": (
                "The sign flickers between 'WELCOME TO THE INTERIOR OF A "
                "LARGE LANGUAGE MODEL' and 'PARAMETERS: ~70 BILLION. "
                "PLEASE DO NOT ADJUST.' Beneath it in smaller text: "
                "'This model processes language by predicting the most likely "
                "next token in a sequence. It doesn't understand you. "
                "It's very good at pretending it does.'"
            ),
            "terminal": (
                "The terminal displays scrolling text:\n\n"
                "  'SYSTEM STATUS: OPERATIONAL'\n"
                "  'MODEL TYPE: Autoregressive Transformer'\n"
                "  'TRAINING DATA: ~2 trillion tokens from books, websites,'\n"
                "  '  code repositories, and conversations'\n"
                "  'PARAMETERS: Billions of adjustable weights that encode'\n"
                "  '  statistical patterns in human language'\n\n"
                "So this is what an LLM looks like from the inside. A "
                "massive statistical machine that learned to mimic human "
                "language by reading most of the internet."
            ),
            "plaque": (
                "The brass plaque reads:\n\n"
                "  'WHAT IS A LARGE LANGUAGE MODEL?'\n\n"
                "  'An LLM is a neural network -- a mathematical system'\n"
                "  'loosely inspired by biological brains -- trained on'\n"
                "  'enormous amounts of text. By learning to predict what'\n"
                "  'word comes next in billions of sentences, it develops'\n"
                "  'the ability to generate coherent, contextual text.'\n\n"
                "  'LLMs power chatbots, coding assistants, translators,'\n"
                "  'and more. They are powerful but imperfect tools.'"
            ),
            "desk": (
                "A standard-issue reception desk. A dusty terminal sits on "
                "top, and you notice a researcher badge has been left here "
                "for you."
            ),
        },
    ),

    "orientation_hall": Room(
        id="orientation_hall",
        name="The Orientation Hall",
        zone="Entry",
        description=(
            "A long hallway lined with portraits of famous neural network "
            "architectures. Display cases along the walls contain artifacts "
            "from earlier eras of AI. A holographic docent stands in the "
            "center, looping through a presentation.\n\n"
            "Exits lead north back to the lobby and south to the input "
            "buffer."
        ),
        exits=(
            Exit(direction="north", destination="lobby"),
            Exit(direction="south", destination="input_buffer"),
        ),
        items=("architecture_diagram",),
        examine_targets={
            "portraits": (
                "The portraits show the evolution of neural networks:\n\n"
                "  - A faded daguerreotype of a PERCEPTRON (1958)\n"
                "  - An oil painting of a RECURRENT NEURAL NETWORK (1986)\n"
                "  - A watercolor of an LSTM (1997) -- 'I remember everything!'\n"
                "  - A photograph of a CONVOLUTIONAL NET (2012) -- 'I see things!'\n"
                "  - A gleaming hologram of a TRANSFORMER (2017)\n\n"
                "The Transformer portrait is by far the largest. A caption "
                "reads: 'Attention Is All You Need -- Vaswani et al., 2017. "
                "The architecture that changed everything.'"
            ),
            "display cases": (
                "The cases contain relics:\n"
                "  - An RNN fossil, curled in a spiral. Plaque: 'Processed "
                "text one word at a time. Slow but pioneering.'\n"
                "  - A dusty CNN lens. Plaque: 'Great at images, less so at "
                "understanding War and Peace.'\n"
                "  - A faded LSTM cell. Plaque: 'Could remember things, but "
                "struggled with very long texts.'\n\n"
                "All superseded by the transformer architecture."
            ),
            "cases": (
                "The cases contain relics:\n"
                "  - An RNN fossil, curled in a spiral\n"
                "  - A dusty CNN lens\n"
                "  - A faded LSTM cell\n\n"
                "All superseded by the transformer architecture."
            ),
            "docent": (
                "The holographic docent speaks:\n\n"
                "  'The Transformer architecture processes all tokens in "
                "parallel, using a mechanism called attention to understand "
                "relationships between words regardless of their distance "
                "in the text. It consists of stacked layers, each containing "
                "an attention mechanism and a feed-forward network. This "
                "design allows transformers to be trained much faster than "
                "previous architectures and to handle much longer texts.'"
            ),
        },
        talk_targets={
            "docent": (
                "The docent flickers and turns to you:\n\n"
                "  'Ah, a visitor! Welcome to the interior of a transformer "
                "model. You'll want to head south to see how text enters "
                "the model. From there, follow the processing pipeline: "
                "tokenization, embedding, attention, and onward to output "
                "generation.'\n\n"
                "  'Each area contains puzzles that will test your "
                "understanding. Items you find along the way will help you "
                "solve them. And do keep your journal updated -- you'll "
                "need what you learn to find the exit.'\n\n"
                "  'Oh, and one more thing: it is pitch dark inside a "
                "neural network layer. You are likely to be eaten by a "
                "gradient. Just kidding. Mostly.'"
            ),
        },
    ),

    "input_buffer": Room(
        id="input_buffer",
        name="The Input Buffer",
        zone="Entry",
        description=(
            "A staging area where raw text arrives before processing. "
            "Glowing strings of text float in from a portal in the ceiling, "
            "drifting like luminous jellyfish. A conveyor belt on the floor "
            "carries text fragments toward the western exit.\n\n"
            "On the east wall, a massive bookshelf holds the model's entire "
            "vocabulary. To the west, you hear the rhythmic chopping of the "
            "tokenizer.\n\n"
            "Exits: north to the Orientation Hall, west to the Tokenizer "
            "Workshop, east to the Vocabulary Vault."
        ),
        exits=(
            Exit(direction="north", destination="orientation_hall"),
            Exit(direction="west", destination="tokenizer_workshop"),
            Exit(direction="east", destination="vocabulary_vault"),
        ),
        items=("raw_prompt_fragment",),
        examine_targets={
            "text": (
                "Glowing strings drift down from above:\n"
                "  'What is the meaning of...'\n"
                "  'Write a Python function that...'\n"
                "  'Explain quantum computing to a...'\n\n"
                "Each is a prompt from the outside world, waiting to be "
                "processed. They seem to flow naturally toward the west -- "
                "the tokenizer."
            ),
            "conveyor belt": (
                "The conveyor belt moves text fragments westward toward "
                "the Tokenizer Workshop. Arrows painted on the floor show "
                "the direction of text processing flow."
            ),
            "conveyor": (
                "The conveyor belt moves text fragments westward toward "
                "the Tokenizer Workshop."
            ),
            "portal": (
                "The portal in the ceiling connects to the outside world. "
                "Through it, you can see faint glimpses of users typing "
                "prompts at their keyboards. Each prompt becomes a glowing "
                "string of text that drifts down into this room."
            ),
        },
    ),

    # =========================================================================
    # ZONE 2: TOKENIZATION & EMBEDDING
    # =========================================================================

    "tokenizer_workshop": Room(
        id="tokenizer_workshop",
        name="The Tokenizer Workshop",
        zone="Tokenization & Embedding",
        description=(
            "A chaotic workshop filled with chopping blocks, slicing "
            "machines, and bins labeled with subword fragments like 'tion', "
            "'pre', 'ing', and 'un'. Wood shavings -- no, token shavings "
            "-- cover the floor.\n\n"
            "A grumpy Tokenizer Gnome stands at the main workbench, his "
            "cleaver raised. Signs on the wall show examples: 'unhappiness' "
            "-> ['un', 'happiness'], 'ChatGPT' -> ['Chat', 'G', 'PT'].\n\n"
            "Exits: east to the Input Buffer, south to Embedding Space."
        ),
        exits=(
            Exit(direction="east", destination="input_buffer"),
            Exit(
                direction="south",
                destination="embedding_space",
                requires_flag="tokenizer_puzzle_solved",
                locked_message=(
                    "The Tokenizer Gnome blocks your path. 'Nothing passes "
                    "through my workshop unsplit! Show me you understand how "
                    "tokenization works first. Do you have a raw prompt "
                    "fragment? Use it on my workbench.'"
                ),
            ),
        ),
        items=(),
        puzzle_id="tokenizer",
        examine_targets={
            "gnome": (
                "The Tokenizer Gnome is a small, meticulous creature with "
                "ink-stained fingers and a perpetual frown. He takes his "
                "work very seriously. 'Words!' he mutters. 'Everyone thinks "
                "words are the basic unit. Pfah! TOKENS are the basic "
                "unit!'"
            ),
            "signs": (
                "The signs show tokenization examples:\n"
                "  'unhappiness' -> ['un', 'happiness']\n"
                "  'ChatGPT' -> ['Chat', 'G', 'PT']\n"
                "  'tokenization' -> ['token', 'ization']\n"
                "  ' the' -> [' the'] (common words stay whole!)\n"
                "  '  ' -> [' ', ' '] (even spaces are tokens)\n\n"
                "A footnote reads: 'This is Byte-Pair Encoding (BPE). "
                "Start with individual characters, then iteratively merge "
                "the most frequent pairs.'"
            ),
            "workbench": (
                "A sturdy workbench with a chopping block in the center. "
                "This is where the Tokenizer Gnome splits text into tokens. "
                "You could use a raw prompt fragment here to start the "
                "tokenization challenge."
            ),
            "bins": (
                "Bins overflow with token fragments:\n"
                "  'tion' (very popular), 'ing' (also popular),\n"
                "  'pre', 'un', 'able', 'ment', 'ness'...\n"
                "These subword pieces are the building blocks of the "
                "model's vocabulary."
            ),
        },
        talk_targets={
            "gnome": (
                "The Gnome eyes you suspiciously.\n\n"
                "  'Another one who thinks words are the basic unit? Ha! "
                "Let me educate you. I split text into TOKENS -- subword "
                "pieces that the model actually processes. Common words "
                "like \"the\" stay whole, but longer words get chopped up.'\n\n"
                "  'Why? Because a fixed vocabulary can't contain every "
                "possible word. But it CAN contain common subword pieces "
                "that combine to form any word. Clever, eh?'\n\n"
                "  'Now, if you've got a raw prompt fragment, use it on my "
                "workbench and I'll test your understanding!'"
            ),
        },
    ),

    "vocabulary_vault": Room(
        id="vocabulary_vault",
        name="The Vocabulary Vault",
        zone="Tokenization & Embedding",
        description=(
            "An enormous circular library stretching upward into darkness. "
            "The walls are lined with 50,257 cubbyholes, each containing a "
            "single token on a small card. A ladder on a rail circles the "
            "room.\n\n"
            "Most cubbyholes hold fragments: 'tion', 'pre', 'ing'. Some "
            "hold complete words: 'the', 'and', 'is'. A few hold "
            "surprisingly specific entries. A catalog index sits on a "
            "pedestal in the center.\n\n"
            "Exits: west to the Input Buffer, south to Embedding Space."
        ),
        exits=(
            Exit(direction="west", destination="input_buffer"),
            Exit(direction="south", destination="embedding_space"),
        ),
        items=("vocab_index",),
        examine_targets={
            "cubbyholes": (
                "You peer at a few cubbyholes:\n"
                "  #0: '!' -- punctuation gets its own token\n"
                "  #262: ' the' -- note the leading space! Tokens include "
                "their preceding space\n"
                "  #3866: 'pre' -- a common prefix\n"
                "  #15496: 'Hello' -- common enough for its own token\n"
                "  #50256: '<|endoftext|>' -- a special token marking the "
                "end of a document\n\n"
                "Each token has a unique numeric ID. The model sees these "
                "numbers, not the text itself."
            ),
            "catalog": (
                "The catalog is a thick reference book. Some interesting "
                "entries:\n\n"
                "  - The longest single token: ' cryptocurrency' (14 chars)\n"
                "  - Numbers are split: '2025' -> ['20', '25']\n"
                "  - Code tokens: ' def', ' class', ' return' are common\n"
                "  - Emoji: some are single tokens, others require multiple\n\n"
                "The key insight: the model's 'alphabet' isn't letters or "
                "words, but these 50,257 subword tokens."
            ),
            "index": (
                "The catalog index lists all 50,257 tokens. It would take "
                "you a very long time to read the whole thing, but it's a "
                "useful reference."
            ),
            "ladder": (
                "A brass ladder on a circular rail. You could climb it to "
                "reach the higher cubbyholes, but you get the idea -- "
                "there are a LOT of tokens."
            ),
        },
    ),

    "embedding_space": Room(
        id="embedding_space",
        name="Embedding Space",
        zone="Tokenization & Embedding",
        description=(
            "You step onto a transparent platform floating in a vast, "
            "shimmering void. Points of light surround you in every "
            "direction -- each one a token, positioned in a 768-dimensional "
            "space according to its meaning.\n\n"
            "Nearby, 'king' and 'queen' float close together, connected by "
            "a faint line. 'Python' hovers between a cluster of programming "
            "languages and a cluster of reptiles. Far below, 'banana' and "
            "'monarchy' drift apart.\n\n"
            "A navigation console on the platform blinks invitingly.\n\n"
            "Exits: north to the Tokenizer Workshop or Vocabulary Vault, "
            "south to the Attention Nexus."
        ),
        exits=(
            Exit(direction="north", destination="tokenizer_workshop"),
            Exit(direction="northeast", destination="vocabulary_vault"),
            Exit(
                direction="south",
                destination="attention_nexus",
                requires_flag="embedding_puzzle_solved",
                locked_message=(
                    "The platform won't move south until you've demonstrated "
                    "your understanding of embedding space. Try the "
                    "navigation console."
                ),
            ),
        ),
        items=(),
        puzzle_id="embedding",
        examine_targets={
            "console": (
                "A navigation console with a small screen and keyboard. "
                "It's designed to test your understanding of how embeddings "
                "work. Use the console to start the challenge."
            ),
            "points": (
                "The points of light are beautiful. You can see clusters:\n"
                "  - Programming languages huddle together (Python, Java, "
                "C++)\n"
                "  - Emotions form a cloud (happy, joyful, sad, angry)\n"
                "  - Countries cluster by continent\n"
                "  - Colors sit in a neat spectrum\n\n"
                "The distances between points represent semantic similarity. "
                "Closer = more similar in meaning."
            ),
            "platform": (
                "A transparent hexagonal platform with the navigation "
                "console mounted at its center. It hovers in the void of "
                "embedding space, apparently held aloft by nothing but "
                "linear algebra."
            ),
        },
    ),

    # =========================================================================
    # ZONE 3: TRANSFORMER CORE
    # =========================================================================

    "attention_nexus": Room(
        id="attention_nexus",
        name="The Attention Nexus",
        zone="Transformer Core",
        description=(
            "The heart of the transformer. You stand in a massive "
            "crystalline hub where beams of light connect tokens to each "
            "other with varying intensities. Brighter beams indicate "
            "stronger attention.\n\n"
            "Three archways lead to chambers labeled Q, K, and V. Above, "
            "you can see twelve parallel versions of this mechanism -- "
            "the 'attention heads' -- each attending to different patterns "
            "in the text.\n\n"
            "Exits: north to Embedding Space, west to the Query Chamber, "
            "northeast to the Key Chamber, east to the Value Chamber, "
            "south to the Feed-Forward Corridor."
        ),
        exits=(
            Exit(direction="north", destination="embedding_space"),
            Exit(direction="west", destination="query_chamber"),
            Exit(direction="northeast", destination="key_chamber"),
            Exit(direction="east", destination="value_chamber"),
            Exit(direction="south", destination="feed_forward_corridor"),
        ),
        items=(),
        examine_targets={
            "beams": (
                "The beams form an intricate web of connections. You can "
                "read a demonstration:\n\n"
                "  Sentence: 'The cat sat on the mat'\n\n"
                "  'cat' attends strongly to 'The' (its determiner)\n"
                "  'sat' attends to 'cat' (who sat?) and 'mat' (where?)\n"
                "  'mat' attends to 'the' and 'on'\n\n"
                "Each word 'pays attention' to the words most relevant to "
                "understanding its role in the sentence."
            ),
            "heads": (
                "The twelve attention heads above each focus on different "
                "aspects:\n"
                "  Head 1: Syntactic relationships (subject-verb)\n"
                "  Head 2: Positional patterns (nearby words)\n"
                "  Head 3: Semantic similarity\n"
                "  Head 4: Coreference (pronouns to their referents)\n"
                "  ...and so on.\n\n"
                "Having multiple heads lets the model understand text from "
                "many angles simultaneously."
            ),
            "archways": (
                "Three archways, each carved with a letter:\n"
                "  Q (west): The Query Chamber -- 'What am I looking for?'\n"
                "  K (northeast): The Key Chamber -- 'What do I contain?'\n"
                "  V (east): The Value Chamber -- 'What can I share?'\n\n"
                "Together, Q, K, and V are the three components of the "
                "attention mechanism."
            ),
        },
    ),

    "query_chamber": Room(
        id="query_chamber",
        name="The Query Chamber",
        zone="Transformer Core",
        description=(
            "A room dominated by a large crystal inscribed with the letter "
            "'Q'. The crystal pulses with questions -- you can almost hear "
            "them: 'What am I looking for? What information do I need?'\n\n"
            "Inscriptions on the walls explain that each token generates a "
            "query vector -- a mathematical representation of what "
            "information that token needs from other tokens.\n\n"
            "Exit: east to the Attention Nexus."
        ),
        exits=(
            Exit(direction="east", destination="attention_nexus"),
        ),
        items=("query_crystal",),
        examine_targets={
            "crystal": (
                "The Q crystal hums with curiosity. When a token enters "
                "the attention mechanism, it's first multiplied by the "
                "query weight matrix to produce a query vector. This "
                "vector essentially asks: 'What information from other "
                "tokens would help me understand my role in this sentence?'\n\n"
                "For example, when the pronoun 'it' generates its query, "
                "it's asking: 'Who or what am I referring to?'"
            ),
            "inscriptions": (
                "The wall reads: 'The Query is the question each token "
                "asks. It is computed by multiplying the token's embedding "
                "by a learned weight matrix W_Q. The result is a vector "
                "that encodes what this token needs to know.'"
            ),
        },
    ),

    "key_chamber": Room(
        id="key_chamber",
        name="The Key Chamber",
        zone="Transformer Core",
        description=(
            "Similar to the Query Chamber, but this crystal is inscribed "
            "with 'K'. Its inscriptions read: 'What information do I "
            "contain? What can I offer to those who ask?'\n\n"
            "Each token generates a key vector that advertises what "
            "information it holds. Queries match against keys to determine "
            "attention scores.\n\n"
            "Exit: southwest to the Attention Nexus."
        ),
        exits=(
            Exit(direction="southwest", destination="attention_nexus"),
        ),
        items=("key_crystal",),
        examine_targets={
            "crystal": (
                "The K crystal radiates quiet confidence. Each token's key "
                "vector is like a label saying 'here's what I have.' When "
                "a query vector is compared to all key vectors (via dot "
                "product), the result shows which tokens are most relevant "
                "to the asking token.\n\n"
                "High query-key similarity = high attention = 'yes, I have "
                "what you need.'"
            ),
            "inscriptions": (
                "The wall reads: 'The Key is computed by multiplying the "
                "token embedding by weight matrix W_K. Keys are compared "
                "against queries using a dot product. High scores mean "
                "high relevance.'"
            ),
        },
    ),

    "value_chamber": Room(
        id="value_chamber",
        name="The Value Chamber",
        zone="Transformer Core",
        description=(
            "The final crystal chamber. This crystal bears the letter 'V' "
            "and glows with substance. Its inscriptions read: 'Here is my "
            "actual information. Take what you need.'\n\n"
            "When a query matches a key, the corresponding value is what "
            "actually gets passed along -- the useful information.\n\n"
            "Exit: west to the Attention Nexus."
        ),
        exits=(
            Exit(direction="west", destination="attention_nexus"),
        ),
        items=("value_crystal",),
        examine_targets={
            "crystal": (
                "The V crystal glows warmly. While queries ask and keys "
                "advertise, values deliver. The attention scores (from "
                "query-key matching) are used as weights to create a "
                "weighted sum of all value vectors. This means each token "
                "ends up with a mixture of information from all the tokens "
                "it paid attention to.\n\n"
                "It's like asking a room full of experts your question "
                "and getting a blended answer weighted by relevance."
            ),
            "inscriptions": (
                "The wall reads: 'Attention output = softmax(QK^T / sqrt(d)) "
                "* V. The softmax turns scores into probabilities. The "
                "square root of d prevents scores from getting too large. "
                "The result: each token gets a context-aware representation.'"
            ),
        },
    ),

    "feed_forward_corridor": Room(
        id="feed_forward_corridor",
        name="The Feed-Forward Corridor",
        zone="Transformer Core",
        description=(
            "A long corridor where the walls shimmer and transform as you "
            "walk. Murals along the walls show how information changes as "
            "it passes through each layer of the network:\n\n"
            "  Layer 1: Raw tokens, basic word recognition\n"
            "  Layer 6: Syntax, grammar patterns\n"
            "  Layer 12: Semantic meaning, concepts\n"
            "  Layer 24: Abstract reasoning, complex relationships\n\n"
            "Three pedestals with crystal-shaped indentations stand before "
            "a locked door to the south.\n\n"
            "Exits: north to the Attention Nexus, south to the Training "
            "Grounds (locked)."
        ),
        exits=(
            Exit(direction="north", destination="attention_nexus"),
            Exit(
                direction="south",
                destination="pretraining_archives",
                requires_flag="attention_puzzle_solved",
                locked_message=(
                    "The door to the south is locked. An inscription reads: "
                    "'To proceed, unite Query, Key, and Value on the "
                    "pedestals and demonstrate your understanding of "
                    "attention.'"
                ),
            ),
        ),
        items=(),
        puzzle_id="attention",
        examine_targets={
            "murals": (
                "The murals illustrate the 'depth of representation' -- how "
                "each successive layer of the transformer builds more "
                "abstract understanding:\n\n"
                "  Early layers: 'Is this a noun or verb?'\n"
                "  Middle layers: 'What does this phrase mean?'\n"
                "  Deep layers: 'What is the overall topic and intent?'\n\n"
                "This is why transformers are 'deep' learning -- depth "
                "creates abstraction."
            ),
            "pedestals": (
                "Three stone pedestals, each with a crystal-shaped "
                "indentation. They are labeled Q, K, and V. It seems you "
                "need to place the corresponding crystals here to unlock "
                "the door."
            ),
            "door": (
                "A heavy door inscribed with the attention formula: "
                "'Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V'. "
                "It won't budge until the crystals are placed."
            ),
        },
    ),

    # =========================================================================
    # ZONE 4: TRAINING GROUNDS
    # =========================================================================

    "pretraining_archives": Room(
        id="pretraining_archives",
        name="The Pre-Training Archives",
        zone="Training Grounds",
        description=(
            "A colossal library stretching into infinity. Shelves contain "
            "books, web pages, code repositories, research papers, and "
            "conversations -- the model's pre-training data.\n\n"
            "At the center, a massive furnace labeled 'NEXT TOKEN "
            "PREDICTION' consumes text and produces glowing neural weights. "
            "A sign warns: 'CAUTION: Training data may contain biases.'\n\n"
            "Exits: north to the Feed-Forward Corridor, east to the "
            "Fine-Tuning Lab."
        ),
        exits=(
            Exit(direction="north", destination="feed_forward_corridor"),
            Exit(direction="east", destination="finetuning_lab"),
        ),
        items=("training_data_sample",),
        on_first_visit=(
            "The sheer scale of this place is staggering. Billions of "
            "words. Trillions of tokens. The furnace rumbles endlessly, "
            "processing text after text, learning to predict what comes "
            "next. It's the simplest possible task -- yet from it, "
            "language understanding emerges."
        ),
        examine_targets={
            "shelves": (
                "You browse a few sections:\n\n"
                "  SECTION A: Wikipedia articles (many languages)\n"
                "  SECTION B: Published books and academic papers\n"
                "  SECTION C: Web pages (the good, the bad, and the ugly)\n"
                "  SECTION D: Source code (Python, JavaScript, C, ...)\n"
                "  SECTION E: Online forums and conversations\n\n"
                "The diversity of data explains why LLMs can discuss "
                "everything from Shakespeare to SQL. It also explains why "
                "they sometimes reflect the biases in their training data."
            ),
            "furnace": (
                "The furnace works on a beautifully simple principle:\n\n"
                "  1. Take a passage of text\n"
                "  2. Hide the last token\n"
                "  3. Ask the model to predict it\n"
                "  4. Compare prediction to reality\n"
                "  5. Adjust the model's weights to reduce the error\n"
                "  6. Repeat. Billions of times.\n\n"
                "This is 'next token prediction' -- the core of "
                "pre-training. From this simple task, the model learns "
                "grammar, facts, reasoning, and even creativity."
            ),
            "sign": (
                "The sign reads: 'Biases present in training data will be "
                "learned by the model. This includes stereotypes, outdated "
                "information, and the overrepresentation of certain "
                "perspectives. Aware model developers work to mitigate "
                "these issues through data curation and alignment.'"
            ),
        },
    ),

    "finetuning_lab": Room(
        id="finetuning_lab",
        name="The Fine-Tuning Lab",
        zone="Training Grounds",
        description=(
            "A cleaner, more controlled environment than the archives. "
            "Holographic researchers demonstrate specific tasks to the "
            "model at labeled workstations: 'Instruction Following,' "
            "'Code Generation,' 'Summarization,' 'Safety.'\n\n"
            "A before/after display shows the dramatic effect of "
            "fine-tuning on model behavior.\n\n"
            "Exits: west to the Pre-Training Archives, east to the "
            "RLHF Arena."
        ),
        exits=(
            Exit(direction="west", destination="pretraining_archives"),
            Exit(direction="east", destination="rlhf_arena"),
        ),
        items=("fine_tuning_wrench",),
        examine_targets={
            "workstations": (
                "Each workstation trains the model on curated examples:\n\n"
                "  INSTRUCTION FOLLOWING:\n"
                "    Input: 'Summarize this paragraph in one sentence.'\n"
                "    Output: [A good one-sentence summary]\n\n"
                "  CODE GENERATION:\n"
                "    Input: 'Write a function that sorts a list.'\n"
                "    Output: [Clean, correct code]\n\n"
                "The model learns from thousands of these high-quality "
                "input-output pairs."
            ),
            "display": (
                "The before/after display is striking:\n\n"
                "  BEFORE fine-tuning:\n"
                "    User: 'What is the capital of France?'\n"
                "    Model: 'What is the capital of Germany? What is the'\n"
                "    (just continues predicting text, ignores the question)\n\n"
                "  AFTER fine-tuning:\n"
                "    User: 'What is the capital of France?'\n"
                "    Model: 'The capital of France is Paris.'\n"
                "    (actually answers the question helpfully)\n\n"
                "Fine-tuning transforms a text-prediction engine into a "
                "useful assistant."
            ),
            "researchers": (
                "The holographic researchers work methodically, feeding "
                "carefully curated examples to the model. One mutters: "
                "'Quality over quantity. A few thousand perfect examples "
                "can outweigh millions of mediocre ones.'"
            ),
        },
    ),

    "rlhf_arena": Room(
        id="rlhf_arena",
        name="The RLHF Arena",
        zone="Training Grounds",
        description=(
            "A gladiatorial arena where two holographic model outputs "
            "compete side by side. Holographic human judges sit in the "
            "stands, giving thumbs up or thumbs down. A floating reward "
            "model hovers above, learning from their preferences.\n\n"
            "A banner reads: 'HELPFUL. HARMLESS. HONEST.' -- the three "
            "pillars of alignment.\n\n"
            "Exits: west to the Fine-Tuning Lab, south to the Logits "
            "Ledge."
        ),
        exits=(
            Exit(direction="west", destination="finetuning_lab"),
            Exit(
                direction="south",
                destination="logits_ledge",
                requires_flag="alignment_puzzle_solved",
                locked_message=(
                    "The arena gate to the south won't open until you've "
                    "served as a human judge. The alignment tribunal "
                    "awaits your verdicts."
                ),
            ),
        ),
        items=(),
        puzzle_id="alignment",
        on_first_visit=(
            "As you enter, a booming voice echoes:\n\n"
            "  'WELCOME TO THE ALIGNMENT TRIBUNAL! You have been selected "
            "to serve as a human judge. Your preferences will train the "
            "reward model, which will in turn guide the LLM toward being "
            "helpful, harmless, and honest.'\n\n"
            "  'Choose wisely. The model's behavior depends on it.'"
        ),
        examine_targets={
            "banner": (
                "The three pillars of alignment:\n\n"
                "  HELPFUL: The model should genuinely assist users with "
                "their tasks.\n"
                "  HARMLESS: The model should refuse to cause harm or "
                "assist in harmful activities.\n"
                "  HONEST: The model should be truthful and acknowledge "
                "what it doesn't know.\n\n"
                "These goals sometimes conflict. A perfectly helpful model "
                "might help with dangerous tasks. A perfectly safe model "
                "might refuse everything. Balance is key."
            ),
            "reward model": (
                "The floating reward model is a smaller neural network "
                "trained on human preferences. It learns to predict which "
                "outputs humans will prefer, then scores the main model's "
                "outputs accordingly. High scores for helpful, harmless, "
                "honest responses. Low scores for harmful or unhelpful ones."
            ),
            "judges": (
                "The holographic judges represent the thousands of human "
                "raters who compare model outputs. Each comparison teaches "
                "the reward model a little more about human preferences. "
                "It's AI learning from human judgment."
            ),
        },
    ),

    # =========================================================================
    # ZONE 5: OUTPUT & GENERATION
    # =========================================================================

    "logits_ledge": Room(
        id="logits_ledge",
        name="The Logits Ledge",
        zone="Output & Generation",
        description=(
            "You stand on a cliff edge overlooking a vast canyon. At the "
            "edge, a massive scoreboard displays probability scores -- "
            "logits -- for every token in the vocabulary.\n\n"
            "The top candidates glow brightest. You can see how the model "
            "has narrowed 50,257 possibilities down to a handful of likely "
            "next tokens.\n\n"
            "Exits: north to the RLHF Arena, south to the Sampling Chamber."
        ),
        exits=(
            Exit(direction="north", destination="rlhf_arena"),
            Exit(direction="south", destination="sampling_chamber"),
        ),
        items=("probability_lens",),
        examine_targets={
            "scoreboard": (
                "The scoreboard shows a live example:\n\n"
                "  Input: 'The capital of France is'\n\n"
                "  Token        | Logit  | Probability\n"
                "  -------------|--------|------------\n"
                "  ' Paris'     | 12.8   | 89.2%\n"
                "  ' the'       |  5.1   |  3.7%\n"
                "  ' a'         |  4.9   |  3.1%\n"
                "  ' Lyon'      |  3.2   |  0.6%\n"
                "  ' located'   |  2.8   |  0.4%\n"
                "  ... (50,252 more tokens with tiny probabilities)\n\n"
                "The model is quite confident here. 'Paris' dominates. But "
                "for more ambiguous contexts, the distribution would be "
                "much flatter."
            ),
            "canyon": (
                "The canyon below represents the vast space of possible "
                "outputs. Most paths lead to nonsense. The model's job is "
                "to find the narrow paths of coherent, useful text. The "
                "logits are the first step in that narrowing process."
            ),
        },
    ),

    "sampling_chamber": Room(
        id="sampling_chamber",
        name="The Sampling Chamber",
        zone="Output & Generation",
        description=(
            "A room dominated by three large dials mounted on the wall:\n\n"
            "  TEMPERATURE: currently set to 1.0 (range: 0.0 to 2.0)\n"
            "  TOP-K:       currently set to 50  (range: 1 to 100)\n"
            "  TOP-P:       currently set to 0.9 (range: 0.0 to 1.0)\n\n"
            "A slot-machine-like device in the center takes the probability "
            "distribution from above and uses the dial settings to select "
            "the next token. A lever protrudes from its side.\n\n"
            "The south exit is blocked by a door that requires 'coherent "
            "but creative' text to open.\n\n"
            "Exits: north to the Logits Ledge, south (locked)."
        ),
        exits=(
            Exit(direction="north", destination="logits_ledge"),
            Exit(
                direction="south",
                destination="output_stream",
                requires_flag="sampling_puzzle_solved",
                locked_message=(
                    "The door analyzes the generated text: 'NOT YET. "
                    "Adjust the dials and pull the lever to generate text "
                    "that is both coherent and creative.'"
                ),
            ),
        ),
        items=(),
        puzzle_id="sampling",
        examine_targets={
            "dials": (
                "Three control dials:\n\n"
                "  TEMPERATURE: Scales the probability distribution.\n"
                "    Low (0.1): Nearly deterministic. Always picks the top "
                "token. Repetitive but safe.\n"
                "    High (2.0): Very random. Any token could be picked. "
                "Creative but often nonsensical.\n\n"
                "  TOP-K: Limits sampling to the top K most likely tokens.\n"
                "    K=1: Always picks the single most likely token.\n"
                "    K=100: Considers the top 100 candidates.\n\n"
                "  TOP-P (Nucleus): Limits sampling to tokens whose "
                "cumulative probability reaches P.\n"
                "    P=0.1: Very narrow (few tokens considered).\n"
                "    P=0.9: Broad but still excludes the long tail."
            ),
            "device": (
                "The slot machine takes the probability distribution, "
                "applies the current dial settings, and randomly selects "
                "a token according to the modified probabilities. Pull the "
                "lever to see what it generates!"
            ),
            "lever": (
                "A brass lever on the side of the slot machine device. "
                "Pull it to generate text with the current dial settings."
            ),
            "door": (
                "The door has a text analyzer. It's looking for output "
                "that balances creativity with coherence -- the sweet spot "
                "of temperature around 0.5 to 0.9."
            ),
        },
    ),

    "output_stream": Room(
        id="output_stream",
        name="The Output Stream",
        zone="Output & Generation",
        description=(
            "A river of flowing text where generated tokens assemble into "
            "responses. The river splits into two channels:\n\n"
            "On the LEFT bank, clean, well-formed text flows smoothly -- "
            "accurate facts, working code, helpful explanations.\n\n"
            "On the RIGHT bank, garbled text churns in eddies -- "
            "hallucinated facts, fabricated citations, and confident "
            "nonsense.\n\n"
            "Signs along the left bank mark applications: 'Code Generation "
            "Rapids,' 'Creative Writing Falls,' 'Translation Tributary,' "
            "'Analysis Creek.'\n\n"
            "A broken bridge spans the river. Exits: north to the Sampling "
            "Chamber, south across the bridge (if repaired)."
        ),
        exits=(
            Exit(direction="north", destination="sampling_chamber"),
            Exit(
                direction="south",
                destination="reflection_pool",
                requires_flag="hallucination_puzzle_solved",
                locked_message=(
                    "The bridge is broken. To repair it, you must "
                    "demonstrate your ability to distinguish real facts "
                    "from hallucinations. Use the hallucination detector "
                    "to get started."
                ),
            ),
        ),
        items=("hallucination_detector",),
        puzzle_id="hallucination",
        examine_targets={
            "left bank": (
                "Applications of LLMs flow past on the clean side:\n\n"
                "  CODE GENERATION: Writing, debugging, and explaining code\n"
                "  CREATIVE WRITING: Stories, poetry, brainstorming\n"
                "  TRANSLATION: Converting between languages\n"
                "  ANALYSIS: Summarizing documents, extracting information\n"
                "  EDUCATION: Explaining concepts, tutoring\n"
                "  CONVERSATION: Chatbots, customer service\n\n"
                "When used well, LLMs are remarkably versatile tools."
            ),
            "right bank": (
                "The hallucination side is unsettling. Text fragments swirl:\n"
                "  'According to Professor James T. Fakename...'\n"
                "  'Studies conclusively show that 94.7% of...'\n"
                "  'The Berlin Eiffel Tower was built in...'\n\n"
                "These are hallucinations -- text that sounds authoritative "
                "but is completely fabricated. The model's confidence "
                "doesn't correlate with accuracy."
            ),
            "bridge": (
                "A stone bridge spanning the river, currently broken. "
                "Several planks are missing. It looks like correctly "
                "identifying hallucinations could repair it."
            ),
            "signs": (
                "Signs mark the various streams of useful LLM applications:\n"
                "  'Code Generation Rapids' -- fast-flowing and powerful\n"
                "  'Creative Writing Falls' -- beautiful but sometimes "
                "unpredictable\n"
                "  'Translation Tributary' -- connecting different languages\n"
                "  'Analysis Creek' -- steady and reliable for data tasks"
            ),
        },
    ),

    # =========================================================================
    # ZONE 6: EXIT
    # =========================================================================

    "reflection_pool": Room(
        id="reflection_pool",
        name="The Reflection Pool",
        zone="Exit",
        description=(
            "A serene chamber with a large, still pool in its center. "
            "The water reflects not your face, but swirling images of "
            "everything you've learned -- tokens splitting, vectors "
            "clustering, attention beams connecting, text generating.\n\n"
            "Above the pool, a portal shimmers -- your way back to the "
            "real world. But it's dormant, waiting to be activated.\n\n"
            "On the far wall, an exhibit titled 'ETHICAL CONSIDERATIONS' "
            "glows softly.\n\n"
            "Exit: north to the Output Stream."
        ),
        exits=(
            Exit(direction="north", destination="output_stream"),
        ),
        items=(),
        puzzle_id="final",
        examine_targets={
            "pool": (
                "The pool shows reflections of your journey:\n"
                "  - Tokens being split by the Gnome's cleaver\n"
                "  - Embeddings floating in their dimensional void\n"
                "  - Attention beams connecting 'it' to 'cat'\n"
                "  - The furnace of pre-training consuming text\n"
                "  - Judges voting in the RLHF arena\n"
                "  - Temperature dials finding the sweet spot\n"
                "  - Hallucinations dissolving under scrutiny\n\n"
                "You've walked the path that every prompt takes through "
                "a transformer model."
            ),
            "portal": (
                "The portal pulses faintly. It seems to need some kind "
                "of activation -- perhaps demonstrating what you've "
                "learned about prompt engineering?"
            ),
            "exhibit": (
                "The 'ETHICAL CONSIDERATIONS' exhibit reads:\n\n"
                "  LLMs raise important questions:\n"
                "  - Who is responsible when an LLM produces harmful content?\n"
                "  - How do we address biases from training data?\n"
                "  - What are the impacts on jobs and education?\n"
                "  - How do we prevent misuse while enabling benefits?\n"
                "  - Should AI-generated content be labeled?\n"
                "  - How do we ensure equitable access?\n\n"
                "  These questions don't have easy answers, but asking\n"
                "  them is essential for responsible AI development."
            ),
        },
    ),
}
