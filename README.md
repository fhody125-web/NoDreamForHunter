i just want to play coop with my friends, why should my shadnet server depend on the hunters dream server!?

# NoDreamForHunter

Matchmaking requests → gets redirected to your real Shadnet server (the one you actually want to use for co‑op).

Everything else (random API calls) → gets a fake 200 OK or a static JSON response so the game stops complaining about being offline.

Basically, the game thinks it's fully online, but only matchmaking actually goes anywhere useful. All other online features (messages, ghosts, etc) aren't implemented, and this server doesn't pretend otherwise, it just returns garbage that keeps the game happy.

# Getting it running

1-Download NoDreamForHunter.exe and real_ss_info.txt from Releases.

2-Open real_ss_info.txt and replace {YOUR SHADNET SERVER} with the IP of your actual Shadnet server. Save it. Must be in the same folder as the .exe or py file.

3-Edit shadPS4's host_overrides.json to this:

{ "https://ss4.scej-network.jp:20443" : "http://127.0.0.1" }

4-Run NoDreamForHunter.exe or if you have python, run.py. A console window pops up – that's it.

Launch Bloodborne. You'll see "online" in‑game. Invite your friends, ring your bells, and co‑op should work if your real Shadnet server is up.

# Note
This is poorly made – I threw it together in an afternoon so my friends and I could play. No error handling, no logging worth a damn, no multi‑threading. It works on my machine™.

Contributing If you want to improve this mess, feel free to fork and PR. Just know that the code is held together with duct tape and spite – I won't judge your hacky fixes.

License MIT, because who cares.
