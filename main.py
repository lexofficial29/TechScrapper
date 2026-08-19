import pandas as pd
import modules.webserver_data as webserver_data
import modules.browser_sim as browser_sim
import json
import time
import os
import sys

df = pd.read_parquet('data/example1.parquet')

print(f"Total domains loaded: {len(df)}")

DATA_TABLE = []

for domain in df["root_domain"]:
    DATA_TABLE.append({"url": domain})

print("Starting Phase 1: Webserver Detection..")
time.sleep(1)

try:
    domain_list = df['root_domain'].tolist()  
    scan_results = webserver_data.scan_webservers(domain_list, max_threads=20)
    
    for i, data in enumerate(scan_results):
        del data['url']
        DATA_TABLE[i].update({"phase1": data})
        
    print("Phase 1 complete!")

except KeyboardInterrupt:
    print("Process interrupted by user.")
    sys.exit(0)

print("Starting Phase 2: Browser Simulation..")
time.sleep(1)

try:
    domain_list = df['root_domain'].tolist()
    scan_results = browser_sim.start_sim(domain_list, max_threads=10)

    for item in scan_results:
        url = item[0].replace("http://","")
        tech_data = item[1]
        for entry in DATA_TABLE:
            if entry['url'] == url:
                entry.update({"phase2": tech_data})
                break

    print("Phase 2 complete!")

except KeyboardInterrupt:
    print("Process interrupted by user.")
    sys.exit(0)

print("Starting phase 3: Removing duplicates and saving..")

FINAL_DATA = []
total_technologies_detected = 0
webserver_technologies_detected = 0

for entry in DATA_TABLE:
    phase1_data = entry.get("phase1", {})
    phase2_data = entry.get("phase2", [])

    technologies = []
    seen_techs = set()

    def add_technologies(items):
        global total_technologies_detected
        if isinstance(items, dict):
            items = [items]
        
        for item in items:
            if isinstance(item, dict):
                tech_name = item.get("tech")
                proof = item.get("proof", "")

                if (tech_name and tech_name != "Not detected" and tech_name not in seen_techs):
                    seen_techs.add(tech_name)
                    technologies.append({"tech": tech_name, "proof": proof})
                    total_technologies_detected += 1

    add_technologies(phase1_data.get("platforms", []))
    add_technologies(phase2_data)

    if (phase1_data.get("webserver", "Not detected") != "Not detected"):
        total_technologies_detected += 1
        webserver_technologies_detected += 1

    FINAL_DATA.append(
        {
            "url": entry.get("url", ""),
            "webserver_tech": phase1_data.get("webserver", "Not detected"),
            "technologies": technologies,
        }
    )

os.makedirs("output", exist_ok=True)
with open('output/output.json', 'w') as f:
    json.dump(FINAL_DATA, f, indent=4)

print("Done! Output saved to output/output.json")

print(f"Total technologies detected: {total_technologies_detected} out of which {webserver_technologies_detected} were webserver technologies.")
print(f"Total without webserver technologies: {total_technologies_detected - webserver_technologies_detected}")
