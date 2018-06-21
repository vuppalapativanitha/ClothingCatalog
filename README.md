# Item Catalog Web App
##By Vanitha Vuppalapati
This web app is a project for the Udacity [FSND Course]
(https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About
This project is a RESTful web application utilizing the Flask framework. 
It also accesses a SQL database that populates categories and their items. 
OAuth2 provides authentication for further CRUD functionality on the application. 
Currently OAuth2 is implemented for Google Accounts.

## Skills Required
1. Python
2. HTML
3. CSS
4. OAuth
5. Flask Framework
  
### How to Run?

#### PreRequisites
  * [Python ~2.7](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)
  
#### Launch Project
  1. Launch the Vagrant VM using command:
  
  ```
    $ vagrant up
  ```
  2. Run your application within the VM
  
  ```
    $ python /vagrant/catalog/main.py
  ```
  3. Access and test your application by visiting [http://localhost:8000](http://localhost:8000).

*Optional step(s)

## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Item-Catalog'
7. Authorized JavaScript origins   = 'http://localhost:5000'
8. Authorized redirect URIs = 'http://localhost:5000/' && 'http://localhost:5000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `clientid` in apps.js
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secret.json
13. Place JSON file in ClothingCatalog directory 
14. Run application

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).
