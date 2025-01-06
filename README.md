# DinnerParty
Server-Client Code that executes and terminates audio files across clients. Made with ChatGPT for a suprise murder mystry dinner party event.

## Dependancies

`pip install pydub simpleaudio`

Note: `pydub` has an unmaintained library `pyaudioop` which segfaults after playing the audio if using Python version 3.12 or higher. 

Requires audio files of same type (i.e. mp3, m4a, etc.) to be downloaded in the same folder as client side code. 

Not tested outside of a local network, use at your own discretion.

## Quick Start

0. replace mutual audio file names in server.py lines 42-51 with actual names of audio files using. Determine if the song should loop with True or not to loop with False. Also replace the format to the one using in client.py line 19 (i.e. "m4a" or "mp3").

1. run server `python server.py server` 

2. connect clients (order of which they are connected is how they are assigned identifiers - 1, 2, 3, etc.) `python client.py client 127.0.0.1` replace 127.0.0.1 with ip address of server.

3. using key bindings a-j, and clients 1-N, play a song on one or multiple clients through keyboard input on server.py program. i.e. `12a` runs song `a` on clients 1 and 2. To stop the song mid-playthrough on both clients, enter `12s` to stop the song from looping enter `12a` again. 

