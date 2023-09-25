=======================
Mentorh Web Controller
=======================

Introdução
============

O Mentorh é um sistema de gestão de recursos humanos criado pela empresa OSM.

O pacote mrh.web serve para automatizar a interação com o Mentorh via navegador web.


Versões Python Suportadas
===========================

* Python 3.10+


Instalação
==============

Utilizando o pip::
    
    pip install mrh.web

A partir do código fonte::

    python setup.py install

Executando testes
===================

Instale o ambiente de desenvolvimento::

    pipenv install

Da pasta do projeto habilite o ambiente virtual::

    pipenv shell

Baixe a versão do chromedriver correspondente à sua versão do Chrome::

    python -m chromedriver_autoinstaller.utils

Defina as variáveis de ambiente necessárias::

    set MRH_USUARIO=USUARIO_DE_TESTES_DO_MENTORH

    set MRH_SENHA=SENHA_DO_USUARIO_DE_TESTES_DO_MENTORH

    set MRH_USUARIO_NOME=NOME_DO_USUARIO_DE_TESTES_DO_MENTORH

Então execute::

    pytest