import re

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/MainActivity.kt', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'(val btnSignIn = findViewById<Button>\(R\.id\.btnSignIn\))'
replacement = r'\1\n        val btnExploreEvents = findViewById<Button>(R.id.btnExploreEvents)\n        val btnOrganizeEvent = findViewById<Button>(R.id.btnOrganizeEvent)'
text = re.sub(pattern, replacement, text)

pattern2 = r'(btnCreateAccount\.setOnClickListener \{\n            startActivity\(Intent\(this, RoleSelectionActivity::class\.java\)\)\n        \})'
replacement2 = r'\1\n\n        btnExploreEvents.setOnClickListener {\n            startActivity(Intent(this, LoginActivity::class.java))\n        }\n\n        btnOrganizeEvent.setOnClickListener {\n            startActivity(Intent(this, LoginActivity::class.java))\n        }'
text = re.sub(pattern2, replacement2, text)

with open('c:/Users/Vishnu/zyntraPassForntend/app/src/main/java/com/simats/zyntrapass/MainActivity.kt', 'w', encoding='utf-8') as f:
    f.write(text)
