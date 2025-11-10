import sys
import textwrap
from crawl import crawl_page


def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    url = sys.argv[1]
    print(f"starting crawl of: {url}")

    page_data = crawl_page(url)
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


if __name__ == "__main__":
    main()
