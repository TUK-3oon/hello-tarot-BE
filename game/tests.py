from django.test import TestCase

# Create your tests here.
class GameTestCase(TestCase):
    def setUp(self):
        pass

    def test_game_rule_by_type_name(self):
        data = {
            "game_type_name": "love" # love, fortune, health
        }

        response = self.client.post("/game/rule", data, content_type="application/json")

    def test_game_start(self):
        data = {
            "game_type_id": "92f4ab20-c59d-4304-85b3-a1e4fda8af4a"
        }

        response = self.client.post("/game/start", data, content_type="application/json")

    def test_game_end(self):
        data = {
                    "game_id": "f8f99895-3d11-4294-bf33-ad220ef54840",
                    "select_card_id": "0b0e3e57-269c-4096-97ab-ab700f96310a",
                    "all_select_card_id": {
                        "primary_select_card_id": "0b0e3e57-269c-4096-97ab-ab700f96310a",
                        "sceondary_select_  card_id": "2f2261df-62b5-42ed-8221-7675b8b0fe88",
                        "tertiary_select_card_id": "fa764062-c9f5-4ddc-a721-aa1c6c450209"
                    }
                }
        
        response = self.client.post("/game/end", data, content_type="application/json")