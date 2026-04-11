def load_high_scores():
    try:
        with open("high_scores.txt", "r") as file:
            scores = []
            for line in file:
                name, score = line.strip().split(",")
                scores.append({"name": name,"score": int(score)})
            return sorted(scores, key=lambda x: x["score"], reverse = True)[:3]
    except (FileNotFoundError, ValueError, IndexError):
        return [{"name": "---","score": 0}] * 3

def save_high_scores(scores):
    with open("high_scores.txt", "w") as file:
        for score in scores:
            file.write(f"{score["name"]},{score["score"]}\n")