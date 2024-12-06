class ScoreManager:
    def __init__(self, file_name='scores.txt'):
        self.file_name = file_name
        self.scores = []
        self.player_name = []

    def save_score(self, player_name, score):
        """Save a new score to the file."""
        with open(self.file_name, 'a') as file:
            file.write(f"{player_name}:{score}\n")

    def load_scores(self):
        """Load all scores from the file and sort them."""
        try:
            with open(self.file_name, 'r') as file:
                self.scores = [
                    (line.split(':')[0], int(line.split(':')[1]))
                    for line in file
                ]
            self.scores.sort(key=lambda x: x[1], reverse=True)  # Sort by score, descending
        except FileNotFoundError:
            self.scores = []

    def get_top_scores(self, limit=10):
        """Return the top N scores."""
        return self.scores[:limit]