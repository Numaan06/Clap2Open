👏 Clap-to-Open Website
Clap your hands → Python detects it → website opens automatically in your browser!

📁 Project Files
clap-opener/
├── main.py           ← Run this file
├── detector.py       ← Clap detection brain
├── config.py         ← Your settings (URLs, sensitivity)
└── requirements.txt  ← Libraries to install

⚙️ Setup (One Time)
1. Install Python
Download Python 3.8+ from https://www.python.org/downloads/
2. Install libraries
Windows:
bashpip install pyaudio numpy
Mac:
bashbrew install portaudio
pip install pyaudio numpy
Linux (Ubuntu/Debian):
bashsudo apt-get install python3-pyaudio portaudio19-dev
pip install numpy

▶️ Run the Project
bashpython main.py
You will see:
  ╔══════════════════════════════════════════╗
  ║        👏  CLAP TO OPEN WEBSITE  👏      ║
  ╚══════════════════════════════════════════╝

  Single clap (1)  →  https://www.youtube.com
  Double clap (2)  →  https://www.google.com
  Triple clap (3)  →  https://www.github.com
Now clap your hands and watch the magic! 🎉

✏️ Change Websites
Open config.py and edit the WEBSITES dictionary:
pythonWEBSITES = {
    1: "https://www.youtube.com",   # 1 clap opens this
    2: "https://www.google.com",    # 2 claps opens this
    3: "https://www.github.com",    # 3 claps opens this
}

🎚️ Adjust Sensitivity
In config.py, change CLAP_THRESHOLD:
pythonCLAP_THRESHOLD = 2500   # Default
# Lower number  = more sensitive (soft claps work)
# Higher number = less sensitive (needs loud claps)

🔍 List Your Microphones
bashpython main.py --list-mics

❌ Stop the Program
Press Ctrl + C in the terminal.

🛠️ Troubleshooting
ProblemFixNo microphone foundCheck mic is plugged in / enabledFalse triggers (noise opens sites)Increase CLAP_THRESHOLD in config.pyClaps not detectedDecrease CLAP_THRESHOLD in config.pypyaudio install error on MacRun brew install portaudio firstpyaudio install error on LinuxRun sudo apt-get install portaudio19-dev first
