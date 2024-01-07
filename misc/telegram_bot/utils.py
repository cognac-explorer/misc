from io import BytesIO
import matplotlib.pyplot as plt
import gspread
from google.oauth2 import service_account

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = service_account.Credentials.from_service_account_file(
    "cognac-explorer-tg-bot.json"
)
scoped_creds = credentials.with_scopes(scope)
client = gspread.authorize(scoped_creds)


def read_last_n_records(column_number, n):
    spreadsheet = client.open("test_tg_bot")
    worksheet = spreadsheet.get_worksheet(0)
    col_values = worksheet.col_values(column_number)
    n = n if len(col_values) > n + 1 else len(col_values) - 1
    dates = worksheet.col_values(1)[-n:]
    return dates, list(map(int, col_values[-n:]))


def render_plot(x_values, y_values):
    plt.plot(x_values, y_values)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("lalalalalla")

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    return img_buffer
