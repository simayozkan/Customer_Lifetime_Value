#Customer Lifetime Value
#The dataset is not shared because it's exclusive to Miuul Data Science Bootcamp
#Online Store

#Variables :
#InvoiceNo: Invoice number. "C" means returned
#StockCode: Product code
#Description: Product name
#Quantity: Product number
#InvoiceDate: Invoice date and time
#UnitPrice: Product price
#CustomerID: Unique customer number
#Country: Country name (Where customer live)



import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df_ = pd.read_excel("datasets", sheet_name="Year 2009-2010")

#Copy of dataframe
df = df_.copy()

#First look to dataframe
df.head()

#Check for null values
df.isnull().sum()

#"C" represents returned invoices. Do not include in the dataset for furher research
df = df[~df["Invoice"].str.contains("C", na=False)]

#Take Quantity which more than 0
df = df[(df["Quantity"] > 0)]

#Drop null values
df.dropna(inplace=True)

#Create "Total Price"
df["TotalPrice"] = df["Quantity"] * df["Price"]

#Customer lifetime value format
cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})

#Change variable names
cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']

#Average Order Value (average_order_value = total_price / total_transaction)
cltv_c.head()

cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

#Purchase Frequency (total_transaction / total_number_of_customers)
cltv_c.head()

#Total number of customers
cltv_c.shape[0]

cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]


#Repeat Rate & Churn Rate (Number of customers who made multiple purchases / All customers)

#More than one purchase
repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]

churn_rate = 1 - repeat_rate

#Profit Margin (profit_margin =  total_price * 0.10)
cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10

#Customer Value (customer_value = average_order_value * purchase_frequency)
cltv_c['customer_value'] = cltv_c['average_order_value'] * cltv_c["purchase_frequency"]

#Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]

cltv_c.sort_values(by="cltv", ascending=False).head()

#Creating Segments
cltv_c.sort_values(by="cltv", ascending=False).tail()

cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

cltv_c.sort_values(by="cltv", ascending=False).head()

cltv_c.groupby("segment").agg({"count", "mean", "sum"})

cltv_c.to_csv("cltc_c.csv")

#All process is functionalized

def create_cltv_c(dataframe, profit=0.10):


    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe['Quantity'] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                                   'Quantity': lambda x: x.sum(),
                                                   'TotalPrice': lambda x: x.sum()})
    cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']

    cltv_c['avg_order_value'] = cltv_c['total_price'] / cltv_c['total_transaction']

    cltv_c["purchase_frequency"] = cltv_c['total_transaction'] / cltv_c.shape[0]

    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate

    cltv_c['profit_margin'] = cltv_c['total_price'] * profit

    cltv_c['customer_value'] = (cltv_c['avg_order_value'] * cltv_c["purchase_frequency"])

    cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']

    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c


df = df_.copy()

clv = create_cltv_c(df)
