import hashlib
import requests
import time

import sys


def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    n = 6
    return guess_hash[:n] == "0"*n


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 4 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    start_time = time.time()
    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(f'{node}/last_proof').json()['proof']
        print("Mining started!")
        new_proof = proof_of_work(last_proof)
        print(new_proof, last_proof)
        # TODO: When found, POST it to the server {"proof": new_proof}
        res = requests.post(f'{node}/mine', json={"proof": new_proof})
        # TODO: If the server responds with 'New Block Forged'
        if res.json()['message'] == 'New Block Forged':
            print(f"Mining finished: {time.time()-start_time} seconds")
            coins_mined += 1
            print("Coins mined:", coins_mined)
            start_time = time.time()
        # else:
            # print(res.json()['message'])

            # add 1 to the number of coins mined and print it.  Otherwise,
            # print the message from the server.
            # pass
