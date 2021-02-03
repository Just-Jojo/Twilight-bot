# Twilight bot

---

A Discord bot created by Jojo#7791, Twilight is a functional (suuuure) Discord bot designed for the My Little Pony community (Sorry, Twilight readers, this isn't Bella :p).

### Features
- [x] A working Moderation set up using JSON files to store data
- [ ] An Episode search feature (Dang you, episodes)
- [ ] A working character search feature
- [x] Fun cogs
- [ ] An economy (dunno if it'll be global or not just yet)

### Support

For support, please either DM Jojo on Discord (username is Jojo#7791, just shoot me a friend requst and say you're here for Twilight) or join [the support server](https://discord.gg/JmCFyq7) and go to `support-jojocogs`


#### Thanks for checking out Twilight!


# Running the bot yourself
Whilst I would perfer you not run Twilight on your own I will give you the tools to do so.

1. Make sure you have Python 3.8 installed
You need this to... run it
2. Set up a virtual env
`py -m venv .venv`
3. Install the requirements
`pip install -U -r requirements.txt`
4. Create a twi_secrets.py file
This should include the token, long traceback (can be any message), temp database, settings.json path, blocklist_path, and cogs path.

settings.json should be in the `cogs` folder, blocklist and cogs should be in the `bot` folder
5. This isn't really necessary but if you're on windows (which this was designed to be ran on)
Create a `.bat` file. This will catch the error level that `launcher.py` raises on exit and allows for auto restart.
#### Thanks kindly!
