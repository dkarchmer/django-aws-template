{% comment "This comment section will be deleted in the generated project" %}

## django-aws-template ##

### Build Status ###

An opinionated Django project starter intended for people that will release to AWS. It assumes

1. main django server will be released to AWS Elastic Beanstalk,
2. static files will be released to s3/cloudfront using a gulp based flow (not django collectstatics)
3. Use docker for development/testing
4. Use a common set of django packages for the basics. In particular, django-allauth for social authentication
and djangorestframework for a rest API.

### Features ###

- Ready Bootstrap-themed, gulp based web pages
- User Registration/Sign up with social login support (using django-allauth)
- Ready to provide rest api for all models (using djangorestframework)
- Gulp based flow to build CSS/JS files and release directly to s3/cloudfront (based on `yo webapp`)
- Better Security with 12-Factor recommendations
- Logging/Debugging Helpers
- Works on Python 3.6+

### Quick start: ###

```
$ python3 -m venv .virtualenv/my_proj
$ . .virtualenv/my_proj/bin/activate
$ pip install django
$ django-admin.py startproject --template=https://github.com/dkarchmer/django-aws-template/archive/master.zip --extension=py,md,html,env,json,config my_proj
```

The do the following manual work:

* Create a .ebextensions directory with decired Elastic Beanstalk options. See https://github.com/dkarchmer/django-aws-template/tree/master/server/.ebextensions

* Search and replace `mydomain` with your own domain
* Search and replace `mystaticbucket` with your own S3 Bucket Name
* Search and replace `myawsregion` with your own AWS_REGION
* Search and replace `myawsprofile` with your own profile. Use `default` if you created the default one from `aws configure`
* Search and replace `mycloudfrontdistributionid` with your CloudFront Distribution ID
* Search  `need-value` and add the appropriate value based on your setup

*Rest of this README will be copied to the generated project.*

{% endcomment %}

# {{ project_name }} #

Project is built with Python using the Django Web Framework.
It is based on the django-aws-template (https://github.com/dkarchmer/django-aws-template)

This project has the following basic features:

* Custom Authentication Model with django-allauth
* Rest API

## Installation

### Assumptions

You must have the following installed on your computer

* Python 3.6 or greater
* Docker and docker-compose

If not using docker, te following dependencies are also needed:

* nodeJS v5
* bower

For MacOS, see https://gist.github.com/dkarchmer/d8124f3ae1aa498eea8f0d658be214a5


## Using Docker (preferred)

While everything can be built and run natively on your computer, using Docker ensures you use a tested environment
that is more likely to run on any computer. Installing the exact version of NodeJS, for example, is particularly
challenging.

Once you have docker and docker-compose installed (see instructions on docker web site), you will be able to build the next set of images.

This project builds the top level Django template file and all static files using modern techniques to ensure all
static files are minized and ready for a CDN.

Before you can start, you need to create a .docker.env file on your server/config/settings directory:

```
$ cp server/config/settings/sample-docker.env server/config/settings/.docker.env
```

This creates a little extra complexity, but is not a big deal when using Docker. Follow the instructions below
carefully:

### Building Static Files

These steps have to be run at least once, and every time the webapp is changed or new django statics are added (e.g.
a new version of a package is installed)

```
# 1a.- Build WebApp using Gulp
docker build -t webapp/builder webapp
docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder bower install --allow-root
docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder npm install
docker run --rm -v ${PWD}/webapp:/var/app/webapp -v ${PWD}/server:/var/app/server -v ${PWD}/staticfiles:/var/app/staticfiles -t webapp/builder gulp

# 1b.- Or run sh script
sh build-webapp.sh

# 2.- Adding any Django package statics
docker-compose build web
docker-compose run --rm web python manage.py collectstatic --noinput
```

### Running Unit Test with docker compose

After the webapp static files have been build, Docker Compose can be used to run the unit test.

```
docker-compose -f docker-compose.utest.yml run --rm web
```

### Running local server with docker compose

To run the local server to test on your local host, use docker compose like:

```
docker-compose build    # Build all containers
docker-compose up -d    # Run containers in background
docker-compose logs web # Shows logs for web container (django server)
docker-compose down     # shutdown containers
```

## Python Environment ###

It is not recommended to run on native python (you are on your own if you do), but you can do this with:

```
$ python3 -m venv  ~/.virtualenv/myproject
$ .  ~/.virtualenv/myproject/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
$ pip install -r server/requirements.txt
$ cp server/config/settings/sample-local.env server/config/settings/.local.env
```

### Static Files

We use nodeJS (v5) with Gulp and Bower to process static files. The Gulp file also contains the required code to deploy these static files to S3 and/or CloudWatch, which is the best way to deploy static files when using AWS based environments.

This is probably the most complicated part of this environment, but probably also the most innovative part. Gulp/Bower was selected (instead of plain Django `collectstatics`) because any proffesional site will end up with a lot of frontend code (using both HTML and JavaScript), and you will end up with a lot of javascript dependencies that require a good managing system. So, just like `pip` is great for Python, you need something like `bower` for javascript dependencies. And you want a modern frontend build flow like Gulp to ensure all your static files are minimized and compied into a couple of CSS and JS files. Gulp does that very well.

```
$ cd webapp
$ bower install
$ npm install
$ gulp
```

And important thing to understand is that we are basically creating the `base.html` template used by Django so these file needs to be moved (moved by the Gulp flow) to the Django `/templates` directory, so Django treats it like any other template that you could have created. The difference is that rather than that base template to be under version control, it is produced by the Gulp flow. This means that every time you change that base template (or the static CSS/JS), you need to run gulp again so it is copied again to the `/templates` directory. If you don't do this, and you try to run the local django server (or deploy it to AWS EB), the Django views will error out with a "Template not found" error.

Note also we that we only build our own front end dependencies using Gulp. But Django comes with its own static files (for the Admin pages, for example), and you may be using popular libraries like `djangorestframework` or `django-crisp` which may include their own static files. Because of this, you still need to run the normal Django `collectstatics` command. Note that the configuration in the settings file will make `collectstatics` copy all these files to the `/statics` directory, which is also where the `gulp` flow will copy the distribution files. `/statics` is the directory we ultimately release static files from. The top level. The toplevel `gulp deploy` uploads all these files to an S3 bucket to either service the static files from, or as source to your CloudWatch CDN.

To collect Django statics, run:

```
cd ../server
$ python manage.py collecstatic
```

### Database ###

To create database (SQLite3 for development), run

```
$ cd ../server
$ python manage.py migrate
$ python manage.py init-basic-data
```

`init-basic-data` will create a super user with username=admin, email=env(INITIAL_ADMIN_EMAIL) and password=admin.
Make sure you change the password right away.
It also creates django-allauth SocialApp records for Facebook, Google and Twitter (to avoid later errors). You will have to modify these records (from admin pages) with your own secret keys, or remove these social networks from the settings.

For the production server, I recommend you do NOT let elastic beanstalk create the database, and instead manually create an RDS instance. This is not done by default in this template, but you can find several comments explaining how to configure a standa-alone RDS instance when ready.


### Testing

```
$ cd ../server
$ python manage.py test
```


## Elastic Beanstack Deployment

Review all files under `server/.ebextensions`, and modify if needed. Note that many settings are
commented out as they require your own AWS settings. For example, `03-loadbalancer.config` shows how you would configure your ACM based SSL certificate. `04_notifications.config` shows how you may want to confirgure the SNS notifications to use a preconfigured topic, rather than EB creating one for you. `02_ec2.config` shows how to configure EB to use a specifc IAM role or a specific security group. Also something you will want to do.

For early development, the `create` command will ask *Elastic Beanstalk (EB)* to create and manage its own
RDS Postgres database. This also means that when the *EB* environment is terminated, the database will be
terminated as well.

Once the models are more stable, and for sure for production, it is recommended that you create your own
RDS database (outside *EB*), and simply tell Django to use that. The `.ebextensions/01_main.config` has
a bunch of `RDS_` environment variables (commented out) to use for this. Simply enable them, and set the
proper RDS address.

Before you can start, you need to create a `.production.env` file with all your secrets:

```
$ cp server/config/settings/sample-production.env server/config/settings/.production.env
```

Because you are about to deploy, you must update that .production.env with your actual secrets and domain
specific information.

### Creating the environment

Make sure you have search for all instances of `mydomain` in the code and replace with the proper settings.
Also make sure you have created your own `server/config/settings/.production.env` based on the
`sample-production.env` file.

Look for the `EDIT` comments in `tasks.py` and `gulpfile.js` and edit as needed.

After your have done all the required editing, the `create` Invoke command will run *Gulp* to deploy all static files,
and then do the `eb init` and `eb create`:

```
invoke create
```

### Deployment (development cycle)

After your have created the environment, you can deploy code changes with the following command (which will run *Gulp*
and `eb deploy`):

```
invoke deploy
```
