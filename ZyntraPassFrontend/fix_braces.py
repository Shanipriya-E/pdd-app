import os

filepath = 'c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/AttendeeDiscoverActivity.kt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I see a double brace `\n    }\n\n    }` before setupBottomNav. Let's remove one.
content = content.replace("    }\n\n    }\n\n    private fun setupBottomNav", "    }\n\n    private fun setupBottomNav")

# Wait, the end of the file is:
#  }
# 
# }
# Let's fix that too.
if content.endswith(" }\n\n}"):
    content = content[:-7] + "    }\n}"

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed braces")
