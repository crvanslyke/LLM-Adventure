"""Help messages, intro/outro text, and command reference."""

INTRO_TEXT = """\
==============================================================================

     L   L   M       A   D   V   E   N   T   U   R   E
     ___________________________________________________

     A Journey Inside a Large Language Model

==============================================================================

The year is 2025. You are a researcher at the Neural Frontiers Institute.
After years of studying LLMs from the outside, you've volunteered for an
experimental procedure: digitization and injection into the interior of a
large language model.

"Think of it like a fantastic voyage," said Dr. Chen, adjusting the
headset on your temples. "But instead of a submarine in a bloodstream,
you'll be walking through the layers of a transformer. Every room you
enter represents a key component of how the model processes language."

"And the way out?" you asked.

Dr. Chen smiled. "Learn enough about how it all works, and you'll find
your way to the exit portal. We've placed items and puzzles throughout
the architecture to help you learn. Oh, and we've added a scoring system
because, well, we're researchers. We measure everything."

The machine hummed. The world dissolved into vectors.

You materialized inside the model.

Type 'help' for a list of commands, or 'look' to examine your surroundings.
"""

HELP_TEXT = """\
==============================================================================
  COMMANDS
==============================================================================

  MOVEMENT:    go north (or just: north, n, s, e, w)
  LOOK:        look (or: l) -- describe your surroundings
  EXAMINE:     examine <thing> (or: x <thing>) -- look closely at something
  TAKE:        take <item> (or: get, grab, pick up)
  DROP:        drop <item> (or: put down)
  INVENTORY:   inventory (or: i) -- see what you're carrying
  USE:         use <item> -- use an item
               use <item> on <target> -- use an item on something
  TALK:        talk to <character> -- speak with someone
  PLACE:       place <item> on <target> -- put an item somewhere specific

  PUZZLE COMMANDS (available in puzzle rooms):
  CHOOSE:      choose <A/B/C/D> -- select an answer
  SET:         set <dial> <value> -- adjust a setting
  PULL:        pull lever -- activate a mechanism
  TAG:         tag <number> <real/hallucination> -- classify a statement

  INFO:
  JOURNAL:     journal (or: j) -- review your knowledge journal
  SCORE:       score -- check your score and rank
  HINT:        hint -- get a context-sensitive hint
  HELP:        help (or: h, ?) -- show this message
  ABOUT:       about -- credits and info

  SAVE/LOAD:
  SAVE:        save -- save your progress
  LOAD:        load (or: restore) -- restore a saved game

  QUIT:        quit (or: q) -- exit the game
"""

ABOUT_TEXT = """\
==============================================================================
  LLM ADVENTURE
==============================================================================

  A text-based adventure game about Large Language Models.
  Inspired by Colossal Cave Adventure (1976).

  Explore the inner workings of an LLM, solve puzzles that teach key
  concepts, and find your way back to the real world.

  Created with Python. No external dependencies. No actual LLMs were
  harmed in the making of this game (though several were consulted).
"""

OUTRO_TEXT = """\
==============================================================================

The portal blazes to life, a swirling vortex of pure information. You
feel your digital form dissolving, your consciousness uploading back
through the layers you traversed.

Embedding space folds. Attention weights release. Tokens reassemble
into meaning.

You open your eyes. Dr. Chen is smiling.

"Welcome back. Tell me -- what did you learn in there?"

You hand over your journal. Every concept, from tokenization to
temperature, from attention mechanisms to alignment, documented and
understood. Dr. Chen flips through it, nodding.

"Not bad," she says. "Not bad at all."

==============================================================================
  FINAL SCORE
==============================================================================
"""

UNKNOWN_COMMANDS = [
    "I don't understand that. Type 'help' for a list of commands.",
    "That's not something you can do. Try 'help' for options.",
    "Hmm, that doesn't compute. Type 'help' if you're stuck.",
    "The model doesn't recognize that input. Try 'help'.",
    "Unknown command. Perhaps 'help' would be... helpful?",
    "Your tokens have been dropped. Just kidding -- type 'help'.",
]
