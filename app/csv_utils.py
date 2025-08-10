import os
import csv

CSV_DIR = "./processed_results"
os.makedirs(CSV_DIR, exist_ok=True)

async def save_results_csv(job_data: dict) -> str:
    csv_path = os.path.join(CSV_DIR, f"{job_data['request_id']}.csv")
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["serial_number", "product_name", "original_url", "status", "processed_url"]
        )
        for img in job_data.get("images", []):
            writer.writerow(
                [
                    img.get("serial_number"),
                    img.get("product_name"),
                    img.get("original_url"),
                    img.get("status"),
                    img.get("processed_url", ""),
                ]
            )
    return csv_path
