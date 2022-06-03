#!/bin/bash

flask db init
flask db migrate -m "Primeiro migrate -> Criando tabelas de Colaboradores e Cargos"
flask db upgrade