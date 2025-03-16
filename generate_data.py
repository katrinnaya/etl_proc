from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Подключение к MongoDB
client = MongoClient('mongodb://root:example@mongo_db:27017/?authSource=admin')
db = client['user_sessions']  # Название базы данных

# Генерация данных для коллекции UserSessions
def generate_user_sessions(num_sessions=100):
    sessions = []
    for _ in range(num_sessions):
        session = {
            "session_id": fake.uuid4(),
            "user_id": fake.uuid4(),
            "start_time": fake.date_time_this_year(),
            "end_time": fake.date_time_this_year(),
            "pages_visited": [fake.url() for _ in range(random.randint(1, 10))],
            "device": fake.user_agent(),
            "actions": [fake.word() for _ in range(random.randint(1, 5))]
        }
        sessions.append(session)
    db.UserSessions.insert_many(sessions)  # Название коллекции

if __name__ == "__main__":
    generate_user_sessions()
    print("Данные успешно сгенерированы и добавлены в MongoDB")
