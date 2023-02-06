import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import yoda as yp

df = pd.read_csv(f"{os.path.dirname(os.path.abspath(__file__))}/weatherHistory.csv", sep=',')
yoda = yp.Yoda(df).prepare()
yoda.run_webserver()
