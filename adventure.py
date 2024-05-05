import argparse
import json
class Room:
    def __init__(self, name, desc, exits, items=None,locked=False,required_items=None):
        self.name = name
        self.desc = desc
        self.exits = exits
        self.items = items if items else []
        self.locked = locked
        self.required_items = required_items if required_items else []

    def describe(self):
        room_info = f"> {self.name}\n\n{self.desc}\n"
        if self.items:
            room_info += "\nItems: " + " ".join(self.items) + "\n"
        room_info += "\nExits: " + " ".join(self.exits.keys()) + "\n"
        if self.locked:
            room_info += "\nThis room is locked.\n"
        return room_info

class GameState:
    def __init__(self, rooms):
        self.rooms = rooms
        self.current_room = rooms[0]
        self.inventory = []
        self.winning_condition=["magic wand","sword"]
        self.commands= {
            "go": "go ...",
            "get": "get ...",
            "look": "look",
            "inventory": "inventory",
            "drop":"drop ...",
            "quit": "quit",
            "help": "help"
        }

    def process_command(self, command):
        command_parts = command.split()
        action = command_parts[0]

        valid_commands = self.commands.keys()
        valid_command = [c for c in valid_commands if c.startswith(action)] 
        if len(valid_command) == 1:
            action = valid_command[0]

        if action == "look":
            print(self.current_room.describe())
        elif command == "help":
            self.display_help()
        elif action == "inventory" or action.startswith("inv"):
            if(len(self.inventory)==0):
                print("You're not carrying anything.")
            else:
                print(f"Inventory:\n  {', '.join(self.inventory)}")
        elif action == "go":
            if len(command_parts) > 1:
                self.move_to_room(command_parts[1])
            else:
                print("Sorry, you need to 'go' somewhere.")
        elif action == "get":
            if len(command_parts) > 1:
                self.get_item(" ".join(command_parts[1:]))
            else:
                print("Sorry, you need to 'get' something.")
        elif action == "drop" or action.startswith("d"):
            if len(command_parts) > 1:
                self.drop_item(" ".join(command_parts[1:]))
            else:
                print("Drop what?")
        else:
            exit_match = self.match_exit(action)
            if exit_match:
                self.move_to_room(exit_match)
            else:
                item_match = self.match_item(action)
                if item_match:
                    self.get_item(item_match)
                else:
                    print("Unknown command. Type 'help' for a list of commands.")

    def match_exit(self, action):
        exits = self.current_room.exits.keys()
        exact_match = [exit for exit in exits if exit == action]
        if exact_match:
            return exact_match[0]
        
        partial_matches = [exit for exit in exits if exit.startswith(action)]
        if len(partial_matches) == 1:
            return partial_matches[0]
        elif len(partial_matches) > 1:
            print("Ambiguous direction. Please be more specific.")
            return None
        else:
            print(f"There's no way to go {action}.")
            return None
    
    def match_item(self, action):
        items = self.current_room.items
        matches = [item for item in items if action in item]
        if not matches:
            print("No such item found.")
        return matches
    
    def move_to_room(self, direction):
        if direction in self.current_room.exits:
            next_room_data = self.current_room.exits[direction]
            if isinstance(next_room_data, dict): 
                if next_room_data.get("locked", False):
                    required_items = next_room_data.get("required_items", [])
                    if all(item in self.inventory for item in required_items):
                        print("You unlock the door.")
                        next_room_name = next_room_data["unlocked_room"]
                    else:
                        print(f"The door to the {direction} is locked. You need {' and '.join(required_items)} to unlock it.")
                        return
                else:
                    next_room_name = next_room_data["unlocked_room"]
            else:
                next_room_name = next_room_data

            next_room = next((room for room in self.rooms if room.name == next_room_name), None)
            if next_room:
                self.current_room = next_room
                print(f"You go {direction}.\n")
                print(self.current_room.describe())
            else:
                print(f"There's no room connected to the {direction}.")
        else:
            print(f"There's no way to go {direction}.")

    def move_to_boss_room(self):
        win_info="To win the game, you need: "+", ".join(self.winning_condition)
        if(set(self.winning_condition).issubset(set(set(self.inventory)))):
            print("Congratulations! You win! ")
        else:
            print(f"Sorry, you lose. {win_info}")
        return ask_yes_no("Would you like to start over?")
          
    def get_item(self, item_name):
        if item_name in self.current_room.items:
            self.current_room.items.remove(item_name)
            self.inventory.append(item_name)
            print(f"You pick up the {item_name}.")
        else:
            print(f"There's no {item_name} anywhere.")
    
    def drop_item(self, item_name):
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            self.current_room.items.append(item_name)
            print(f"You dropped {item_name}.")
        else:
            print(f"You don't have {item_name}.")
    
    def display_help(self):
        print("You can run the following commands:")
        for command, description in self.commands.items():
            print(f"  {command}: {description}")
        print()
        

def ask_yes_no(question):
    valid_responses = {"yes": True, "y": True, "no": False, "n": False}
    prompt = f"{question} (yes/no): "

    while True:
        response = input(prompt).strip().lower()
        if response in valid_responses:
            return valid_responses[response]
        else:
            print("Please enter 'yes' or 'no'.")


def load_game_map(filename):
    with open(filename) as file:
        data = json.load(file)
        rooms_data = data["rooms"]
        rooms = []
        for room_data in rooms_data:
            room = Room(
                name=room_data["name"],
                desc=room_data["desc"],
                exits=room_data["exits"],
                items=room_data.get("items"),
                locked=room_data.get("locked",False),
                required_items=room_data.get("required_items")
            )
            rooms.append(room)
        return rooms
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map_filename")
    args = parser.parse_args()

    while True: 
        rooms = load_game_map(args.map_filename)
        game_state = GameState(rooms)

        game_state.process_command("look")
        while True:
            try:
                command = input("What would you like to do? ").strip().lower()
                if command == "quit":
                    print("Goodbye!")
                    return
                game_state.process_command(command)

                if game_state.current_room.name == "Boss Room":
                    if game_state.move_to_boss_room(): 
                        break 
                    else:
                        print("Thank you for playing! Goodbye.")
                        return
            except EOFError:
                print("Use 'quit' to exit.")
                continue
            except KeyboardInterrupt:
                return
    
if __name__ == "__main__":
    main()
