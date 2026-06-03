# ============================================================
#  config.py  —  Clap-to-Open Website Settings
# ============================================================

# --- Website to open ---
WEBSITES = {
    1: "https://www.youtube.com",    # Single clap
    2: "https://www.google.com",     # Double clap
    3: "https://www.github.com",     # Triple clap
}

# --- Microphone / Audio Settings ---
SAMPLE_RATE      = 44100   # Hz  (standard mic rate)
CHUNK_SIZE       = 512    # Samples per audio chunk
CHANNELS         = 1       # Mono mic input

# --- Clap Detection Sensitivity ---
CLAP_THRESHOLD   = 2500    # Volume level to count as a clap
                            # Lower = more sensitive (picks up soft claps)
                            # Higher = less sensitive (needs louder claps)

# --- Timing Settings ---
CLAP_WINDOW      = 1.5     # Seconds to wait for multiple claps
COOLDOWN_TIME    = 1.0     # Seconds to ignore sound after opening a site
MIN_CLAP_GAP     = 0.15    # Minimum seconds between two clap spikes
