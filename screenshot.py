from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
from openpyxl.styles import Font
from time import time, localtime, strftime

class ExplorerScreenShot:
    def __init__(self, workbook, sheet):
        self.workbook = openpyxl.load_workbook(filename=workbook, data_only=True)
        self.sheet = self.workbook[sheet]

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        self.options.add_argument("--window-size=1920,1440")
        self.options.add_argument(f'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        
        self.network_map = {
            'ETH': "https://etherscan.io/tx/",
            'ERC20': "https://etherscan.io/tx/",
            "BTC": "https://www.blockchain.com/btc/tx/",
        }


    def logger(func):
        def wrapper(*args, **kwargs):
            start = time()
            start_time = strftime("%Y-%m-%d %I:%M:%S", localtime(start))
            print(f"starts now! {start_time}")
            func(*args, **kwargs)

            end = time()
            end_time = strftime("%Y-%m-%d %I:%M:%S", localtime(end))
            print(f"completed at {end_time}, took {end - start } seconds")
        return wrapper
    
    @logger
    def get_screenshot(self, target_network):
        for i in range(self.sheet.max_row + 1):
            network = self.sheet[f"K{str(i)}"].value
            if network in target_network:
                tx_hash = self.sheet[f"K{str(i)}"].value

                self.driver.get( self.network_map[network] + tx_hash )
                self.driver.implicitly_wait(10)
                self.driver.save_screenshot(f"sceenshots/{network}_{tx_hash}.png")

    
if __name__ == "__main__":
    filename ="screenshots/OKEx Funding Account History_v5.xlsx"
    es = ExplorerScreenShot(filename, "OKEx Funding 출금 History")
    es.get_screenshot(["ERC20", "BTC"])
