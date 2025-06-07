import json
import os
import random
from typing import List, Dict

DATA_FILE = 'users.json'

# Sample question bank for demonstration
QUESTIONS = [
    {
        'question': 'Which class of drugs does aspirin belong to?',
        'options': ['Antibiotic', 'NSAID', 'Antiviral', 'Antifungal'],
        'answer': 1,
    },
    {
        'question': 'What is the mechanism of action of beta-blockers?',
        'options': ['Increase heart rate', 'Decrease blood pressure by blocking beta receptors', 'Promote vasodilation via nitric oxide', 'Block calcium channels'],
        'answer': 1,
    },
    {
        'question': 'Which symptom is commonly associated with Parkinson\'s disease?',
        'options': ['Tremor', 'Fever', 'Rash', 'Hypertension'],
        'answer': 0,
    },
]

def load_users() -> Dict[str, dict]:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users: Dict[str, dict]):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(users: Dict[str, dict]) -> str:
    username = input('Enter a new username: ').strip()
    if username in users:
        print('Username already exists.')
        return ''
    users[username] = {'points': 0}
    save_users(users)
    print(f'Welcome, {username}!')
    return username

def login_user(users: Dict[str, dict]) -> str:
    username = input('Enter your username: ').strip()
    if username not in users:
        print('User not found. Please register first.')
        return ''
    print(f'Welcome back, {username}!')
    return username

def ask_question() -> bool:
    q = random.choice(QUESTIONS)
    print('\n' + q['question'])
    for idx, opt in enumerate(q['options']):
        print(f'{idx + 1}. {opt}')
    try:
        choice = int(input('Your answer (number): ')) - 1
    except ValueError:
        print('Invalid input.')
        return False
    if choice == q['answer']:
        print('Correct!')
        return True
    else:
        print('Incorrect.')
        return False

def quiz_session(username: str, users: Dict[str, dict]):
    print('\nStarting quiz. Type q to quit.')
    while True:
        result = ask_question()
        if result:
            users[username]['points'] += 10
            save_users(users)
        cont = input('Continue? (y/n): ').strip().lower()
        if cont != 'y':
            break
    print(f"Total points: {users[username]['points']}")

def leaderboard(users: Dict[str, dict]):
    print('\nLeaderboard:')
    sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)
    for idx, (name, data) in enumerate(sorted_users, start=1):
        print(f"{idx}. {name} - {data['points']} pts")

def main():
    users = load_users()
    print('Welcome to ParkoMed CLI')
    while True:
        choice = input('\n1. Register\n2. Login\n3. Exit\nSelect option: ').strip()
        if choice == '1':
            username = register_user(users)
            if username:
                quiz_session(username, users)
        elif choice == '2':
            username = login_user(users)
            if username:
                quiz_session(username, users)
        elif choice == '3':
            break
        else:
            print('Invalid choice')
    leaderboard(users)

if __name__ == '__main__':
    main()
