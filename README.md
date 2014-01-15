AutoCog is a tool to assess how well an Android application description reveal the security-concerned permission in semantics level. Based on our learning approach, the tool leverages large-scale of Android applications and descriptions to generate a Description-to-Permission Relatedness (DPR) Model (semantic patterns and permission with high correlation). 

Prerequest:
nltk package python: http://nltk.org
ESAlib: https://github.com/ticcky/esalib

To Use it:
setup the ESAlib
cp neweval_0103.jar and neweval_0103.jar_lib in src/ to /semant2/esalib
go to dir: /semant2/esalib
java -jar neweval_0103.jar noskip(skip) PERMISSION

parameter: noskip - scan the whole description to identify all the pairs of verb and noun phrase revealing the target permission
	     skip - once a pair of verb and noun phrase revealing the target permission is identified, the description is skipped, for the efficiency of measurement of the Permission-to-description fidelity of the current android market.

Example: java -jar neweval_0103.jar noskip READ_CONATCTS


Permissions covered:

WRITE_EXTERNAL_STORAGE
ACCESS_FINE_LOCATION 
ACCESS_COARSE_LOCATION  
RECEIVE_BOOT_COMPLETED
GET_ACCOUNTS
CAMERA    
WRITE_SETTINGS
READ_CALENDAR           
RECORD_AUDIO            
READ_CONTACTS                                         
WRITE_CONTACTS


If you want to generate your own description-to-permission relatedness model:
(1) Find the potential noun phrase correlated with the permission by runing scripts/potentialNP.py

(2) Select the top-k noun phrases (sorted by our metrics) by running scripts/selecttopkNP.py

(3) Pair the top-k noun phrases with verb by running scripts/findverbNP.py

(4) Get the DPR model by running scripts/checkvNP.py

