# Fraud Detection Data Dictionary

| Fields | Description |
| :--- | :--- |
| **step** | Maps a unit of time in the real world (1 step = 1 hour of time). |
| **type** | The categorization of the transaction (CASH_IN, CASH_OUT, DEBIT, PAYMENT, or TRANSFER). |
| **amount** | The total monetary amount of the transaction in local currency. |
| **nameOrig** | The unique identifier of the customer who started the transaction. |
| **oldbalanceOrg** | The initial balance of the sender before the transaction occurred. |
| **newbalanceOrig** | The new balance of the sender after the transaction concluded. |
| **nameDest** | The unique identifier of the customer who is the recipient of the transaction. |
| **oldbalanceDest** | The initial balance of the recipient before the transaction occurred. |
| **newbalanceDest** | The new balance of the recipient after the transaction concluded. |
| **isFraud** | The target variable indicating actual fraudulent transactions (1 = Fraud, 0 = Clean). |
| **isFlaggedFraud** | A legacy internal system flag indicating massive transfers (often >200,000). |
| **errorBalanceOrig** *(Engineered)* | Advanced feature tracking structural inconsistency in the sender's accounting loop. |
| **errorBalanceDest** *(Engineered)* | Advanced feature tracking structural inconsistency in the receiver's accounting loop. |
| **hour_of_day** *(Engineered)* | Advanced feature extracting the precise hour of the day to detect anomalous timing patterns. |
