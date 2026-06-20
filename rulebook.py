class Rulebook:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.load()

# Load the rulebook from file
    def load(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
            print(f"Loaded {len(self.content)} characters from {self.file_path}")
        except FileNotFoundError:
            print(f"Error: {self.file_path} not found")
        except Exception as e:
            print(f"Error reading file: {e}")

# Search for a Keyword and show matching lines
    def search(self, keyword):
        results = []
        for line_number, line in enumerate(self.content.split('\n'), 1):
            if keyword.lower() in line.lower():
                results.append((line_number, line.strip()))
        return results

# Print Search Results Nicely
    def show_results(self, keyword, max_results=10):
        results = self.search(keyword)
        if not results:
            print(f"\nNo results found for '{keyword}'")
            return
        print(f"\n Found {len(results)} results for '{keyword}':")

# Truncate long lines to 120 characters       
        for i, (line_num, line) in enumerate(results[:max_results]):
            display_line = line[:120] + "..." if len(line) > 120 else line
            print(f" Line {line_num}: {display_line}")

if __name__ == "__main__":
    rules = Rulebook("mtg_rules2026.txt")
    rules.show_results("haste")
    rules.show_results("flying")
    rules.show_results("commander")
    rules.show_results("lifelink")

