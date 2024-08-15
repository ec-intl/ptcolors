#!/bin/bash

# Post installation script for an ECI Container

# 1. Install dotfiles from Company repository if the directory does not exist
if [ -d /home/"${USER}"/dotfiles ]; then
    echo "Dotfiles already exist. Skipping installation."
else
    echo "Installing dotfiles..."
    cd /home/"${USER}" || exit
    git clone https://github.com/ec-intl/dotfiles.git
    pushd dotfiles || exit
    ./install bash
    popd || exit

  # 2. Install python packages
  export PATH="/home/${USER}/.local/bin:${PATH}"
  # shellcheck disable=SC1091
  . /venv/bin/activate

  # 3. Copy custom bash dotfiles
  cp -r /tmp/bash-src /home/"${USER}"/
fi
# 4. Print a message letting the user know the container is ready
echo "Container setup complete. Happy coding!"