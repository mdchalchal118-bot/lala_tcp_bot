BUNDLE_MAP = {
    "rampage": 914000002,
    "werewolf": 914000003,
    "devil": 914038001,
    "scorpio": 914039001,
    "frostfire": 914042001,
    "paradox": 914044001,
    "naruto": 914047001,
    "aurora": 914047002,
    "midnight": 914048001,
    "itachi": 914050001,
    "dreamspace": 914051001,
    "eclipse": 914053001
}

def get_bundle_menu(signature):
    return f"""[C][B][FF0000]─── Available Bundles ───
[FFFFFF] 1 > Rampage
[FFFFFF] 2 > Werewolf
[FFFFFF] 3 > Devil
[FFFFFF] 4 > Scorpio
[FFFFFF] 5 > Frostfire
[FFFFFF] 6 > Paradox
[FFFFFF] 7 > Naruto
[FFFFFF] 8 > Aurora
[FFFFFF] 9 > Midnight
[FFFFFF] 10 > Itachi
[FFFFFF] 11 > Dreamspace
[FFFFFF] 12 > Eclipse
[FF0000]────────────
[00FF00]Usage: /bundle [name]
[FFFFFF]Example: /bundle dreamspace
[FF0000]────────────
{signature}
[FF0000]────────────"""