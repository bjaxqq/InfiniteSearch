import aiohttp
import asyncio
import json
import itertools
import time
from aiohttp import ClientResponseError

async def combine(element, session):
    url = "https://neal.fun/api/infinite-craft/pair"
    params = {
        "first": element[0],
        "second": element[1]
    }
    headers = {
        "Referer": "https://neal.fun/infinite-craft/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    async with session.get(url, params=params, headers=headers) as response:
        if response.status == 200:
            output = await response.json()
            return output
        else:
            print(f"Error: {response.status}")
            return None

async def main():
    print("Starting script...")
    include_duplicates = False
    max_retries = 3

    initial_elements = {"Water": "💧", "Fire": "🔥", "Wind": "🌬️", "Earth": "🌍"}

    async with aiohttp.ClientSession() as session:
        discovered_elements = set(initial_elements.keys())
        retry_count = 0
        while True:
            combinations = itertools.combinations_with_replacement(discovered_elements, 2)
            craft_found = False
            for combination in combinations:
                try:
                    result = await combine(combination, session)
                    if result is None:
                        print("Skip")
                        continue
                    if result["result"] not in discovered_elements:
                        discovered_elements.add(result["result"])
                        initial_elements[result["result"]] = result["emoji"]
                        text = f"{initial_elements[combination[0]]} {combination[0]} & {initial_elements[combination[1]]} {combination[1]} -> {result['emoji']} {result['result']}{' (New Recipe)' if result['isNew'] else ''}"
                        print(text)
                        with open("crafts.json", "a", encoding="utf-8") as f:
                            f.write(text + "\n")
                            f.flush()  # Flush buffer to ensure immediate writing to the file
                        craft_found = True
                except ClientResponseError as e:
                    if e.status == 429:
                        print("Rate limited, retrying after delay...")
                        await asyncio.sleep(5)  # Wait for 5 seconds before retrying
                        retry_count += 1
                        if retry_count >= max_retries:
                            print("Max retries reached. Exiting.")
                            return
                        break
                    else:
                        print(f"Unexpected error: {e}")
                        break
                # Introduce a delay between requests to avoid being rate-limited
                await asyncio.sleep(1)

            if not craft_found:
                break  # If no new crafts were found, exit the loop

if __name__ == "__main__":
    asyncio.run(main())
