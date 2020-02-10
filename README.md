# Invoice Upload BackEnd

## Getting Started

### Setup
### Create Database
```
    $ sudo su postgres
    $ psql`
    postgres=# CREATE DATABASE dbname;
    postgres=# \q
    $ exit

```
### Clone the repo
``` $ git clone git@github.com:Philipotieno/Invoice-API.git
```
### Installing Dependencies
#### Python 3.6
 - cd into the Incoice-API folder and create a virtual environment
 ``` $ virtualenv -p python3 name_of_virtualenvironment
 ```
 - Activate the vitual environment
 ```
    $ source name_of_virtualenv/bin/activate
 ```
 - install dependancies
 ```
    $ pip install -r requirements.txt
 ```
- Then add a .env file as shown in the following .env_sample
  ```
   $ source .env
   ```
- To run the server
```
 $ flask run --reload
```
- Create tables  :
```
    $ python manage.py create_tables

```

## Endpoints...
```
    localhost:5000
    heroku: https://capstone-philip.herokuapp.com/
```
### POST '/invoices'

- Upload a new csv file and read data
- CSV must have all the headers required for a succesfull upload

- Body
![Uploadbody](https://github.com/Philipotieno/Invoice-API/blob/upload-invoice-csv/images//upload.png)
 
- Returns
![Returns](https://github.com/Philipotieno/Invoice-API/blob/upload-invoice-csv/images/returnsupload.png)

### GET '/invoices/topcustomers'

- Gets invoices of top five customers acording to the amount due
- Returns
![Returns](https://github.com/Philipotieno/Invoice-API/blob/upload-invoice-csv/images/topcustomers.png)

### GET '/invoices/transactions'
- This route returns the last 30 transactions
- Date must be of the formt %Y-%m-%d

- Body
![dateBody](https://github.com/Philipotieno/Invoice-API/blob/upload-invoice-csv/images/transactions.png)

- Returns
![returns transactions](https://github.com/Philipotieno/Invoice-API/blob/upload-invoice-csv/images/transactions.png)
### GET '/invoices/summary'
- This route returns a summary of total amount incurred for each month in every year

- Returns
![Returns](https://github.com/Philipotieno/Invoice-API/blob/upload-invoice-csv/images/summary.png)


- To drop tables  :
```
    $ python manage.py drop_tables

```