import csv


def write_csv_report(page_data: dict, filename: str = "report.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "page_url",
            "h1",
            "first_paragraph",
            "outgoing_link_urls",
            "image_urls",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        print("wrote headers")
        for data in page_data.values():
            if not isinstance(data, dict):
                continue
            writer.writerow(
                {
                    "page_url": data["url"],
                    "h1": data["h1"],
                    "first_paragraph": data["first_paragraph"],
                    "outgoing_link_urls": ";".join(data["outgoing_link_urls"]),
                    "image_urls": ";".join(data["image_urls"]),
                }
            )
