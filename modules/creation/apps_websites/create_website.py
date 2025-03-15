# AI-assisted website creation
import os
import json

TEMPLATES = {
    "html": {
        "index.html": """<!DOCTYPE html>\n<html>\n<head>\n    <title>My Website</title>\n</head>\n<body>\n    <h1>Welcome to My Website</h1>\n</body>\n</html>"""
    },
    "flask": {
        "app.py": """from flask import Flask, render_template\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return render_template('index.html')\n\nif __name__ == '__main__':\n    app.run(debug=True)""",
        "templates/index.html": """<!DOCTYPE html>\n<html>\n<head>\n    <title>Flask Website</title>\n</head>\n<body>\n    <h1>Welcome to My Flask Website</h1>\n</body>\n</html>""",
        "requirements.txt": "flask"
    },
    "django": {
        "setup.sh": """#!/bin/bash\npython -m venv venv\nsource venv/bin/activate\npip install django\ndjango-admin startproject mysite .""",
        "requirements.txt": "django"
    },
    "vite": {
        "setup.sh": """#!/bin/bash\nnpm create vite@latest my-website --template react\ncd my-website\nnpm install\nnpm run dev""",
        "package.json": "{}"
    },
    "react": {
        "setup.sh": """#!/bin/bash\nnpx create-react-app my-website\ncd my-website\nnpm start""",
        "package.json": "{}"
    }
}

class WebsiteCreator:
    def __init__(self, project_name, template):
        self.project_name = project_name
        self.template = template.lower()
        self.create_website()
    
    def create_website(self):
        """Creates a new website project with the selected template."""
        if self.template not in TEMPLATES:
            print(f"❌ Error: Template '{self.template}' not found.")
            return
        
        os.makedirs(self.project_name, exist_ok=True)
        for filename, content in TEMPLATES[self.template].items():
            file_path = os.path.join(self.project_name, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
        print(f"✅ Successfully created '{self.project_name}' using '{self.template}' template.")
    
if __name__ == "__main__":
    project_name = input("Enter project name: ")
    template = input("Choose a template (html/flask/django/vite/react): ")
    WebsiteCreator(project_name, template)