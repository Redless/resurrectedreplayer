# What is this?

This is a Pokemon log-to-replay converter. I made it in 5 hours for a youtuber I like, BKC. I don't maintain it and I'm not proud of the style (it's spaghetti code) so if you're an employer reading this, understand that.

# What I did

Created a script to automate M Dragon vs Floppy. All the stuff that happens in that match (spikes, sleep, toxic, stat raising/lowering, sandstorm, leftovers, moves doing damage) is implemented in the script, so it was able to parse that log into a replay.

# Stuff I didn't implement

-   "missing" doesn't use a different animation
-   "sandstorm" is not animated
-   all the chats and talk of people joining/leaving the battle. I don't care about this stuff.
-   fixed the weird speedup on turn 13ish

# Stuff that's impossible to implement

-   Getting rid of the rounding errors. Sorry.
-   Gender
-   Switching avatar to something other than roughneck-gen4, I promise

# What to do next

-   Do a similar process for other logs that BKC wants turned into replays, expanding this script each time to cover whatever mechanics in those battles it doesn't already implement
