from datetime import datetime
from model.scoopy import Scoopy
import asyncio
import json

def main():

    scoopy = Scoopy()


    while True:

        # Take input
        query = input("\n\nYou: ")

        # Thread logic here, maybe

        try:
            scoopy.query(query)
        except Exception as e:
            print(f"[!] Error querying Scoopy! ({e})")
            continue

if __name__ == "__main__":
    main()

