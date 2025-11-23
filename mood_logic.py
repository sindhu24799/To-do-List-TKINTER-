MOOD_MAP = {
    "happy": ["goals", "learning", "creative"],
    "stressed": ["simple", "quick", "chores"],
    "tired": ["light", "fun"],
    "sad": ["selfcare", "comfort"]
}


def suggest_categories(mood):
    return MOOD_MAP.get(mood, [])
