import re

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'(const roleButtons = document\.querySelectorAll\(\'\.role-btn\'\);)'
replacement = r'\1\n\n    const exploreBtn = document.querySelector(".btn-primary");\n    const organizeBtn = document.querySelector(".btn-secondary");\n    \n    if (exploreBtn && exploreBtn.textContent.includes("Explore Events")) {\n        exploreBtn.addEventListener("click", () => {\n            window.location.href = "login.html";\n        });\n    }\n    if (organizeBtn && organizeBtn.textContent.includes("Organize an Event")) {\n        organizeBtn.addEventListener("click", () => {\n            window.location.href = "login.html";\n        });\n    }'
text = re.sub(pattern, replacement, text)

with open('c:/Users/Vishnu/OneDrive/Desktop/ZyntraPassweb/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
