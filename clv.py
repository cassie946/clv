import pandas as pd
import numpy as np


df =pd.read_csv('orders.txt',sep='\t',encoding="ISO-8859-1",parse_dates=['orderdate'])
print(df.columns)
print(df.dtypes)

margin = 0.05
ac = 1
#ltv-=margin *avg order *freq/churn+ac

#avg order
#orderid =number of transaction
customers = df.groupby('customerid').agg({'orderdate':lambda x: (x.max() -x.min()).days,
                                          'totalprice':lambda x: x.sum(),
                                          'orderid' : lambda x: len(x) })

retention = customers[customers['orderid'] >1].shape[0]/ customers.shape[0]
customers = customers[customers['orderdate'] >0]
avg_order = customers['totalprice'].sum() / customers['orderid'].sum()
freq =  customers['orderdate'].sum()/customers['orderid'].sum()


print(customers)
print(f' avg_order: {avg_order} and freq: {freq}')
print (margin *avg_order *freq/(1-retention)+ac)
