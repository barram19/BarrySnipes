from datetime import datetime
from model.barry import Barry
import asyncio
import json

def main():

    barry = Barry()


    while True:

        # Take input
        query = input("\n\nYou: ")

        # Thread logic here, maybe

        try:
            barry.query(query)
        except Exception as e:
            print(f"[!] Error querying Barry! ({e})")
            continue

if __name__ == "__main__":
    main()

