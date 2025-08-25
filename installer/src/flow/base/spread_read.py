# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%$$$$$$$$$$$$$$$$$$$
import gspread

gc = gspread.service_account(
    filename = "libe-auto-tweet.json"
)

sh = gc.create("test_1", folder_id="1ZO3eZuSukBruqwW54IOw7BjiwruUn2po")

ws = sh.get_worksheet(0)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# **********************************************************************************
# class定義

class SpreadsheetReader:
    def __init__(self):
        pass
    # ------------------------------------------------------------------------------
    # 関数定義

    def read_data(self, spreadsheet_id, range_name):
        gc = gspread.service_account(
            filename="libe-auto-tweet.json"
        )
        sh = gc.open_by_key(spreadsheet_id)
        ws = sh.get_worksheet(0)
        return ws.get(range_name)

    # ------------------------------------------------------------------------------
    # 関数定義





    # ------------------------------------------------------------------------------

# **********************************************************************************
