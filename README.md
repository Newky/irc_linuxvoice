IRC Linuxvoice Example
----------------------

This repository holds the code that was used in the Linux Voice article
written by me on the IRC protocol.

This has got a single file called "client.py" which is an irc client.

Its quite minimal and uses only raw python sockets to talk to IRC.

It is open for extension by adding more commands to the COMMANDS dictionary.

I encourage any pull requests or forks and look forward to seeing a plethora
of IRC bots in #linuxvoice.

client.py is pretty well commented so its likely best to just read the source.

Additionally running `python client.py --help` will show more information on
the arguments you can pass.

Some small things I recommend trying:
- Adding a more sophisticated `priv_msg_responder` function.
- Making it so that the bot does not greet himself when he joins.
