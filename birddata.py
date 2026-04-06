import json
import os

BIRDS_FILE = "birds.json"

class BirdManager:
    def _load(self):
        if os.path.exists(BIRDS_FILE):
            try:
                with open(BIRDS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save(self, data):
        with open(BIRDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_countries(self):
        data = self._load()
        return list(data.keys())

    def get_birds(self, country):
        data = self._load()
        return data.get(country, [])

    def save_birds(self, country, birds):
        data = self._load()
        data[country] = birds
        self._save(data)

    def delete_country(self, country):
        data = self._load()
        if country in data:
            del data[country]
            self._save(data)