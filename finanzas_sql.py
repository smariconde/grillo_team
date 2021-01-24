from sqlalchemy import create_engine

def getEarningsDate(symbol):
    try:
        sql_engine = create_engine('mysql+pymysql://root:@34.66.111.107/finanzas')
        sql_conn = sql_engine.connect()
        q = f"SELECT earnings FROM finviz WHERE symbol = '{symbol}' ORDER BY created_at DESC"
        earnings = sql_conn.execute(q).fetchone()
        sql_conn.close()
    except:
        raise

    return earnings