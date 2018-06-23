# -*- coding: utf-8 -*-
# coding: utf-8

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/fernandoarrj/staging-superlists'
ENVNAME = 'superlists'
SITENAME = 'staging-superlists'
ENV = '/home/eslpeth/miniconda3/envs/superlists/bin/python3.6'

def deploy():
	site_folder = f'/home/{env.user}/sites/staging-superlists'
	source_folder = site_folder + '/superlists'
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(site_folder)
	_update_settings(source_folder, SITENAME)
	_update_static_files(source_folder)
	_update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database','static','virtualenv','source'):
		run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(site_folder):
	if exists(site_folder +'/.git'):
		run(f'cd {site_folder} && git fetch')
	else:
		run(f'git clone {REPO_URL} {site_folder}')
	current_commit = local("git log -n 1 --format=%H", capture=True)
	run(f'cd {site_folder} && git reset --hard {current_commit}')

def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/superlists/settings.py'
	sed(settings_path, "DEBUG = True", "DEBUG = False")
	sed(settings_path,
		'ALLOWED_HOSTS =.+$',
		f'ALLOWD_HOSTS = ["{site_name}"]'
	)
	secret_key_file = source_folder + '/secret_key.py'
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, f'SECRET_KEY = "{key}"')
	append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_static_files(source_folder):
	run(
		f'cd {source_folder}'
		f' && {ENV} manage.py collectstatic --noinput'
	)

def _update_database(source_folder):
	run(
		f'cd {source_folder}'
		f' && {ENV} manage.py migrate --noinput'
	)
