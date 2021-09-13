# This script isn't inteded to be run directly, but sourced
#   $ source mega.sh
# The functions herein act like commands to execute the utility

# ref:
# https://manpages.ubuntu.com/manpages/bionic/man7/megatools.7.html

MEGA_DIR=$(readlink -f $PWD)
DUMP_DIR=$(readlink -f ~/Downloads/mega_dls)
DOCKER_IMAGE="aenygma/megatools"

DOCKER_PREFIX="docker run --rm -it -v $MEGA_DIR/.megarc:/.megarc 
    -v $DUMP_DIR:/dump $DOCKER_IMAGE"

dbuild(){
    docker build -t $DOCKER_IMAGE .
}

minfo(){
    echo "> Configs <"
    echo "> MEGA_DIR: $MEGA_DIR"
    echo "> DUMP_DIR: $DUMP_DIR"
}

megadl(){
    # gateway for mega cli

   echo "> $DOCKER_PREFIX $@"
   $DOCKER_PREFIX megadl --path /dump "$@"
}

deactivate() {
    # undo
    unset MEGA_DIR
    unset DOCKER_PREFIX

    unset minfo
    unset megadl
    unset deactivate
}
