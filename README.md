{% comment "This comment section will be deleted in the generated project" %}

## django-aws-template ##

### Build Status ###

An opinionated Django project starter intended for people that will release to AWS. It assumes

1. Django 3.2+
1. main django server will be released to AWS Elastic Beanstalk,
1. static files will be released to s3/cloudfront using a gulp based flow (not django collectstatics)
1. Use docker for development/testing
1. Use a common set of django packages for the basics. In particular, django-allauth for social authentication
and djangorestframework for a rest API.

### Features ###

- Ready Bootstrap-themed, gulp based web pages
- User Registration/Sign up with social login support (using django-allauth)
- Ready to provide rest api for all models (using djangorestframework)
- Gulp based flow to build CSS/JS files and release directly to s3/cloudfront (based on `yo webapp`)
- Better Security with 12-Factor recommendations
- Logging/Debugging Helpers
- Works on Python 3.8+ with Django 3.2+

### Quick start: ###

```
$ python3 -m venv .virtualenv/my_proj
$ . .virtualenv/my_proj/bin/activate
$ pip install django
$ django-admin.py startproject --template=https://github.com/dkarchmer/django-aws-template/archive/master.zip --extension=py,md,html,env,json,config my_proj
```

The do the following manual work:

* Create a .ebextensions directory with decired Elastic Beanstalk options. See https://github.com/dkarchmer/django-aws-template/tree/master/server/.ebextensions

* Search and replace `PROECT_NAME` with your own project name.
* Search and replace `mydomain` with your own domain
* Search and replace `mystaticbucket` with your own S3 Bucket Name
* Search and replace `us-east-1` with your own AWS_REGION
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

* Python 3.8 or greater
* Docker and docker-compose

If not using docker, the following dependencies are also needed:

* nodeJS v10
* gulp

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

```bash
inv build-statics
inv run-local -a collectstatics
```

### Running Unit Test with docker compose

After the webapp static files have been build, Docker Compose can be used to run the unit test.

```bash
inv test -a build
inv test -a signoff
inv test -a custom -p apps/main
```

### Running local server with docker compose

To run the local server to test on your local host, use docker compose like:

```bash
inv run-local -a up
inv run-local -a logs-web
inv run-local -a makemigrations
inv run-local -a migrate
inv run-local -a down
```

And important thing to understand is that we are basically creating the `base.html` template used by Django so these file needs to be moved (moved by the Gulp flow) to the Django `/templates` directory, so Django treats it like any other template that you could have created. The difference is that rather than that base template to be under version control, it is produced by the Gulp flow. This means that every time you change that base template (or the static CSS/JS), you need to run gulp again so it is copied again to the `/templates` directory. If you don't do this, and you try to run the local django server (or deploy it to AWS EB), the Django views will error out with a "Template not found" error.

Note also we that we only build our own front end dependencies using Gulp. But Django comes with its own static files (for the Admin pages, for example), and you may be using popular libraries like `djangorestframework` or `django-crisp` which may include their own static files. Because of this, you still need to run the normal Django `collectstatics` command. Note that the configuration in the settings file will make `collectstatics` copy all these files to the `/statics` directory, which is also where the `gulp` flow will copy the distribution files. `/statics` is the directory we ultimately release static files from. The top level. The toplevel `inv build-statics deploy-staics` uploads all these files to an S3 bucket to either service the static files from, or as source to your CloudWatch CDN.

To collect Django statics, run:

```
inv run-local -a collectstatics
```

### Run local server (Docker)

```bash
inv run-local -a build
inv run-local -a up
inv run-local -a down
```

`init-basic-data` will create a super user with username=admin, email=env(INITIAL_ADMIN_EMAIL) and password=admin.
Make sure you change the password right away.
It also creates django-allauth SocialApp records for Facebook, Google and Twitter (to avoid later errors). You will have to modify these records (from admin pages) with your own secret keys, or remove these social networks from the settings.

For the production server, I recommend you do NOT let elastic beanstalk create the database, and instead manually create an RDS instance. This is not done by default in this template, but you can find several comments explaining how to configure a standa-alone RDS instance when ready.

### Testing

```bash
inv test -a signoff
inv test -a custom -p apps/main
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
inv build-statics deploy-statics
inv deploy
```

# Updating requirements

This projects use pip-tools to manage requirements. Lists of required packages for each environment are located in *.in files, and complete pinned *.txt files are compiled from them with pip-compile command:

```bash
cd server 
pip-compile requirements/base.in
pip-compile requirements/development.in
```

To update dependency (e.g django) run following:

```bash
pip-compile --upgrade-package django==3.1 requirements/base.in
pip-compile --upgrade-package django==3.1 requirements/development.in
```
