import asyncio
import sys
from crawl import crawl_site_async
from csv_report import write_csv_report


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
    successful_visits = 0
    for normalized_url, data in page_data.items():
        # invalid entry
        if not isinstance(data, dict):
            continue

        # print(normalized_url)
        # for k, v in data.items():
        #     if isinstance(v, list):
        #         print(f"\t{k}: [")
        #         for item in v:
        #             text = textwrap.fill(
        #                 str(item),
        #                 initial_indent="\t\t",
        #                 subsequent_indent="\t\t",
        #             )
        #             print(text)
        #         print("\t]")
        #     else:
        #         text = textwrap.fill(
        #             str(v),
        #             initial_indent="",
        #             subsequent_indent="\t\t",
        #         )
        #         print(f"\t{k}: {text}")

        successful_visits += 1

    print(f"complete crawing {url} ({successful_visits}/{len(page_data)}) pages.")
    filename = "report.csv"
    print(f"writing report to {filename}...")
    try:
        write_csv_report(page_data, filename)
        print("finished writing report.")
    except Exception as e:
        print(f"failed to write report: {str(e)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCrawl interrupted by user. Exiting...")
