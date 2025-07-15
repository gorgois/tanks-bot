# utils.py (Fixed version)
import requests

def get_player_stats(username):
    try:
        url = f"https://ratings.ranked-rtanks.online/api/profile/{username}"
        res = requests.get(url)
        if res.status_code != 200:
            return None
        data = res.json()

        stats = {
            "Username": data.get("name", "Unknown"),
            "Rank": data.get("rank", "N/A"),
            "XP": data.get("exp", 0),
            "Kills": data.get("kills", 0),
            "Deaths": data.get("deaths", 0),
            "K/D": f"{data.get('kills', 0) / max(data.get('deaths', 1), 1):.2f}",
            "Crystals": data.get("crystals", 0),
            "Gold Boxes": data.get("golds", 0),
        }
        return stats
    except Exception as e:
        print("Error in get_player_stats:", e)
        return None

def get_leaderboard(category):
    try:
        url = f"https://ratings.ranked-rtanks.online/api/leaderboard/{category}?limit=10"
        res = requests.get(url)
        if res.status_code != 200:
            return None
        data = res.json()

        results = []
        for entry in data:
            name = entry.get("name", "Unknown")
            value = entry.get(category, 0)
            results.append((name, value))

        return results
    except Exception as e:
        print("Error in get_leaderboard:", e)
        return None
