# astrology/mock_data.py (if no API available)
ZODIAC_TRAITS = {
    'Aries': {'times': ['morning'], 'colors': ['#ff0000'], 'keywords': ['bold']},
    'Taurus': {'times': ['afternoon'], 'colors': ['#00ff00'], 'keywords': ['reliable']},
    # ... add all zodiac signs
}

HOROSCOPE_TEMPLATES = [
    "The stars say you'll {action} in {language} today. {emoji}",
    "Your {planet} is aligned with {tool}... time to debug!",
]

def mock_horoscope(commit_data):
    # Generate funny predictions using commit stats
    return f"Mercury in {random.choice(['Python', 'JavaScript'])} " + 
           f"indicates {random.choice(['segfaults', 'NaN errors'])} ahead!"
