#! /bin/bash

MYSQL_HOST=34.173.227.59

mysql -h $MYSQL_HOST -u root -p  classicmodels < ./mysqlsampledatabase.sql