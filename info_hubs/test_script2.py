import requests

url = "https://www.theamericanconservative.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print(response.text)
else:
    print("Error: Unable to retrieve HTML content from URL")


# version: 2.1
#
# workflows:
#     version: 1
#     build:
#       jobs:
#         - build:
#             filters:
#               branches:
#                 only:
#                   - main
#
# jobs:
#   build:
#     working_directory: ~/Information-hub
#     docker:
#       - image: circleci/node:10.16.3
#     steps:
#       - checkout
#       - run:
#           name: update-npm
#           command: 'sudo npm install -g npm@5'
#       - restore_cache:
#           key: dependency-cache-{{ checksum "package-lock.json" }}
#       - run:
#           name: install-npm
#           command: npm install
#       - save_cache:
#           key: dependency-cache-{{ checksum "package-lock.json" }}
#           paths:
#             - ./node_mdodules
#   deploy:
#     docker:
#       - image: circleci/node:10.16.3
#     steps:
#       - run:
#           name: deploy-application
#           command: ssh -o StrictHostKeyChecking=no $EC2_USERNAME@EC2_PUBLIC_DNS "rm -rf Information-hub;git clone https://github.com/Aflynn987/Information-hub.git; source Information-hub/deploy.sh"


# #!/usr/bin/env bash
# sudo apt update && sudo apt install nodejs npm
# # Install pm2 which is a production process manage for Node.js with a built-in load balancer.
# sudo npm install -g pm2
# # stop any instance of our application running currently
# pm2 stop example_app
# # change directory into folder where application is downloaded
# cd Information-hub/
# # Install application dependencies
# npm install
# # Start the application with the process name example_app using pm2
# pm2 start ./bin/ww --name information-hub