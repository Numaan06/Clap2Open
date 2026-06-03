# ============================================================
#  main.py  —  Clap-to-Open Website  (Main Entry Point)
# ============================================================

import pyaudio
import webbrowser
import time
import sys

from detector import ClapDetector
from config import (
    SAMPLE_RATE, CHUNK_SIZE, CHANNELS,
    WEBSITES, COOLDOWN_TIME
)


# ── Colour helpers (work on Windows/Mac/Linux terminals) ─────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"


def banner():
    print(f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════╗
  ║        👏  CLAP TO OPEN WEBSITE  👏      ║
  ╚══════════════════════════════════════════╝
{RESET}
  {YELLOW}Single clap (1){RESET}  →  {WEBSITES[1]}
  {YELLOW}Double clap (2){RESET}  →  {WEBSITES[2]}
  {YELLOW}Triple clap (3){RESET}  →  {WEBSITES[3]}

  Press  {BOLD}Ctrl + C{RESET}  to quit.
""")


def open_website(clap_count: int):
    url = WEBSITES.get(clap_count)
    if url:
        print(f"\n  {GREEN}{BOLD}✅  {clap_count} clap(s) detected!  Opening → {url}{RESET}\n")
        webbrowser.open(url)
    else:
        print(f"  {RED}No website configured for {clap_count} clap(s).{RESET}")


def list_microphones():
    """Print all available input devices so the user can pick one."""
    p = pyaudio.PyAudio()
    print(f"\n{CYAN}Available microphones:{RESET}")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"  [{i}] {info['name']}")
    p.terminate()


def get_default_input_device():
    p = pyaudio.PyAudio()
    try:
        idx = p.get_default_input_device_info()["index"]
    except OSError:
        idx = None
    p.terminate()
    return idx


def run():
    banner()

    # --- Check microphone availability ---
    device_index = get_default_input_device()
    if device_index is None:
        print(f"{RED}❌  No microphone found. Please connect a mic and retry.{RESET}")
        list_microphones()
        sys.exit(1)

    print(f"  {CYAN}🎙️  Listening on microphone (device {device_index})…{RESET}\n")

    detector    = ClapDetector()
    pa          = pyaudio.PyAudio()
    cooldown_until = 0          # Timestamp until which we ignore detections

    stream = pa.open(
        format            = pyaudio.paInt16,
        channels          = CHANNELS,
        rate              = SAMPLE_RATE,
        input             = True,
        input_device_index= device_index,
        frames_per_buffer = CHUNK_SIZE,
    )

    try:
        while True:
            # Read one chunk of audio
            try:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            except OSError as e:
                print(f"{RED}Audio read error: {e}{RESET}")
                continue

            # Skip processing during cooldown
            if time.time() < cooldown_until:
                continue

            # Run clap detection
            clap_count = detector.process_chunk(data)

            if clap_count > 0:
                open_website(clap_count)
                cooldown_until = time.time() + COOLDOWN_TIME

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}👋  Stopped. Goodbye!{RESET}\n")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


# ── Entry point ───────────────────────────────────────────────────────
if __name__ == "__main__":
    # Optional flag: --list-mics
    if "--list-mics" in sys.argv:
        list_microphones()
    else:
        run()
