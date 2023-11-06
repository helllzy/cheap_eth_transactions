from sys import platform
from asyncio import WindowsSelectorEventLoopPolicy, set_event_loop_policy, run
from random import randint, sample, shuffle, choice

from termcolor import cprint

from modules.account import Account
from modules.modules import Module
from data.data import WALLETS, HELZY
from modules.utils import write_to_csv, sleeping, logger
from config import (
    ACTIONS_DELAY,
    MODULES,
    EXTRA_MODS_COUNT,
    EXTRA_MODULES,
    EXTRA,
    ACCS_DELAY,
    RANDOMIZE_WALLETS,
    EXACT_NONCE,
    EXACT_NONCE_COUNT
)

    
async def main():
    raws = list(WALLETS.keys())

    if RANDOMIZE_WALLETS:
        shuffle(raws)

    for raw_id, raw in enumerate(raws, start=1):
        try:
            account = Account(wallet=WALLETS[raw], id=raw_id)
        except:
            logger.critical(raw_id, 'PROXY ERROR', sep=" | ")
            continue

        logger.debug(f"{raw_id} | Working on: {account.address}")

        if EXACT_NONCE:
            random_nonce = randint(*EXACT_NONCE_COUNT)
            acc_nonce = await account.w3.eth.get_transaction_count(account.address)
            if random_nonce < acc_nonce:
                logger.debug(f'{raw_id} | wallet nonce: {acc_nonce} > random nonse: {random_nonce}')
                continue

        ALL_MODULES = MODULES.copy()

        shuffle(ALL_MODULES)

        if EXTRA:
            ALL_MODULES += sample(EXTRA_MODULES, randint(*EXTRA_MODS_COUNT))

        modules = Module(account=account)

        for mod_id, module in enumerate(ALL_MODULES, start=1):
            status = await modules.start(module)

            if status == 0:
                await write_to_csv(account.address, 'doesn`t have enough ETH')
                break

            await write_to_csv(account.address, status)
            
            if len(ALL_MODULES) != mod_id:
                await sleeping(ACTIONS_DELAY, 'Sleeping between modules', 'yellow')

        if len(raws) != raw_id:
            await sleeping(ACCS_DELAY, 'Sleeping between wallets', 'yellow')
        else:
            logger.success('All wallets were processed')


if __name__ == '__main__':
    cprint(choice(HELZY), choice(['green', 'magenta', 'light_cyan']))

    if platform.startswith("win"):
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    run(main())
