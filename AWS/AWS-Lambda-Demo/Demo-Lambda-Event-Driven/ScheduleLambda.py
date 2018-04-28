
# coding: utf-8

from __future__ import print_function
import psycopg2
import logging


def connector():
#Set DB Account & Password for Redshift
	redshift_endpoint = "your endpoint"
	redshift_user = "your user name"
	redshift_pass = "your pswd"
	port = 1234
	DB = "dbname"
	connector.aws_key = 'key'      
	connector.aws_secret = "secret"
    
    connector.con = psycopg2.connect(dbname=DB,host=redshift_endpoint,port=port,user=redshift_user,password=redshift_pass)
    connector.cur = connector.con.cursor()





def handler(event, context):

    connector()

    columns = """
				 column_1
				,column_2
              """

    ETL = """
            CREATE TEMP TABLE #aggregate_table
            AS
            SELECT {0},1 AS branch
            FROM db.branch_1.table

            UNION ALL

            SELECT {0},2 AS branch
            FROM db.branch_2.table

            UNION ALL

            SELECT {0},3 AS branch 
            FROM db.branch_3.table;
          """.format(columns)


    select = "SELECT * FROM #aggregate_table"


#Allow to overwrite the record
    UNLOAD = """ 
             unload ('%s')
             to 's3://bucket/folder1/sub-folder/prefix-' 
             ACCESS_KEY_ID '%s'
             SECRET_ACCESS_KEY '%s'
             delimiter as '|' addquotes ESCAPE ALLOWOVERWRITE gzip;
             """%(select,connector.aws_key,connector.aws_secret)
    try:
        connector.cur.execute(ETL)
        connector.cur.execute(UNLOAD)
        connector.con.commit()
        print('Unload successfully!! Staging table was saved to s3://bucket/folder1/sub-folder/prefix-')

#Log the error into AWS Cloudwatch and rollback the SQL Transaction
    except Exception:
        logging.exception("Errors at main function") 
        connector.con.rollback()

    connector.cur.close()
    connector.con.close()