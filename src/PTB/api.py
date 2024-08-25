import json
from fastapi import FastAPI, Body

from botModule import *

app = FastAPI()


@app.post("/discordreq")
async def find(dis_req: Body(...)):
    try:
        data = json.loads(dis_req)
        sample = ["title", "3", "No me", "-4181556113"]
        find_fwrd, find_txt = result(sample[0], sample[1], sample[2], sample[3])

        return "done"

    except Exception as e:
        # Handle potential errors and return a suitable response
        return {"error": str(e)}, 500
