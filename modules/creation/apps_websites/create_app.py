import os
import json

TEMPLATES = {
    "flask": {
        "main.py": """from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello, World!'\n\nif __name__ == '__main__':\n    app.run(debug=True)""",
        "requirements.txt": "flask"
    },
    "cli": {
        "main.py": """import argparse\n\ndef main():\n    parser = argparse.ArgumentParser(description='CLI App')\n    parser.add_argument('--name', type=str, help='Your name')\n    args = parser.parse_args()\n    print(f'Hello, {args.name}!')\n\nif __name__ == '__main__':\n    main()""",
        "requirements.txt": ""
    },
    "django": {
        "setup.sh": """#!/bin/bash\npython -m venv venv\nsource venv/bin/activate\npip install django\ndjango-admin startproject myproject .""",
        "requirements.txt": "django"
    },
    "fastapi": {
        "main.py": """from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {"message": "Hello, World!"}\n\nif __name__ == '__main__':\n    import uvicorn\n    uvicorn.run(app, host='0.0.0.0', port=8000)""",
        "requirements.txt": "fastapi\nuvicorn"
    },
    "vite": {
        "setup.sh": """#!/bin/bash\nnpm create vite@latest my-project --template react\ncd my-project\nnpm install\nnpm run dev""",
        "package.json": "{}"
    },
    "react": {
        "setup.sh": """#!/bin/bash\nnpx create-react-app my-app\ncd my-app\nnpm start""",
        "package.json": "{}"
    }
}

class AppCreator:
    def __init__(self, project_name, template):
        self.project_name = project_name
        self.template = template.lower()
        self.create_project()
    
    def create_project(self):
        """Creates a new project with the selected template."""
        if self.template not in TEMPLATES:
            print(f"❌ Error: Template '{self.template}' not found.")
            return
        
        os.makedirs(self.project_name, exist_ok=True)
        for filename, content in TEMPLATES[self.template].items():
            with open(os.path.join(self.project_name, filename), "w") as f:
                f.write(content)
        print(f"✅ Successfully created '{self.project_name}' using '{self.template}' template.")
    
if __name__ == "__main__":
    project_name = input("Enter project name: ")
    template = input("Choose a template (flask/cli/django/fastapi/vite/react): ")
    AppCreator(project_name, template)