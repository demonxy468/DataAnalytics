# coding: utf-8

import psycopg2
import logging

def load_StagingTable(aws_key,aws_secret,cur):
    #Unstaging Process
    columns = """
				 column_1
				,column_2
				!3243;I am the error ..(*)&^(@) -- define a SQL syntax error below for the demo
			  """
 
	#take data files from S3 staging bucket
    COPY =  """
                 COPY  db.schema1.table1  (%s)
                 FROM 's3://bucket/staging/sub-folder/' 
                 ACCESS_KEY_ID '%s' SECRET_ACCESS_KEY '%s' 
                 DELIMITER '|' IGNOREHEADER 1 EMPTYASNULL REMOVEQUOTES FILLRECORD 
                 acceptanydate acceptinvchars timeformat 'auto' ESCAPE gzip;
            """%(columns,aws_key,aws_secret)

    cur.execute(COPY)

    
def unstaging(cur):    
	#Define an upsert operation to update Redshift
    DeleteMktPlc = """
                      DELETE 
                         table_A 
                      FROM
                         staging.B T2
                      WHERE
                         DB.table_A.id = T2.id AND DB.table_A.userid = T2.userid;
                   """


    INSERT =    """
                   INSERT INTO DB.table_A 
                   SELECT * FROM staging.B
                """
    
    DeleteStg = """
                  DELETE FROM staging.B 
                """

    cur.execute(DeleteMktPlc)
    cur.execute(INSERT)
    cur.execute(DeleteStg)

    

    
def unload_S3(aws_key,aws_secret,cur):
    #Allow to overwrite the record
    SELECT = "SELECT * FROM table_A"
    
    UNLOAD = """ 
             unload ('%s')
             to 's3://bucket/production/sub-folder/prefix-' 
             ACCESS_KEY_ID '%s'
             SECRET_ACCESS_KEY '%s'
             delimiter as ';' addquotes ESCAPE ALLOWOVERWRITE gzip;
             """%(SELECT,aws_key,aws_secret)
    
    cur.execute(UNLOAD)


def connector():
    #Set DB Account & Password for Redshift
    redshift_endpoint = "endpoint"
    redshift_user = "user"
    redshift_pass = "pass"
    port = 1234
    DB = "DB"
    connector.aws_key = 'aws_key'      
    connector.aws_secret = "aws_secret"
    
    connector.con = psycopg2.connect(dbname=DB,host=redshift_endpoint,port=port,user=redshift_user,password=redshift_pass)
    connector.cur = connector.con.cursor()



def handler(event, context):
#handler serves as main function to execute all the functions
    connector()

    try: 
        load_StagingTable(connector.aws_key,connector.aws_secret,connector.cur)
        unstaging(connector.cur)
        unload_S3(connector.aws_key,connector.aws_secret,connector.cur)
        connector.con.commit()
#Detect the error detail and log the error to AWS Cloudwatch
    except Exception:
        logging.exception("Errors at main function") 
        connector.con.rollback()

    connector.cur.close()
    connector.con.close()