import pandas as pd
from datetime import datetime
import os


#path = "/home/kaveen/Documents/ESILV_A4/Final_project/ADV_Git_Project/"
path = "/home/ec2-user/ADV_Git_Project/"

try:
    df = pd.read_csv(f"{path}data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[df['timestamp'].dt.date == datetime.today().date()]

    if len(df) >= 2:
        open_price = df.iloc[0]['price_eur']
        close_price = df.iloc[-1]['price_eur']
        min_price = df['price_eur'].min()
        max_price = df['price_eur'].max()
        mean_price = df['price_eur'].mean()
        volatility = df['price_eur'].std()
        evolution = ((close_price - open_price) / open_price) * 100

        output = pd.DataFrame([{
            "date": datetime.today().strftime("%Y-%m-%d"),
            "open": open_price,
            "close": close_price,
            "min": min_price,
            "max": max_price,
            "mean": mean_price,
            "volatility": volatility,
            "evolution_percent": evolution
        }])

        if os.path.exists(f"{path}daily_report.csv"):
            existing = pd.read_csv(f"{path}daily_report.csv")
            existing = existing[existing['date'] != output.iloc[0]['date']]
            output = pd.concat([existing, output], ignore_index=True)

        output.to_csv(f"{path}daily_report.csv", index=False)
        print("Rapport quotidien mis à jour.")
    else:
        print("Pas assez de données pour générer le rapport.")

except Exception as e:
    print(f"Erreur lors de la génération du rapport quotidien : {e}")
