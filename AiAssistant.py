from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List
from abc import ABC, abstractmethod

# Part 1: Data Type Design
class CommandType(Enum):
    MUSIC = "MUSIC"
    FITNESS = "FITNESS"
    STUDY = "STUDY"

@dataclass
class UserProfile:
    name: str
    age: int
    preferences: Dict[str, Any]
    isPremium: bool

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.age, int) or self.age < 0:
            raise ValueError("age must be a non-negative integer")
        if not isinstance(self.preferences, dict):
            raise ValueError("preferences must be a dictionary")
        if not isinstance(self.isPremium, bool):
            raise ValueError("isPremium must be a boolean")

@dataclass
class Request:
    input: str
    timestamp: datetime
    command_type: CommandType

    def __post_init__(self):
        if not isinstance(self.input, str) or not self.input.strip():
            raise ValueError("input must be a non-empty string")
        if not isinstance(self.timestamp, datetime):
            raise ValueError("timestamp must be a datetime object")
        if not isinstance(self.command_type, CommandType):
            raise ValueError("command_type must be a CommandType enum")

@dataclass
class Response:
    message: str
    confidence: float
    actionPerformed: bool

    def __post_init__(self):
        if not isinstance(self.message, str):
            raise ValueError("message must be a string")
        if not isinstance(self.confidence, float) or not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be a float between 0.0 and 1.0")
        if not isinstance(self.actionPerformed, bool):
            raise ValueError("actionPerformed must be a boolean")

# Part 2: Core OOP Structure
class AIAssistant(ABC):
    def __init__(self, profile: UserProfile):
        self.profile = profile

    def greetUser(self) -> None:
        print(f"Hello, {self.profile.name}! How can I assist you today?")

    def handleRequest(self, request: Request) -> Response:
        return self.generateResponse(request)

    @abstractmethod
    def generateResponse(self, request: Request) -> Response:
        ...

class MusicAssistant(AIAssistant):
    def recommendPlaylist(self, mood: str) -> List[str]:
        mood_playlists = {
            "happy": ["Happy - Pharrell Williams", "Walking on Sunshine - Katrina & The Waves"],
            "sad": ["Someone Like You - Adele", "Fix You - Coldplay"],
            "relaxed": ["Weightless - Marconi Union", "Clair de Lune - Debussy"]
        }
        return mood_playlists.get(mood.lower(), ["Shape of You - Ed Sheeran"])

    def generateResponse(self, request: Request) -> Response:
        mood = request.input
        playlist = self.recommendPlaylist(mood)
        msg = f"Based on your mood ({mood}), here's a playlist: {', '.join(playlist)}."
        return Response(message=msg, confidence=0.9, actionPerformed=True)

class FitnessAssistant(AIAssistant):
    def suggestWorkout(self, goal: str) -> List[str]:
        goal_plans = {
            "strength": ["3x5 Squats", "3x5 Deadlifts", "3x8 Bench Press"],
            "cardio": ["30-min Run", "15-min HIIT", "20-min Cycling"]
        }
        return goal_plans.get(goal.lower(), ["20-min Walk"])

    def generateResponse(self, request: Request) -> Response:
        goal = request.input
        plan = self.suggestWorkout(goal)
        msg = f"Here's a {goal} workout plan: {', '.join(plan)}."
        return Response(message=msg, confidence=0.85, actionPerformed=True)

class StudyAssistant(AIAssistant):
    def scheduleStudy(self, subject: str) -> str:
        return f"Scheduled a 1-hour study session for {subject} tomorrow at 6 PM."

    def explainTopic(self, topic: str) -> str:
        return f"Here's a brief explanation of {topic}: [placeholder explanation]."

    def generateResponse(self, request: Request) -> Response:
        subject = request.input
        session_info = self.scheduleStudy(subject)
        explanation = self.explainTopic(subject)
        msg = f"{session_info}\n{explanation}"
        return Response(message=msg, confidence=0.8, actionPerformed=True)

# Part 3:
if __name__ == "__main__":
    name = input("Enter your name: ").strip()
    age = int(input("Enter your age: ").strip())
    is_premium_input = input("Are you a premium user? (yes/no): ").strip().lower()
    is_premium = is_premium_input in ("yes", "y", "true", "1")

    # Choose assistant type
    print("Which assistant would you like? (music/fitness/study)")
    choice = input("Choice: ").strip().lower()

    # Get domain-specific input
    if choice == "music":
        mood = input("How are you feeling today (e.g., happy, sad, relaxed)? ").strip()
        preferences = {"mood": mood}
        profile = UserProfile(name=name, age=age, preferences=preferences, isPremium=is_premium)
        assistant = MusicAssistant(profile)
        cmd_type = CommandType.MUSIC
        user_input = mood

    elif choice == "fitness":
        goal = input("What is your fitness goal (e.g., strength, cardio)? ").strip()
        preferences = {"fitness_goal": goal}
        profile = UserProfile(name=name, age=age, preferences=preferences, isPremium=is_premium)
        assistant = FitnessAssistant(profile)
        cmd_type = CommandType.FITNESS
        user_input = goal

    elif choice == "study":
        subject = input("Which subject would you like help with? ").strip()
        preferences = {"subject": subject}
        profile = UserProfile(name=name, age=age, preferences=preferences, isPremium=is_premium)
        assistant = StudyAssistant(profile)
        cmd_type = CommandType.STUDY
        user_input = subject

    else:
        print("Invalid choice. Exiting.")
        exit(1)

    # Create and process request
    request = Request(input=user_input, timestamp=datetime.now(), command_type=cmd_type)
    assistant.greetUser()
    response = assistant.handleRequest(request)
    print(f"\nAssistant Response: {response.message}")
    print(f"Confidence Score: {response.confidence}")
    print(f"Action Performed: {response.actionPerformed}")
