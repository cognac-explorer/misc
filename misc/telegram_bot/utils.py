from io import BytesIO
import matplotlib.pyplot as plt
import gspread
from google.oauth2 import service_account
import pandas as pd


GSHEET_FILENAME = "test_tg_bot"

def get_gs_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(
        "cognac-explorer-tg-bot.json"
    )
    scoped_creds = credentials.with_scopes(scope)
    client = gspread.authorize(scoped_creds)
    return client


def read_last_n_records(exercise, n):
    spreadsheet = get_gs_client().open("test_tg_bot")
    worksheet = spreadsheet.get_worksheet(0)
    df = pd.DataFrame(worksheet.get_all_records())
    df = df[df['exercise'] == exercise][['date', 'best weight']].reset_index(drop=True)
    print(type(list(df['date'])[1]))
    df['date'] = pd.to_datetime(df['date']).dt.date
    # n or all available recodrs
    n = n if df.shape[0] > n else len(df.shape[0])
    df = df[-n:]
    x_vals = [date.strftime('%d %b') for date in df['date'].values]
    return x_vals, df['best weight'].values


def render_plot(x_values, y_values):
    plt.plot(x_values, y_values)
    plt.ylabel("Best weight")

    # Save the plot to a BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    return img_buffer
