docker build -t webapp/builder webapp
docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder bower install --allow-root
docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder npm install
docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder gulp
