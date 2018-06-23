Provisionamento de um novo site

==============================

## Pacotes ncessários

* nginx
* python 3.6
* conda
* git

## Config do Nginx Virtual Host

* veja nginx.template.conf
* substitua SITENAME, por exemplo, por staging.my-domain.com

## Serviço Systemd

* veja gunicorn-systemd.template.service
* substitua SITENAME, por exemplo, por staging.my-domaing.com

## Estrutura de pastas:
Suponha que temos uma conta de usuário em /home/username

/home/username
___sites
	___SITENAME
		___database
		___source
		___static
		___virtualenv
