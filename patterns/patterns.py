import os

# Pattern Class
class Pattern:
    def __init__(self, name, author, description, url, pattern):
        self.name = name
        self.author = author
        self.description = description
        self.url = url
        self.pattern = pattern

# Patterns Class
class Patterns:
    
    def __init__(self):
        # Init empty dict to hold Pattern objs
        self.patterns = {}

        # File character reference for alive/dead state
        self._state_chars = {
            'O' : True,
            '.' : False
        }


    # Get filenames for all .cells files in cwd
    def get_filenames(self):
        return [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if f.endswith('.cells')]

    # Read pattern file line by line
    def read_pattern_file(self, filename):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)) as f:
            text = f.read()
            for line in text.splitlines():
                yield line

    # Add Pattern obj from .cells file
    def add_pattern_from_file(self, filename):
        # Read Lines
        lines = [l for l in self.read_pattern_file(filename)]
        # Get discriptive info
        name = lines[0][7:]
        author = lines[1][9:]
        desc = lines[2][1:]
        url = lines[3][1:]
        # Convert pattern
        pattern = [[self._state_chars[char] for char in line] for line in lines[4:]]
        # Create obj & add to patterns dict
        self.patterns[filename.split('.')[0]] = Pattern(
            name = name,
            author = author,
            description = desc,
            url = url,
            pattern = pattern
        )

    # Add all .cells files as patterns
    def add_all_patterns(self):
        for f in self.get_filenames():
            self.add_pattern_from_file(f)


