1. Flask is a full-stack micro framework,
-- combining Frontend(HTML,CSS,JS), Backend(Python,JS,Java, etc.), Database (SQL)

2. MVC (Model View Controller)
-- Model (Database), View (Frontend), Controller (Backend)

3. Virtual Environment
-- A tool that helps to keep dependencies required by different projects separate by 
-- creating isolated python virtual environments for them.

-Mac: 
		-create: python3 -m venv my_venv
		-activate: source my_venv/bin/activate

-Windows:
		-create: python -m venv my_venv
		-activate: my_venv\Scripts\activate

4. useful pip commands
-- pip install
-- pip uninstall
-- pip list
-- pip freeze
-- NOTE: use pip3 for MAC

5. Requirements.txt
-- pip freeze > requirements.txt
-- Just a text file that includes all of the packages needed for the specific project

6. Jinja2
-- templating language for python
-- for loops, if-else statements
-- routing to different pages
-- template inheritance (extends, include)

7. Create templates folder & import render_template
-- flask render_template looks for a folder named "templates" in order to render html documents.

8. .gitignore
-- Ignores files/folders to push up to github
(my_venv, __pycache__)