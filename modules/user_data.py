import json
from pathlib import Path
from modules.luna_lib import create_file

# Define a function to ensure the existence of a user data directory and files.
def ensure_user_data_exists():
    """
    Ensures that the user data directory exists and contains necessary files.
    Creates the directory and files if they don't exist.
    """
    # Define the required files that must exist within the user data directory.
    required_files = {"settings.json"}
    
    # Define the path to the user data directory.
    user_data_path = Path("./userdata/").resolve()
    
    # Check if the user data directory does not exist and create it if needed.
    if not user_data_path.is_dir():
        user_data_path.mkdir(parents=True, exist_ok=True)
    
    # Iterate over the required files.
    for filename in required_files:
        # Construct the full path to the file.
        file_path = user_data_path / filename
        
        # Create the file if it does not exist.
        if not file_path.is_file():
            create_file(str(file_path))

class settings:
    """
    Manages application settings stored in a JSON file.

    Attributes:
        config_file (str): Path to the JSON file where settings are stored.
        settings (dict): Dictionary containing the loaded settings.
    """

    def __init__(self, config_file="./userdata/settings.json"):
        """
        Initialize the settings instance and load settings from the JSON file.

        Args:
            config_file (str): Optional path to the JSON file. Default is './userdata/settings.json'.
        """
        try:
            with open(config_file, "r") as file:
                self.settings = json.load(file)
        except Exception as error:
            print(f"Failed to load settings from {config_file}:\n\n{error}")
            self.settings = {}

    def get(self, key, default=None):
        """
        Retrieve a setting value by key, returning a default value if the key is not present.

        Args:
            key (str): The key of the setting to retrieve.
            default: The value to return if the key is not found. Default is None.

        Returns:
            The value associated with the key or the default value.
        """
        return self.settings.get(key, default)

    def set(self, key, value):
        """
        Set a setting value by key.

        Args:
            key (str): The key of the setting to set.
            value: The value to associate with the key.
        """
        self.settings[key] = value
        self._save()

    def _save(self):
        """
        Save the current settings to the JSON file.
        """
        try:
            with open("./userdata/settings.json", "w") as file:
                json.dump(self.settings, file, indent=4)
        except Exception as error:
            print(f"Failed to save settings to file:\n{error}")

Settings = settings()

if __name__ == "__main__":
    ensure_user_data_exists() # if you'd like to run the check manuelly 