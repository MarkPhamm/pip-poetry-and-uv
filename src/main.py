import pandas as pd
import duckdb

def load_data():
    # sample pandas DataFrame
    df = pd.DataFrame({"id": [1,2,3,4], "value": [10,20,30,40]})
    return df

def query_data(df: pd.DataFrame):
    con = duckdb.connect()        # in-memory by default
    # register DataFrame as a table
    con.register("t", df)
    # run SQL
    result = con.execute("SELECT id, value, value*2 AS value2 FROM t WHERE value >= 20 ORDER BY id DESC").df()
    return result

if __name__ == "__main__":
    df = load_data()
    print("Input:\n", df)
    out = query_data(df)
    print("Result:\n", out)