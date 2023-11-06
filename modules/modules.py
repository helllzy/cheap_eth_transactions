from random import choice, uniform

from web3 import Web3

from modules.account import Account
from modules.utils import check_gas, retry, sleeping, logger
from config import ACTIONS_DELAY, ETH_FOR_TRANSFER, ETH_FOR_BLUR
from data.data import (
    BLUR_ADDRESS,
    DNA_ADDRESS,
    BUNGEE_ADDRESS,
    BLUR_ABI,
    BUNGEE_ABI
)


class Module:
    def __init__(self, account: Account):
        self.account = account
        self.dna_address = Web3.to_checksum_address(DNA_ADDRESS)
        self.blur_address = Web3.to_checksum_address(BLUR_ADDRESS)
        self.bungee_address = Web3.to_checksum_address(BUNGEE_ADDRESS)


    @retry
    @check_gas
    async def start(self, module: str, text: str = ''):
        match module:
            case 'bungee':
                tx = await self.bungee()
            case 'transfer':
                tx = await self.transfer()
            case 'blur':
                amount = uniform(*ETH_FOR_BLUR)
                tx = await self.blur(amount=amount)
                if tx:
                    await sleeping(
                        ACTIONS_DELAY, 'Sleeping between blur actions')
                    tx = await self.blur(amount=amount, mod='withdraw')
            case 'zerion_dna':
                tx = await self.zerion_dna()
            case _:
                text = f'WRONG MODULE: {module}'
                logger.error(text)
                return text

        text = module.capitalize()

        if tx:
            text += ' done'
            logger.success(f'{self.account.id} | {text}')
        else:
            text += ' failed'
            logger.error(f'{self.account.id} | {text}')

        return text
    

    async def bungee(self):

        contract = self.account.w3.eth.contract(
            abi=BUNGEE_ABI,
            address=self.bungee_address
        )
        
        match choice(['avalanche', 'polygon', 'gnosis']):
            case 'avalanche':
                chain_id = 43114
                amount = uniform(0.00035, 0.0005)
            case 'polygon':
                chain_id = 137
                amount = uniform(0.00006, 0.0001)
            case 'gnosis':
                chain_id = 100
                amount = uniform(0.000006, 0.00001)
        
        return await self.account.send_transaction(
            to=self.bungee_address,
            data=contract.encodeABI(
                'depositNativeToken', args=(chain_id, self.account.address)
                ),
            value=self.account.w3.to_wei(amount, "ether")
            )
    

    async def blur(self, amount, mod=None):
        amount = self.account.w3.to_wei(amount, "ether")

        if not mod:
            data='0xd0e30db0'
            value = amount
        elif mod == 'withdraw':
            contract = self.account.w3.eth.contract(
            abi=BLUR_ABI,
            address=self.blur_address
            )
            
            data=contract.encodeABI(mod, args=[amount])
            value = 0

        return await self.account.send_transaction(
            to=self.blur_address,
            data=data,
            value=value
            )
    

    async def zerion_dna(self):
        return await self.account.send_transaction(
            to=self.dna_address,
            data='0x1249c58b0021fb3f',
            value=0
            )
    

    async def transfer(self):
        return await self.account.send_transaction(
            to=self.account.trans_addr,
            value=self.account.w3.to_wei(uniform(*ETH_FOR_TRANSFER), "ether")
            )
