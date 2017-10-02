#!/bin/bash
case $1 in
    "pg" )
        case $2 in
            "i" )
                pip install git+https://github.com/CrimsonVista/Playground3.git@master
                exit
            ;;

            "u" )
                pip install git+https://github.com/CrimsonVista/Playground3.git@master --upgrade
                exit
            ;;

            * ) echo "Incorrect args"
        esac
        exit
    ;;

    "run" )
        case $2 in
            "test" )
                python -m netsec_fall2017.lab_$3.submission
                exit
            ;;

            "server" )
                python -m netsec_fall2017.lab_1d.server
                exit
            ;;

            "client" )
                if [[ $# == 2 ]]
                then
                    mode="26.1.22.9"
                else
                    mode=$3
                fi
                python -m netsec_fall2017.lab_1d.client ${mode}
                exit
            ;;

            * ) echo "Incorrect args"
        esac
        exit
    ;;

    * ) echo "Incorrect args"

esac