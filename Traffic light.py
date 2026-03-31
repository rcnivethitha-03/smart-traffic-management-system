
import time
import random
from datetime import datetime

# ANSI colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def countdown(label, seconds, color=""):
    for sec in range(seconds, 0, -1):
        print(f"{color}{label} in {sec}...{RESET}", end="\r")
        time.sleep(1)
    print(f"{color}{label}: GO!{' ' * 20}{RESET}")


# Base Class
class System:
    def __init__(self, config):
        self.config = config
        print(f"\n{BOLD}{BLUE}Smart Traffic Management System Initialized{RESET}")


# Google Maps Simulation
class GoogleMapsIntegration:
    def __init__(self):
        print(f"{BLUE}Google Maps Simulation Initialized{RESET}")

    def get_traffic_data(self):
        directions = ["North", "East", "South", "West"]
        congestion_levels = {}

        current_hour = datetime.now().hour
        is_rush = (7 <= current_hour <= 9) or (17 <= current_hour <= 19)

        for d in directions:
            if is_rush:
                congestion = random.choice(["high", "high", "medium", "low"])
            else:
                congestion = random.choice(["low", "medium", "high"])
            congestion_levels[d] = congestion

        return congestion_levels

    def get_weather_data(self):
        conditions = ["sunny", "rainy", "cloudy", "foggy"]
        return {
            "condition": random.choice(conditions),
            "temperature": random.randint(20, 35)
        }


# Traffic Signal
class TrafficSignal(System):
    def signal_cycle(self, red, yellow, green):
        print(f"\n{GREEN}GREEN LIGHT{RESET}")
        countdown("Green", green, GREEN)

        print(f"\n{YELLOW}YELLOW LIGHT{RESET}")
        countdown("Yellow", yellow, YELLOW)

        print(f"\n{RED}RED LIGHT{RESET}")
        countdown("Red", red, RED)


# Emergency Handler
class EmergencyHandler:
    def emergency_override(self, directions, emergency_direction, duration):
        print(f"\n{RED}EMERGENCY OVERRIDE: {emergency_direction}{RESET}")
        for i in range(duration, 0, -1):
            for d in directions:
                if d == emergency_direction:
                    print(f"{d}: GREEN ({i}s)", end=" | ")
                else:
                    print(f"{d}: RED", end=" | ")
            print()
            time.sleep(1)


# Smart Traffic Signal
class SmartTrafficSignal(TrafficSignal, EmergencyHandler):
    def __init__(self, config):
        super().__init__(config)
        self.directions = ["North", "East", "South", "West"]
        self.maps = GoogleMapsIntegration()
        self.base_green = config["green"]

    def adjust_timings(self):
        traffic = self.maps.get_traffic_data()
        weather = self.maps.get_weather_data()

        print(f"\nWeather: {weather['condition']} | Temp: {weather['temperature']}°C")

        self.timings = {}
        for d in self.directions:
            level = traffic[d]

            if level == "high":
                factor = 1.5
            elif level == "low":
                factor = 0.8
            else:
                factor = 1

            if weather["condition"] in ["rainy", "foggy"]:
                factor *= 1.2

            self.timings[d] = int(self.base_green * factor)

        print("\nAdjusted Timings:")
        for d in self.directions:
            print(f"{d}: {traffic[d]} → {self.timings[d]} sec")

    def run(self):
        self.adjust_timings()

        for d in self.directions:
            print(f"\n=== {d} Lane ===")
            self.signal_cycle(5, 2, self.timings[d])


# MAIN
def main():
    config = {
        "green": 10
    }

    system = SmartTrafficSignal(config)

    while True:
        print("\n1. Run Simulation")
        print("2. Emergency Mode")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            system.run()

        elif choice == "2":
            direction = input("Enter emergency direction: ")
            system.emergency_override(system.directions, direction, 10)

        elif choice == "3":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()