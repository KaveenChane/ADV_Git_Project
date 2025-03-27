#!/bin/bash

# Nom du fichier CSV
FILE="data.csv"

# Écrire l'en-tête si le fichier n'existe pas
if [ ! -f "$FILE" ]; then
    echo "timestamp,price_eur" >> "$FILE"
fi

# Boucle infinie avec récupération toutes les 10 secondes
while true; do
    # Récupérer l'horodatage au format ISO (ex: 2025-03-27T15:22:01)
    timestamp=$(date -Iseconds)

    # Récupérer le prix spot BTC en euros depuis ABC Bourse
    price=$(curl -s https://www.abcbourse.com/cotation/BTCUSDu \
      | grep -oP '<span id="lastcx"[^>]*>\K[^<]+' \
      | sed 's/&#xA0;//g' \
      | tr -d ' ' \
      | sed 's/,/./')

    # Vérifier qu'on a bien un prix (sinon ne pas écrire de ligne vide)
    if [[ $price =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        echo "$timestamp,$price" >> "$FILE"
        echo "[OK] $timestamp - Prix BTC : $price €"
    else
        echo "[ERREUR] $timestamp - Impossible de récupérer le prix"
    fi

    # Attendre 10 secondes
    sleep 10
done
