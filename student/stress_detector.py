LOW_STRESS_KEYWORDS = [
    "okay", "fine", "good", "happy", "relaxed", "calm", "normal"
]

MEDIUM_STRESS_KEYWORDS = [
    "stressed", "anxious", "worried", "tired", "pressure",
    "overthinking", "panic", "confused", "nervous",
    "not feeling good", "sad", "demotivated"
]

HIGH_STRESS_KEYWORDS = [
    "depressed", "hopeless", "worthless", "crying",
    "suicide", "kill myself", "want to die",
    "life is meaningless", "no reason to live",
    "self harm", "end my life", "can't live anymore"
]


def detect_stress_level(message):

    message = message.lower()

    for word in HIGH_STRESS_KEYWORDS:
        if word in message:
            return "High"

    for word in MEDIUM_STRESS_KEYWORDS:
        if word in message:
            return "Medium"

    for word in LOW_STRESS_KEYWORDS:
        if word in message:
            return "Low"

    return "Low"