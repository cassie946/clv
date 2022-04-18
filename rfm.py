import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df_order =pd.read_csv('orders.txt',sep='\t',encoding="ISO-8859-1",parse_dates=['orderdate'])
df_customer  =pd.read_csv('customer.txt',sep='\t',encoding="ISO-8859-1")

#print(df_order.dtypes)
#print(df_customer.dtypes)

df_order =df_order[['orderid','customerid','orderdate','totalprice']]
df= df_order.merge(df_customer[['customerid','householdid']],left_on='customerid',right_on='customerid')
#print (df)
#print(df.groupby('householdid').agg({'orderid':lambda x: len(x)}))

df_1=df.groupby('householdid')['orderdate'].max().reset_index()
df_1.columns=[ ['householdid','max_date']]
df_1['recency']=(df_1['max_date'].max()-df_1['max_date']).apply(lambda x: x.dt.days)
#print(df_1)

import matplotlib.pyplot as plt
#看图看数据什么时候出现的最多
#plt.hist(df_1['recency'])
#plt.show(block=True)
#plt.interactive(False)

from sklearn.cluster import KMeans
''''
sse = {}


for n in range(1,10):
    kmeans = KMeans(n_clusters=n, random_state=0).fit(df_1['recency'].to_numpy())
    df_1['clusters'] = kmeans.labels_
    sse[n] =kmeans.inertia_ #面试考点：如何找到 kmeans n_cluster 里的n ? answer：找elbow，拐点

print(df_1)
print(sse.items())
plt.plot(sse.keys(),sse.values())
plt.show(block=True)
plt.interactive(False)
'''

kmeans = KMeans(n_clusters=4, random_state=0).fit(df_1['recency'].to_numpy())
df_1['recency_cluster'] = kmeans.predict(df_1['recency'].to_numpy())

df_1.columns = df_1.columns.get_level_values(0)

def order_cluster(cluster_field_name, target_field_name,df,ascending):

    df_new = df.groupby(cluster_field_name) [target_field_name].mean().reset_index()
    df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
    df_new['index'] =df_new.index
    df_final =pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
    df_final = df_final.drop([cluster_field_name],axis=1)
    df_final =df_final.rename(columns={"index":cluster_field_name})
    return df_final

df_orderd_by_recency = order_cluster('recency_cluster', 'recency',df_1,False)
print(df_orderd_by_recency)

