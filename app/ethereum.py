from time import sleep
from web3 import Web3, KeepAliveRPCProvider, contract

web3 = Web3(KeepAliveRPCProvider(host='localhost', port='8545'))
eth = web3.eth


def submit_file(file):
    # TODO
    return 'TODO_the_ethereum_tx'


def traversal_all_contract():
    for i in range(7000, eth.blockNumber + 1):
        if eth.getBlockTransactionCount(i) > 0:
            block = eth.getBlock(i)
            for transaction in block['transactions']:
                contractAddress = eth.getTransactionReceipt(transaction)['contractAddress']
                print(i, block['hash'], transaction, contractAddress)


contract_data = {
    'abi': [{"constant":True,"inputs":[],"name":"getData","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"","type":"bytes32"}],"name":"proofs","outputs":[{"name":"name","type":"string"},{"name":"description","type":"string"},{"name":"timestamp","type":"uint256"},{"name":"sender","type":"address"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"d","type":"string"}],"name":"setData","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"hash","type":"bytes32"}],"name":"getProofDescription","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"a","type":"int256"},{"name":"b","type":"int256"}],"name":"add","outputs":[{"name":"","type":"int256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"hash","type":"bytes32"},{"name":"name","type":"string"},{"name":"description","type":"string"}],"name":"proof","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"hash","type":"bytes32"}],"name":"getProofSender","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"hash","type":"bytes32"}],"name":"getProofName","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"hash","type":"bytes32"}],"name":"getProofTimestamp","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"inputs":[],"payable":False,"type":"constructor"}],
    # 'code': '0x...',
    # 'code_runtime': '0x...',
    # 'source': 'contract Token {.....}',
}


def deploy_contract():
    pass


def load_contract(address):
    contract_factory = contract.construct_contract_factory(web3, contract_data['abi'])
    my_contract = contract_factory(address=address)
    result = my_contract.call().add(1, 2)
    print(result)

    print(my_contract.call().getProofTimestamp("aa"))

    print(web3.personal.unlockAccount(eth.coinbase, '4869'))
    # print(my_contract.transact().proof("aaa", "bb", "cc"))

    from datetime import datetime
    print(datetime.now())
    new_data = "test4"
    print(my_contract.transact().setData(new_data))
    print(my_contract.transact().setData(new_data))
    print(my_contract.transact().setData(new_data))
    print(my_contract.transact().setData(new_data))
    print(my_contract.transact().setData(new_data))
    while True:
        data = my_contract.call().getData()
        print(data)
        if data == new_data:
            break
        sleep(2)
    print(datetime.now())


if __name__ == '__main__':
    print(eth.blockNumber)
    # traversal_all_contract()

    # deploy_contract()

    load_contract("0xd6b38575df44e72861237b3c127894bc90892b98")
