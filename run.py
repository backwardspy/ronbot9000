import os

from bot import ronbot9000

token = os.getenv("TOKEN")

if __name__ == "__main__":
    ronbot9000.run(token)
