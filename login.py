import asyncio
import sys
from playwright.async_api import async_playwright
import asyncssh

async def login_en_mainFrame(userDia, passDia, userSSH, passSSH):

    JUMP_SERVER = "nogal.usal.es"
    FINAL_SERVER = "prodiasv21.fis.usal.es"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context()
        page = await context.new_page()

        print("Cargando estructura de frames...")
        await page.goto("https://diaweb.usal.es/diaweb/comun/loguear.jsp")
        await page.wait_for_timeout(3000)

        # Accedemos al frame que contiene el login
        main_frame = page.frame(name="mainFrame")
        if not main_frame:
            print("No se pudo acceder al frame 'mainFrame'")
            await browser.close()
            return

        print("Rellenando formulario de login dentro de 'mainFrame'...")
        try:
            print("Rellenando el login con XPath...")
            await main_frame.fill('//html/body/table[1]/tbody/tr/td/form/div/table/tbody/tr[1]/td[2]/input', userDia)
            await main_frame.fill('//html/body/table[1]/tbody/tr/td/form/div/table/tbody/tr[2]/td[2]/input', passDia)

            await main_frame.click('input[type="submit"]')
            await page.wait_for_timeout(3000)

            # Wait for 2 minutes
            await asyncio.sleep(120)

            ## SSH implementation
            print("Estableciendo conexión SSH...")
            async with asyncssh.connect(
                JUMP_SERVER, 
                username=userDia, 
                password=passDia, 
                known_hosts=None, 
                client_keys=None
            ) as jump_conn:
                print(f"Conexión establecida con el servidor de salto: {JUMP_SERVER}")
                async with asyncssh.connect(FINAL_SERVER,
                    username=userSSH,
                    password=passSSH,
                    tunnel=jump_conn, 
                    known_hosts=None, 
                    client_keys=None
                ) as final_conn:
                    print(f"Conexión establecida con el servidor final: {FINAL_SERVER}")          
                    # Example command execution on FINAL_SERVER
                    await final_conn.run("docker stop malagasytts_container", check=True)
                    pruneResult = await final_conn.run("docker system prune --all --force", check=True)
                    print(f"{pruneResult.stdout.strip()}")
                    pullResult = await final_conn.run("docker pull andrespm2000/malagasytts_image:latest", check=True)
                    print(f"{pullResult.stdout.strip()}")
                    runResult = await final_conn.run("docker run -d -p 8000:8000 --name malagasytts_container andrespm2000/malagasytts_image:latest", check=True)
                    print(f"{runResult.stdout.strip()}")
                    print(f"Comandos ejecutados con éxito")

        except Exception as e:
            print("Error al interactuar con el login o SSH:", e)

        await browser.close()

asyncio.run(login_en_mainFrame(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))