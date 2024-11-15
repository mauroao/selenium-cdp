import json
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome


# url = "https://qa-container.agilecontent.com.br/jira-reports/"
url = "https://qa-container.agilecontent.com.br/ec2-monitor/index.html"

def main():
    options = ChromeOptions()

    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
     
    driver = Chrome(options) 
    driver.execute_cdp_cmd("Network.enable", {})

    driver.get(url)

    save_logs_to_file(driver)

    driver.quit()

def save_logs_to_file(driver: Chrome):
    logs = []
    for entry in driver.get_log("performance"):
        log_data = json.loads(entry["message"])["message"]
        if log_data["method"] in ["Network.responseReceived", "Network.requestWillBeSent"]:
            logs.append(log_data)

    data = { "network": logs }
    filename = "file.json"
    with open(filename, "w", encoding="utf-8") as har_file:
        json.dump(data, har_file, indent=4)
    print(f"Logs saved to: {filename}")


if __name__ == "__main__":
    main()

