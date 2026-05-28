import sys
import ftfy

filepath = r"g:\gagan\uncle_bot\newbot.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Fix the text using ftfy
fixed_text = ftfy.fix_text(text)

if text != fixed_text:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fixed_text)
    print("Fixed and saved!")
else:
    print("No issues found.")
