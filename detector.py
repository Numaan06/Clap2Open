# ============================================================
#  detector.py  —  Clap Detection Logic
# ============================================================

import numpy as np
import time
from config import CLAP_THRESHOLD, CLAP_WINDOW, MIN_CLAP_GAP


class ClapDetector:
    """
    Detects claps by watching for sudden loud spikes in audio.
    Tracks how many claps happen within a short time window.
    """

    def __init__(self):
        self.clap_times = []          # Timestamps of recent claps
        self.last_spike_time = 0      # Time of last detected spike (debounce)

    def process_chunk(self, audio_data: bytes) -> int:
        """
        Feed one raw audio chunk.
        Returns:
          0  — no new clap pattern yet
          1  — single clap confirmed
          2  — double clap confirmed
          3  — triple clap confirmed
        """
        volume = self._get_volume(audio_data)

        now = time.time()

        # ---- Spike detection (with debounce) ----
        if volume > CLAP_THRESHOLD:
            if now - self.last_spike_time >= MIN_CLAP_GAP:
                self.clap_times.append(now)
                self.last_spike_time = now
                print(f"   👏  Clap spike!  volume={int(volume)}")

        # ---- Remove claps outside the time window ----
        self.clap_times = [t for t in self.clap_times if now - t <= CLAP_WINDOW]

        # ---- Wait until there is a brief pause before deciding ----
        if len(self.clap_times) >= 1:
            last_clap_age = now - self.clap_times[-1]
            if last_clap_age > 0.15:                     # 0.45 s silence = done clapping
                count = len(self.clap_times)
                self.clap_times.clear()
                return min(count, 3)                     # Cap at 3

        return 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_volume(audio_data: bytes) -> float:
        """Convert raw PCM bytes → RMS amplitude."""
        samples = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        if len(samples) == 0:
            return 0.0
        rms = np.sqrt(np.mean(samples ** 2))
        return rms
