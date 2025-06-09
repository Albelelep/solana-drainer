import json, argparse, sys, time
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

class KapanJP:

  def __init__(self, rpc, program_id, payer):
    self.rpc = rpc
    self.program_id = program_id
    self.payer = payer
    self.client = Client(rpc)
    if not self.client.is_connected():
      sys.exit("yang bener aja")

    self.token_client = Token(self.client, program_id, TOKEN_PROGRAM_ID, payer)

  def get_balance(self, pubkey, integer=True):
    balance = self.token_client.get_balance(pubkey).value.amount
    if integer:
      balance = int(balance)
    return balance

  def transfer(self, source, dest, owner, amount):
    self.token_client.transfer(source, dest, owner.pubkey(), amount, multi_signers=[self.payer, owner])

  def main(self, source, dest, owner, interval):
    while True:
      print ("\r[*] Aiming...", end="")
      balance = self.get_balance(source)
      if balance > 0:
        print (f"\r[+] Transferring {balance} token")
        self.transfer(source, dest, owner, balance)
      time.sleep(interval)

  def get_token_account(self, pubkey, index):
    return self.token_client.get_accounts_by_owner(pubkey).value[index].pubkey

  def create_token_account(self, pubkey):
    return self.token_client.create_associated_token_account(pubkey)

class Kunci:

  def __init__(self, target="", x=None):
    if target == "private":
      self.private(x)
    elif target == "public":
      self.public(x)

  def private(self, private_key):
    self.keypair = Keypair.from_bytes(bytes(private_key))
    self.pubkey = self.keypair.pubkey()

  def public(self, public_key):
    self.pubkey = Pubkey.from_string(public_key)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("source", help="a private key from source address")
  parser.add_argument("token_mint_address", help="token address (likely smart contract on evm)")
  parser.add_argument("--token-account-index", help="index of token account", default=0)
  parser.add_argument("--create-sccount", help="auto create token account (in source) if not exists")
  parser.add_argument("--payer", help="custom private key to fill gas fees")
  parser.add_argument("--receiver", help="public key (address)")

  args = parser.parse_args()
  data = json.loads(open("data.json").read())

  rpc = data["rpc"]
  interval = data["interval"]
  payer = data["payer"]
  if args.payer:
    payer = args.payer
  receiver = data["receiver"]
  if args.receiver:
    receiver = args.receiver
  source_0 = [int(x) for x in args.source.strip("][").split(",")]

  token = Kunci("public", args.token_mint_address).pubkey
  payer = Kunci("private", payer).keypair
  source = Kunci("private", source_0).pubkey
  dest_0 = Kunci("public", receiver).pubkey
  owner = Kunci("private", source_0).keypair
  account_index = args.token_account_index

  client = KapanJP(rpc, token, payer)

  source = client.get_token_account(source, account_index)
  try:
    dest = client.get_token_account(dest_0, account_index)
  except IndexError:
    if account_index == 0:
      client.create_token_account(dest_0)
      dest = client.get_token_account(dest_0, account_index)
  try:
    client.main(source, dest, owner, interval)
  except KeyboardInterrupt:
    sys.exit("stopped")
