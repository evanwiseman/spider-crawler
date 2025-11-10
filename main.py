import asyncio
import sys
import textwrap
from crawl import crawl_site_async


async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    max_concurrency = 3
    if len(sys.argv) == 3:
        max_concurrency = int(sys.argv[2])

    max_pages = 25
    if len(sys.argv) == 4:
        max_pages = int(sys.argv[3])

    url = sys.argv[1]
    print(f"starting crawl of: {url}")

    page_data = await crawl_site_async(url, max_concurrency, max_pages)
    for normalized_url, data in page_data.items():
        # invalid entry
        if not isinstance(data, dict):
            continue

        print(normalized_url)
        for k, v in data.items():
            if isinstance(v, list):
                print(f"\t{k}: [")
                for item in v:
                    text = textwrap.fill(
                        str(item),
                        initial_indent="\t\t",
                        subsequent_indent="\t\t",
                    )
                    print(text)
                print("\t]")
            else:
                text = textwrap.fill(
                    str(v),
                    initial_indent="",
                    subsequent_indent="\t\t",
                )
                print(f"\t{k}: {text}")

    print(f"complete crawing {url} successfully on {len(page_data)} pages.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCrawl interrupted by user. Exiting...")
