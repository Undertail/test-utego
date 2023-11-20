from transaction_V import TranscationValue
import pytest
from playwright.async_api import async_playwright, expect
import asyncio
import re
import tempfile
import os



        
class PageInteraction: 
        async def firstAuthentication(self, link: str, namev:str):
         async with async_playwright() as p:
                browser =  await p.chromium.launch(headless=False, slow_mo=500)
                video_path = "test_videos/firstAuthentication"+namev 
                #controlla che eseista la cartella altrimenti la crea
                my_makedirs(video_path)
                context = await  browser.new_context(record_video_dir=video_path)
                page = await  context.new_page()
                await page.goto(link)
               
                await page.get_by_placeholder('Codice Identificativo').click()
                await page.get_by_placeholder('Codice Identificativo').fill('1234567')
                await page.get_by_placeholder('PIN/Password ').click()
                await page.get_by_placeholder('PIN/Password ').fill('1')
                await page.get_by_role('button', name=re.compile("Accedi", re.IGNORECASE)).click()
                await page.locator('#codiceOTP').click()
                await page.locator('#codiceOTP').fill('1')
                await page.get_by_role('button', name=re.compile("Accedi", re.IGNORECASE)).click()
                await page.get_by_role('gridcell', name="Lino Agostini Conto Corrente:871412938123 IBAN:IT77O0848283352871412938123").click()
                await page.get_by_role('button', name=re.compile("Seleziona", re.IGNORECASE)).click()
                await context.close()
                await browser.close()

        async def secondAuthentication(self, link: str, validation:bool, namev:str):
         async with async_playwright() as p:
                browser =  await p.chromium.launch(headless=False, slow_mo=500)
                video_path = "test_videos/secondAuthentication"+namev
                my_makedirs(video_path)
                context = await  browser.new_context(record_video_dir=video_path)
                page = await  context.new_page()
                await page.goto(link)
                await page.get_by_placeholder('Codice Identificativo').click()
                await page.get_by_placeholder('Codice Identificativo').fill('1234567')
                await page.get_by_placeholder('PIN/Password ').click()
                await page.get_by_placeholder('PIN/Password ').fill('1')
                await page.get_by_role('button', name=re.compile("Accedi", re.IGNORECASE)).click()
                await page.locator('#codiceOTP').click()
                await page.locator('#codiceOTP').fill('1')
                await page.get_by_role('button', name=re.compile("Accedi", re.IGNORECASE)).click()
                if validation:
                 await page.get_by_role('button', name=re.compile("Accetta", re.IGNORECASE)).click()
                else:
                 await page.get_by_role('button', name=re.compile("Rifiuta", re.IGNORECASE)).click()
                await context.close()
                await browser.close()



@pytest.fixture
def p_istance():
     return PageInteraction()



@pytest.mark.asyncio
async def test_accetta_pagmaneto(p_istance):
        tv = TranscationValue(0)
        tv.givToken()
        #caso in cui Accetta
        tv.givLinkSCA1()
        print(tv.linkSCA1)
        #nome del video
        namev="accetta"
 
        await p_istance.firstAuthentication(tv.linkSCA1,namev)
        #genera il link per effetturare la prima sca
        print(tv.getResponseStatusSCA())
        await p_istance.secondAuthentication(tv.linkSCA2, True, namev)
        #fornisce info sullo stato finale della transazione
        assert tv.getResponseStatusSCAFinal() == 'VERIFIED'

    
@pytest.mark.asyncio
async def test_rifiuta_pagamento(p_istance):
        tv = TranscationValue(0)
        tv.givToken()
        #caso in cui Accetta
        tv.givLinkSCA1()
        namev="rifiuta"
        await p_istance.firstAuthentication(tv.linkSCA1,namev)
        #genera il link per effetturare la prima sca
        print(tv.getResponseStatusSCA())
        await p_istance.secondAuthentication(tv.linkSCA2, False, namev)
        #fornisce info sullo stato finale della transazione
        assert tv.getResponseStatusSCAFinal() == 'FAILED'


# Esegui la funzione principale in un ciclo asincrono
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(test_accetta_pagmaneto())
    #loop.run_until_complete(test_rifiuta_pagamento())




def my_makedirs(path_dir):
         if not os.path.isdir(path_dir):
                os.makedirs(path_dir)

