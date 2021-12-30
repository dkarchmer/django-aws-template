import os

from invoke import run, task

PROJECT_NAME = 'aws_template'

# EDIT with your own settings
AWS_PROFILE = 'myprofile'
AWS_REGION  = 'us-east-1'

# EDIT with your own settings
DEFAULT_SERVER_APP_NAME = f'{PROJECT_NAME.lower()}'
DEFAULT_SERVER_ENV_NAME = f'{PROJECT_NAME.lower()}-prod'

PROFILE_OPT = '--profile {profile}'.format(profile=AWS_PROFILE)
REGION_OPT = '--region {region}'.format(region=AWS_REGION)

SERVER_AMI = '64bit Amazon Linux 2 v3.1.1 running Python 3.7'
# SERVER_AMI = '64bit Amazon Linux 2018.03 v2.10.6 running Python 3.6'

SERVER_INSTANCE_TYPE = 't2.micro'
# Use Elastic Beanstalk managed RDS database early during development
# But it is recommended to later switch to your own RDS outside EB, especially for production.
# This makes it easy to destroy the EB environment without destroying the database
# Note that you will need to set the env variables on .ebextensions/01_main.config
DB_CMD = '-db -db.i db.t2.micro -db.engine postgres -db.version 9.5 -db.user ebroot -db.pass pass.DB'

CDN_STATICS_DISTRIBUTION_ID = 'mycloudfrontdistributionid'

@task
def create(ctx, env=DEFAULT_SERVER_ENV_NAME, app=DEFAULT_SERVER_APP_NAME):
    os.chdir('server')
    ctx.run('eb init -p "{ami}" {region} {profile} {name}'.format(region=REGION_OPT,
                                                              ami=SERVER_AMI,
                                                              profile=PROFILE_OPT,
                                                              name=app))

    # basic = '--timeout 30 --instance_type t2.micro --service-role aws-elasticbeanstalk-service-role'
    basic = '--timeout 30 --instance_type {0}'.format(SERVER_INSTANCE_TYPE)
    ctx.run("eb create {basic} {db} {region} {profile} -c {cname} {name}".format(basic=basic,
                                                                             db=DB_CMD,
                                                                             region=REGION_OPT,
                                                                             profile=PROFILE_OPT,
                                                                             cname=env,
                                                                             name=env))

@task
def deploy(ctx, type='server'):
    if type == 'server':
        # Just for Server, we need to execute gulp first
        # Will deploy everything under /staticfiles. If new
        # third party packages are added, a local python manage.py collectstatic
        # will have to be run to move static files for that package to /staticfiles

        ctx.run('gulp deploy')
    os.chdir('server')
    ctx.run('eb deploy --region={region}'.format(region=AWS_REGION))


@task
def ssh(ctx, type='server'):
    os.chdir('server')
    ctx.run('eb ssh')


@task
def build_statics(ctx, build=False):
    """Deploy static
    e.g.
       inv build-statics
    """
    cmd = 'sh build-webapp.sh'
    ctx.run(cmd, pty=True)
    run_local(ctx, action='collectstatic')


@task
def deploy_statics(ctx, build=False):
    """Deploy static
    e.g.
       inv deploy-statics
    """
    cmds = [
        f'aws s3 sync --profile {AWS_PROFILE} ./staticfiles/ s3://{PROJECT_NAME}-statics/static',
        f'aws cloudfront --profile {AWS_PROFILE} create-invalidation --distribution-id {CDN_STATICS_DISTRIBUTION_ID} --paths /',
    ]

    for cmd in cmds:
        ctx.run(cmd, pty=True)


@task
def test(ctx, action='custom', path='./apps/'):
    """Full unit test and test coverage.
    Includes all django management funcions to setup databases
    (See runtest.sh)
    Args:
        action (string): One of
            - signoff: To run full/default runtest.sh
            - custom: To run a specific set of tests
            - stop: to stop all containters
            - down: to bring down (kill) all containers (and dbs)
        path (strin): If custom, path indicatest the test path to run
    e.g.
        inv test -a signoff       # To run full default signoff test
        inv test -p ./apps/main   # to run Report tests
        inv test -a stop          # To stop all containers
        inv test -a down          # To kill all containers
    """
    # 2 Scale up or down
    cmd = f'docker-compose -f docker-compose.utest.yml -p {PROJECT_NAME.lower()}_test'
    if action == 'signoff':
        cmd += '  run --rm web'
    elif action == 'custom':
        cmd += f'  run --rm web py.test -s {path}'
    elif action in ['stop', 'down', 'build',]:
        cmd += f' {action}'
    elif 'migrate' in action:
        cmd += ' run --rm web python manage.py migrate'
    else:
        print('action can only be signoff/custom/build/stop/down/migrate')
    ctx.run(cmd, pty=True)


@task
def run_local(ctx, action='up'):
    """To run local server
    Args:
        action (string): One of
            - up: To run docker-compose up
            - stop: to stop all containters
            - down: to bring down (kill) all containers (and dbs)
            - logs-<name>: to show logs where <name> is server, worker1, worker2, etc.
    e.g.
        inv run-local -a up             # To run docker-compose up -d
        inv run-local -a stop           # To run docker-compose stop
        inv run-local -a down           # To run docker-compose down
        inv run-local -a logs-server    # To show logs for Server
        inv run-local -a makemigrations # Run Django makemigrations
        inv run-local -a collectstatic  # Run Django collectstatic
    """
    # 2 Scale up or down
    cmd = f'docker-compose -f docker-compose.yml -p {PROJECT_NAME.lower()}'
    if action == 'up':
        cmd += '  up -d'
    elif action in ['stop', 'down', 'build']:
        cmd += f' {action}'
    elif 'logs' in action:
        parts = action.split('-')
        assert len(parts) == 2
        cmd += ' logs {}'.format(parts[1])
    elif 'exec' in action:
        parts = action.split('-')
        assert len(parts) == 2
        cmd += ' exec {} bash'.format(parts[1])
    elif 'makemigrations' in action:
        cmd += ' run --rm web python manage.py makemigrations'
    elif 'collectstatic' in action:
        cmd += ' run --rm web python manage.py collectstatic --noinput'
    elif 'migrate' in action:
        cmd += ' run --rm web python manage.py migrate'
    elif 'init' in action:
        cmd += ' run --rm web ./server-init.sh'
    else:
        print('action can only be up/stop/down')
    ctx.run(cmd, pty=True)
