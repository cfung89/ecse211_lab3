#! /bin/bash

set -euo pipefail

project="ecse211_lab3"

username="pi"
remote="192.168.50.5"
hostname="$HOSTNAME"

validate_hostname() {
    if [ -z "$hostname" ]; then
        hostname=$(uname -n)
        if [ -z "$hostname" ]; then
            echo "Error: No machine hostname."
            exit 1
        fi
    fi
}

if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    echo "Send files to RaspberryPi"
    echo "setup.sh [ -h | --help ]" "Help menu."
    echo "setup.sh [ --setup ]" "Setup SSH keys."
    echo "setup.sh [ --delete ]" "Delete SSH setup."
    echo "setup.sh [ filenames ]" "Send all files to the project repository."

elif [[ "$1" == "--setup" ]]; then
    validate_hostname
    echo "Setting up SSH key."
    if [ -z $USER ]; then
        echo "Error: No machine username."
        exit 1
    fi
    ssh-keygen -f "/home/$USER/.ssh/dpm_$hostname" -N ""
    echo ""
    ssh-copy-id -i "/home/$USER/.ssh/dpm_$hostname.pub" "$username@$remote"
    echo "SSH key successfully set up."

elif [[ "$1" == "--delete" ]]; then
    validate_hostname
    rm "/home/$USER/.ssh/dpm_$hostname"
    rm "/home/$USER/.ssh/dpm_$hostname.pub"
    echo "Remember to delete the corresponding public key from ~/.ssh/authorized_keys from the RaspberryPi."

else
    validate_hostname
    if [ -f "/home/$USER/.ssh/dpm_$hostname" ]; then
        eval "$(ssh-agent -s)"
        ssh-add "/home/$USER/.ssh/dpm_$hostname"
    fi
    for arg; do
        ssh "$username@$remote" "rm -rf /home/$username/Documents/teamate/$project/$arg"
        scp -r $arg "$username@$remote:/home/$username/Documents/teamate/$project/$arg"
    done
fi
