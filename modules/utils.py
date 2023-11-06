from random import randint, choice
from asyncio import sleep
import csv

from loguru import logger
from web3 import Web3

from config import MAX_GWEI, RETRIES_COUNT

logger.add('data/logs.log')


async def sleeping(secs, text=None, color="white") -> None:
    if text:
        await info(text, color)

    await sleep(randint(*secs))


async def info(text, color="white") -> None:
    logger.opt(colors=True).info(f'<{color}>{text}</{color}>')


def check_gas(func):
    async def _wrapper(*args, **kwargs):
        while True:
            try:
                w3 = Web3(
                     Web3.HTTPProvider(
                          choice(['https://ethereum.publicnode.com',
                                  'https://1rpc.io/eth',
                                  'https://rpc.ankr.com/eth'])))
                eth_gas_price = round(w3.from_wei(w3.eth.gas_price, 'gwei'), 2)

                if eth_gas_price > MAX_GWEI:
                    logger.warning(
                        f"gas`s {eth_gas_price} | sleep 30 seconds"
                        )
                    await sleep(30)
                else:
                    break

            except:
                pass

        return await func(*args, **kwargs)
    return _wrapper


def retry(func):
    async def _wrapper(*args, **kwargs):
        retries = 0

        while retries <= RETRIES_COUNT:
            try:
                return await func(*args, **kwargs)

            except Exception as error:
                error = str(error).lower()

                if 'insufficient funds' in error or 'gas required exceeds allowance' in error:
                    logger.error(f'doesn`t have enough ETH')
                    return 0
                else:
                    logger.error(f'error: {error}')
                    retries += 1
                    await sleep(30)

    return _wrapper


async def write_to_csv(address, result):
    with open('data/result.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['address', 'result'])
        writer.writerow([address, result])
