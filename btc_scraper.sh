#!/bin/bash

PROJECT_DIR= "/home/ec2-user/ADV_Git_Project/"

FILE="$PROJECT_DIR/data.csv"

# Si le fichier n'existe pas, ajouter l'en-tête
if [ ! -f "$FILE" ]; then
    echo "timestamp,price_eur" >> "$FILE"
fi

timestamp=$(date -Iseconds)

price=$(curl -s https://www.abcbourse.com/cotation/BTCUSDu \
  | grep -oP '<span id="lastcx"[^>]*>\K[^<]+' \
  | sed 's/&#xA0;//g' \
  | tr -d ' ' \
  | sed 's/,/./')

if [[ $price =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "$timestamp,$price" >> "$FILE"
    echo "[OK] $timestamp - Prix BTC : $price €"
else
    echo "[ERREUR] $timestamp - Impossible de récupérer le prix"
fi

