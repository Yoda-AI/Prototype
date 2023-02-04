import pandas as pd
import yoda as yp

df = pd.read_csv("weatherHistory.csv", sep=',')
yoda = yp.Yoda(df).prepare()
yoda.run_webserver()
