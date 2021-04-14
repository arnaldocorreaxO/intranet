#!/bin/bash
#Script para iniciar la Intranet
echo "Exportando PATH's..."
INFORMIXDIR=/opt/IBM/Informix_Client-SDK;export INFORMIXDIR
LD_LIBRARY_PATH="$INFORMIXDIR/lib:$INFORMIXDIR/lib/cli:$INFORMIXDIR/lib/esql";export LD_LIBRARY_PATH
PATH="$LD_LIBRARY_PATH:$INFORMIXDIR/bin:$PATH"
export PATH
echo "Arrancando Server..."
/home/intranet/.venv/bin/python /home/intranet/ProyectoINC/proIntranet/manage.py runserver 10.130.10.121:80
#python manage.py runserver 10.130.10.121:80
