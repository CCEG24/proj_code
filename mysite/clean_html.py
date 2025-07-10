file_path = "tetris/templates/tetris/game.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all non-ASCII characters with a space
cleaned = ''.join(c if ord(c) < 128 else ' ' for c in content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(cleaned)

print("All non-ASCII characters replaced with spaces!")