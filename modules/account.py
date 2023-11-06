from random import choice
from time import time

from web3 import AsyncWeb3
from web3.middleware import async_geth_poa_middleware
from web3.exceptions import TransactionNotFound

from modules.utils import check_gas, sleeping, info
from config import USE_PROXY, RPC, MODULES, EXTRA_MODULES


class Account:
    def __init__(
            self,
            wallet: dict,
            id: int
    ):
        request_kwargs = {}
        
        if USE_PROXY:
            proxy = wallet["proxy"]
            _proxy = f'{proxy[proxy.find(":")+6:]}@{proxy[:proxy.find(":")+5]}'
            request_kwargs = {"proxy": f"http://{_proxy}"}

        if 'transfer' in MODULES+EXTRA_MODULES:
            self.trans_addr = wallet["trans_addr"]

        self.id = id
        self.w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(choice(RPC)),
            middlewares=[async_geth_poa_middleware],
            request_kwargs=request_kwargs
        )
        self.private_key = wallet["private_key"]
        self.address = self.w3.eth.account.from_key(private_key=self.private_key).address


    async def get_max_priority_fee_per_gas(self, block: dict) -> int:
        block_number = block['number']
        latest_block_transaction_count = await self.w3.eth.get_block_transaction_count(block_number)
        max_priority_fee_per_gas_list = []

        for _id in range(latest_block_transaction_count):
            try:
                transaction = await self.w3.eth.get_transaction_by_block(block_number, _id)
                if 'maxPriorityFeePerGas' in transaction:
                    max_priority_fee_per_gas_list.append(transaction['maxPriorityFeePerGas'])
            except:
                continue

        if not max_priority_fee_per_gas_list:
            max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
        else:
            max_priority_fee_per_gas_list.sort()
            max_priority_fee_per_gas = max_priority_fee_per_gas_list[len(max_priority_fee_per_gas_list) // 2]

        return max_priority_fee_per_gas


    @check_gas
    async def send_transaction(
            self,
            to,
            increase_gas=1.1,
            data=None,
            value=None
        ):

        last_block = await self.w3.eth.get_block('latest')

        max_priority_fee_per_gas = await self.get_max_priority_fee_per_gas(block=last_block)

        base_fee = int(last_block['baseFeePerGas'] * increase_gas)

        max_fee_per_gas = base_fee + max_priority_fee_per_gas

        tx = {
            'chainId': await self.w3.eth.chain_id,
            'nonce': await self.w3.eth.get_transaction_count(self.address),
            'from': self.address,
            'to': AsyncWeb3.to_checksum_address(to),
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'maxFeePerGas': max_fee_per_gas
        }

        if data:
            tx['data'] = data

        if value:
            tx['value'] = value

        tx['gas'] = int(await self.w3.eth.estimate_gas(tx) * increase_gas)

        sign = self.w3.eth.account.sign_transaction(tx, self.private_key)

        tx_hash = await self.w3.eth.send_raw_transaction(sign.rawTransaction)

        return await self.verif_tx(tx_hash)


    async def verif_tx(self, tx_hash) -> bool:
        await info(
            f"{self.id} | Waiting transaction: "
            f"https://etherscan.io/tx/{tx_hash.hex()}", "magenta"
            )
        
        start_time = time()
        while True:
            try:
                data = await self.w3.eth.get_transaction_receipt(tx_hash)
                status = data.get("status")

                if status == 1:
                    return True
                elif not status:
                    await sleeping([1, 1])
                else:
                    return

            except TransactionNotFound:
                if time() - start_time > 200:
                    return
