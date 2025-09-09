import json
from fastapi import FastAPI
from pydantic import BaseModel
from web3 import Web3
from eth_account import Account

# -----------------------------
# Загрузка конфига
# -----------------------------
with open("config.json", "r") as f:
    config = json.load(f)

networks = {}
for name, data in config["networks"].items():
    networks[name] = Web3(Web3.HTTPProvider(data["rpc"]))

tokens = config["tokens"]

# -----------------------------
# FastAPI
# -----------------------------
app = FastAPI(title="1C Blockchain Service")

# -----------------------------
# Модель для генерации кошельков
# -----------------------------
class WalletRequest(BaseModel):
    count: int = 1

# -----------------------------
# Модель для проверки балансов
# -----------------------------
class BalanceRequest(BaseModel):
    addresses: list[str]
    network: str

# -----------------------------
# Генерация кошельков
# -----------------------------
@app.post("/wallets/generate")
def generate_wallets(req: WalletRequest):
    wallets = []
    for _ in range(req.count):
        acct = Account.create()
        wallets.append({
            "address": acct.address,
            "private_key": acct._private_key.hex()
        })
    return {"wallets": wallets}

# -----------------------------
# Баланс кошелька
# -----------------------------
@app.post("/balances")
def get_balances(req: BalanceRequest):
    network_name = req.network.lower()
    if network_name not in networks:
        return {"error": f"Unknown network {req.network}"}
    w3 = networks[network_name]

    results = []
    for addr in req.addresses:
        addr_checksum = Web3.to_checksum_address(addr)
        balance_eth = w3.eth.get_balance(addr_checksum)
        balances = {"ETH": balance_eth / 10**18}

        # Проверяем токены
        for token in tokens:
            if token["network"].lower() == network_name:
                contract = w3.eth.contract(
                    address=Web3.to_checksum_address(token["address"]),
                    abi=[
                        {
                            "constant": True,
                            "inputs": [{"name": "_owner", "type": "address"}],
                            "name": "balanceOf",
                            "outputs": [{"name": "balance", "type": "uint256"}],
                            "type": "function",
                        }
                    ]
                )
                raw_balance = contract.functions.balanceOf(addr_checksum).call()
                balances[token["symbol"]] = raw_balance / 10**token["decimals"]

        results.append({"address": addr, "balances": balances})

    return {"network": network_name, "results": results}
