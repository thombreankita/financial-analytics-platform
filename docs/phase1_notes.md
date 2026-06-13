PaySim Data set:
This data set has data regarding the financial transations, details of the transactions and whether or not the transactions is fraud or not. Following are the columns of this data set.
Step: This column stores the is a time unit in which the transaction was completed. Here 1 step means 1 hour.
Type: This columnstores what type/kind of transaction was carried out.
Amount: This column stores the amount of money that was used for that particular transaction.
nameOrig : This column states the name or identity of the account that has initiated the transacton.
oldbalanceOrg: The original amount present in the account before the transaction initiated was stored in this column
newbalanceOrig: Stores the amount in the source account after the transaction is completed.
nameDest: States the destination account
oldbalanceDest: Stores the amount of money present in thedestination account prior to transaction
newbalanceDest :Stores the amount of money present in thedestination account after the transaction is completed
isFraud: States if the transaction is fraudulent or not.
isFlaggedFraud: States whether a fraudulent transactions is actually flagged as fraud or not mapped correctly.

Examples of bad data for PaySim Dataset:
1. If the type is stored as credit for ex. but the amount in destination account is getting deducted.
2. Incorrect data stored in the columns. i.e. type column has name of account 
3. Records with blank values for few columns i.e.no transaction types are mentioned or amount or destname column of any record are null.
4. The amount column is having 0 or negative value.
5. If the values in nameDest and nameOrig are same
6. The initial amount in source account is less than the amount column for debit transaction types.

Partitioned Output:
Partitioned Output means that we have processed and cleaned the data and also have it segregated based on the key attribute of the data. In case of PaySim db, The transaction type isan important attribute for this data. Thus we clean the data and store it as per the transaction type of the records. This can be helpful in cases where we only want to deal and use a specific partition, we willsimply apply the transformations on that partitioned set of data insted of applying it on the entire dataset. Moreover,  partitioning also improves pipeline reliability. If the CASH_OUT transformation fails, PAYMENT data is unaffected. 

The difference between isFraud and isFlaggedFraud:
The isFlaggedFraud column tells us that in this dataset whether or not the actually fraud transactions are marked as fraud or not. Meaning does any of the fraud transaction is actually marked as fraud or not is shown in this column. isFraud column marks the fraud transactions.
isFraud marks whether a transaction is actually fraudulent — 8213 transactions in this dataset are confirmed fraud. isFlaggedFraud marks whether the system detected and flagged the transaction as suspicious — only 16 transactions were flagged. This means the fraud detection system missed 8197 genuine fraud cases, catching less than 0.2% of actual fraud. This gap between isFraud and isFlaggedFraud is what makes this dataset interesting for building better fraud detection models

validation checks for this dataset wolud be as follows:
1. Amount > 0. mark it a flag if amount <=0
2. if transaction type = transfer and destination new balance <  destination old balance flag it. {For TRANSFER type: if newbalanceDest is less than or equal to oldbalanceDest, flag it — money should have arrived in the destination account}
3. Flag nullvalues in  any important columns like Flag null values in: step, type, amount, nameOrig, nameDest, isFraud
4. Source account != destination account
5. if transaction type = debit and source old balance < amount flag it
6. If type is not one of these ['PAYMENT' 'TRANSFER' 'CASH_OUT' 'DEBIT' 'CASH_IN'] flag it