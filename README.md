# Django dxChat

Chat web application using Django, Django Channels, Websockets and Web Technologies (HTML, CSS, JavaScript).

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

### Build with:

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](http://www.djangoproject.com/)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindui.com/)

## :rocket: Try [dxChat](https://dxchat.ruveloper.dev) :globe_with_meridians:
The project is **LIVE** and can be accessed at the following link [dxChat](https://dxchat.ruveloper.dev).

https://user-images.githubusercontent.com/101607822/217402815-8cdb7db1-432a-4682-854b-617e304fa2e1.mp4


## Features

### Project-wide features

* Real-time updates through Django Channels and ASGI server
* HTTP and Websockets protocols implementation
* Cache system modules to manage online users and chat rooms
* User authentication and protected routes
* HTML templates system
* Scalable project structure
* Production-ready setup
* reCaptcha v3 form validation

### Chat client features

* Light and Dark theme
* Responsive design
* Sign Up, Sign In and Log Out functionality
* Echo chat to test websocket connection
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
