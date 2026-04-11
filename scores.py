def load_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            lines = file.readlines()
            scores = []
            for line in lines:
                scores.append(int(line.strip()))
            return sorted(scores + [0, 0, 0], reverse = True)[:3]
    except (FileNotFoundError, ValueError):
        return [0, 0, 0]

def save_high_scores(scores):
    with open("high_scores.txt", "w") as file:
        for score in scores:
            file.write(str(score) + "\n")