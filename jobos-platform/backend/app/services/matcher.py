from ..config import settings

def score_job(title: str, location: str, description: str) -> int:
    text = f"{title} {location} {description}".lower()
    roles = settings.csv(settings.target_roles)
    locations = settings.csv(settings.target_locations)
    score = 40
    score += min(35, sum(1 for r in roles if r.lower() in text) * 10)
    score += min(15, sum(1 for l in locations if l.lower() in text) * 5)
    if any(x.lower() in text for x in settings.csv(settings.excluded_countries)):
        score -= 30
    return max(0, min(100, score))
