docker build -t webapp/builder webapp

docker run --rm -v ${PWD}/webapp:/var/app/webapp -t webapp/builder rm -rf /var/app/webapp/node_modules
docker run --rm -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder rm -rf /var/app/staticfiles/admin
docker run --rm -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder rm -rf /var/app/staticfiles/debug_toolbar
docker run --rm -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder rm -rf /var/app/staticfiles/rest_framework
docker run --rm -v ${PWD}/server:/var/app/server -t webapp/builder rm -rf /var/app/server/templates/dist
docker run --rm -v ${PWD}/server:/var/app/server -t webapp/builder mkdir /var/app/server/templates/dist /var/app/server/templates/dist/webapp

docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder npm install
docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder gulp
