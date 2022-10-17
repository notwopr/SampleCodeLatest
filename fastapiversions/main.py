"""
Title: API Endpoint Home
Date Started: Jan 22, 2022
Version: 1.00
Version Start: Jan 22, 2022
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose:  Main API endpoints.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import sys
#   THIRD PARTY IMPORTS
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
#   LOCAL APPLICATION IMPORTS
from webapp.html import gen_html, html_body, html_servernotes
from webapp.servernotes import server_stats
from webapp.routers import bestletter, agebot, bestperformers, dipdatebot, compedgebot


app = FastAPI()


app.include_router(bestletter.router)
app.include_router(agebot.router)
app.include_router(bestperformers.router)
app.include_router(dipdatebot.router)
app.include_router(compedgebot.router)


def get_all_eps():
    ep_list = [{"name": route.tags[0], "path": route.path} for route in app.routes if route.name.startswith('input_')]
    return ep_list


def generatelinks(allboteps):
    return ''.join([f'<a href={i["path"]}>{i["name"]}</a><br>' for i in allboteps])


mainpage_desc = 'Welcome to the main page of my stock investing platform.  Below are links to the different investing tools available on this platform.  Have a nice day!'
mainpage_body = generatelinks(sorted(get_all_eps(), key=lambda x: x['name']))


@app.get("/", response_class=HTMLResponse)
async def root():
    mainpagebody = html_body("Main Page", mainpage_desc, mainpage_body, html_servernotes(server_stats))
    return HTMLResponse(content=gen_html("Main Page", '', mainpagebody), status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
