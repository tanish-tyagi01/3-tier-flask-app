#!/bin/bash

#cloning the code

code_clone() {
	if [ -d "3-tier-flask-app" ]; then
		echo "Directory already exists!"
	else 
		git clone "https://github.com/tanish-tyagi01/3-tier-flask-app" || {
			echo "failed to clone the code"
			return 1
		}
	fi
}

#Installing the requirements

install_requirements() {
	echo "Installing dependencies...."
	sudo apt update && sudo apt install docker.io nginx docker-compose-v2 || {
		echo "failed to install dependencies"
		return 1
	}
}


#function to  perform required restarts
required_restarts() {
	sudo chown "$USER" /var/run/docker.sock || {
		echo "failed to change ownership"
		return 1
	}
}

#function to Deploy flask app
deploy() {
	docker build -t flask_image . && docker compose up -d || {
		echo "failed to deploy the app"
		return 1
	}
}


# Main deployment script
echo "********** DEPLOYMENT STARTED *********"

if ! code_clone; then
	cd 3-tier-flask-ap || exit 1
fi

if !  install_requirements; then
	exit 1
fi

if ! required_restarts; then
	exit 1
fi

if ! deploy; then
	echo "Deployment failed. Mailing the admin..."
	exit 1
fi

echo "********** DEPLOYMENT DONE *********"
