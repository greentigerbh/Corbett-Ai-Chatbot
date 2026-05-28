import sys

test_str = "ðŸ ¾" # This is the emoji 🐾 encoded as utf-8, decoded as cp1252/latin1, encoded as utf-8 again
print("Original:", repr(test_str))
try:
    print("Latin1 bytes:", test_str.encode('latin1'))
    print("Decoded back:", test_str.encode('latin1').decode('utf-8'))
except Exception as e:
    print("Latin1 error:", e)

try:
    print("cp1252 bytes:", test_str.encode('cp1252'))
    print("Decoded back:", test_str.encode('cp1252').decode('utf-8'))
except Exception as e:
    print("cp1252 error:", e)

with open(r"g:\gagan\uncle_bot\newbot.html", "r", encoding="utf-8") as f:
    text = f.read()

# Let's try to fix a small snippet
snippet = "Since you prefer wildlife views, planning safari sessions in <strong>Bijrani</strong> or\n                            <strong>Dhikala</strong> is highly recommended.</span>\n                    </li>\n                    <li class=\"flex gap-2\">\n                        <span class=\"text-orange-500 shrink-0\">ðŸŒŠ</span>"
print("\nSnippet to fix:", repr(snippet))
try:
    print("Fixed snippet (latin1):", snippet.encode('latin1').decode('utf-8'))
except Exception as e:
    print("Snippet latin1 error:", e)

try:
    print("Fixed snippet (cp1252):", snippet.encode('cp1252').decode('utf-8'))
except Exception as e:
    print("Snippet cp1252 error:", e)

