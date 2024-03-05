import sqlite3
import pandas as pd

tidy_finance_python = sqlite3.connect( database="/Users/asbjornfyhn/Desktop/Emp Fin/data/tidy_finance_python.sqlite")

crsp_monthly = (
    pd.read_sql_query(sql=("SELECT * FROM crsp_monthly"),
                        con=tidy_finance_python, parse_dates={"month"})
                        .dropna()
)

crsp_monthly

db_conn = sqlite3.connect("/Users/asbjornfyhn/Desktop/superstore.db")
c = db_conn.cursor()

c.execute(
    """
    drop TABLE Test ;
    """
)
db_conn.commit()
db_conn.close()
db_conn = sqlite3.connect("/Users/asbjornfyhn/Desktop/superstore.db")
testDataset = (crsp_monthly
               .iloc[:3000]
               [['date','mktcap','altprc','ret_excess']]
               .set_index('date')
               .stack()
               .reset_index()
               .rename(columns={'level_1':'value_id',0:'value'})
               )
testDataset.to_sql(name='test',con=db_conn,if_exists='replace',index=False)

crsp_monthly[['date','mktcap','altprc','ret_excess']].iloc[:1048576].to_excel('/Users/asbjornfyhn/Desktop/superstore.xlsx')

import time

start_time = time.perf_counter()  # Start time before the query

df = pd.read_excel('/Users/asbjornfyhn/Desktop/superstore.xlsx')

end_time = time.perf_counter()  # End time after the query

total_time = end_time - start_time

print(f"Data retrieval took {total_time:.4f} seconds")



testDataset = (crsp_monthly
               .iloc[3000:]
               [['date','mktcap','altprc','ret_excess']]
               .set_index('date')
               .stack()
               .reset_index()
               .rename(columns={'level_1':'value_id',0:'value'})
               )
#9,282,108
testDataset.to_sql(name='test',con=db_conn,if_exists='append',index=False)

import time

start_time = time.perf_counter()  # Start time before the query

df = pd.read_sql_query('select * from test', con=db_conn)

end_time = time.perf_counter()  # End time after the query

total_time = end_time - start_time

print(f"Data retrieval took {total_time:.4f} seconds")

9291108-9282108