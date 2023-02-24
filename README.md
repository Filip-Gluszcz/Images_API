Docker is required to run the solution.
https://docs.docker.com/engine/install/

After installing and starting Docker, run terminal/cmd. In the project folder, first type the command to build Docker image:
docker-compose -f local.yml build

Then type:
docker-compose -f local.yml up

In a new terminal/cmd window, type:
docker exec -it core_local_django /bin/bash

Then create new admin user:
python manage.py createsuperuser

Go to http://127.0.0.1:8000/admin/ and login with created admin user credentials

First create thumbnails with 200px and 400px size.
Next create tiers: 
-Basic (select 200px thumbnail)
-Premium (select 200px thumbnail, 400px thumbnail and ori_img_link)
-Enterprise (select 200px thumbnail, 400px thumbnail, ori_img_link and expiring_link)

Create account (assign a admin user to any tier)

Go to http://127.0.0.1:8000/swagger/ for usage docs.
