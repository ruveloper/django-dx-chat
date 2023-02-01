# Django HTMX Chat

Chat web application using Django, Django Channels and web technologies (HTML, CSS, JavaScript).

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

### Build with:

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](http://www.djangoproject.com/)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindui.com/)

License: MIT

### Project Features

* Realtime Application
* ASGI server
* HTTP and Websockets implementation
* User authentication
* Protected routes
* HTML templates system
* Custom user model
* Scalable project folder structure
* Production ready project template

### Chat App features

* Light and Dark theme
* Responsive design
* Sign Up, Sign In and Log Out
* Echo chat to test the websocket connection
* List of users online
* Temporally store chat messages

## ✨ GETTING STARTED WITH DEV MODE

1. Create a python virtualenv and install requirements:
   ```
   python -m venv .venv
   (windows) .\.venv\Scripts\activate
   pip install -r .\requirements\local.txt
   ```

2. Set the environment variables:
    - Copy or rename **.env-dev-template** to **.env**
   ```
   cp .env-dev-template .env
   ```

3. Init Django:
   ```
   python manage.py migrate
   python manage.py runserver
   ```

4. **[OPTIONAL]** Init Tailwind using the Standalone CLI:

   Use Tailwind CSS without Node.js with the Standalone CLI
    - Download the [latest release](https://github.com/tailwindlabs/tailwindcss/releases/) in the root project folder
    - Start the watcher in development environment
   ```
   ./tailwindcss -i ./apps/website/static/css/input.css -o ./apps/website/static/css/dist/output.css --watch
   ```
    - Start the watcher in development environment
   ```
   ./tailwindcss -i ./apps/website/static/css/input.css -o ./apps/website/static/css/dist/output.css --minify
   ```

5. Visit: http://127.0.0.1:8000/

## License

[MIT](https://choosealicense.com/licenses/mit/)
