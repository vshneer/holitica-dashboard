import pandas as pd
import datetime as dt

def segment_customer(row):
    if row['R_Score'] >= 5 and row['F_Score'] >= 4:
        return 'VIP'
    elif row['R_Score'] >= 4 and row['F_Score'] >= 4:
        return 'Loyal'
    elif row['R_Score'] == 5:
        return 'Recent'
    elif row['F_Score'] >= 4:
        return 'Frequent'
    elif row['M_Score'] >= 4:
        return 'Big Spender'
    else:
        return 'Others'

def build_rfm(df, date_field, order_id_field, customer_id_field, monetary_field):
    snapshot_date = df[date_field].max() + dt.timedelta(days=1)
    # Group by CustomerID and aggregate
    rfm = df.groupby(customer_id_field).agg({
        date_field: lambda x: (snapshot_date - x.max()).days,  # Recency
        order_id_field: 'nunique',  # Frequency
        monetary_field: 'sum'  # Monetary
    })

    # Rename columns for clarity
    rfm.rename(columns={
        date_field: 'Recency',
        order_id_field: 'Frequency',
        monetary_field: 'Monetary'
    }, inplace=True)

    # Create R, F, M scores from 1 to 5
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    rfm['Segment'] = rfm.apply(segment_customer, axis=1)
    return rfm