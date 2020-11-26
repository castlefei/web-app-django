# my code for web app by Django
The project builds a Python Django web app that uses the Microsoft Graph API to retrieve calendar information, access google calendar and schedule meetings for users.
# Run server
`python manage.py runserver`

changing the port:

`python manage.py runserver 8080`

for other users in LAN to load the web:

1. `python manage.py runserver 0.0.0.0:8080`-for other users in LAN 
2. settings.py: ALLOWED_HOST

# Structure

    CalendarAssistantApplication/
        manage.py - A command-line utility to interact with Django project.
        oauth_settings.yml - authorization setting file.
        graph_tutorial /
        tutorial / - web app
            migrations / - for models.
            static / - static files: .csc file.
            templates / - html pages.
            python files:
            views.py - views file.
            url.py - map url to view function.
        


