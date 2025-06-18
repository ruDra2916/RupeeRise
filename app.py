import gradio as gr
from accounts import Account, get_share_price

account = Account(user_id="user123")

def create_account():
    return "✅ Account created for user123"

def deposit(amount):
    try:
        account.deposit_funds(float(amount))
        return f"💰 Deposited ₹{amount}. Current balance: ₹{account.balance:.2f}"
    except ValueError as e:
        return f"❌ {str(e)}"

def withdraw(amount):
    try:
        account.withdraw_funds(float(amount))
        return f"🏦 Withdrew ₹{amount}. Current balance: ₹{account.balance:.2f}"
    except ValueError as e:
        return f"❌ {str(e)}"

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, int(quantity))
        return f"📈 Bought {quantity} shares of {symbol}. Balance: ₹{account.balance:.2f}"
    except ValueError as e:
        return f"❌ {str(e)}"

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, int(quantity))
        return f"📉 Sold {quantity} shares of {symbol}. Balance: ₹{account.balance:.2f}"
    except ValueError as e:
        return f"❌ {str(e)}"

def view_portfolio():
    value = account.portfolio_value()
    return f"📊 Portfolio Value: ₹{value:.2f}"

def view_holdings():
    holdings = account.report_holdings()
    return f"📂 Holdings: {holdings}"

def view_transactions():
    transactions = account.transaction_history()
    return f"📜 Transactions: {transactions}"

def view_profit_loss():
    profit_loss = account.profit_or_loss()
    return f"📈 Profit/Loss: ₹{profit_loss:.2f}"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="green", secondary_hue="purple")) as demo:
    gr.Markdown(
        """
        <h1 style='color:#10B981; font-size: 2.5rem; text-align: center;'>💸 RupeeRise</h1>
        <p style='color:#6B7280; font-size: 1.1rem; text-align: center;'>Smart Trading Simulator – Manage funds, trade stocks, and grow your portfolio.</p>
        """
    )

    with gr.Row():
        acc_status = gr.Textbox(label="Account Status", interactive=False)
        gr.Button("🚀 Create Account", variant="primary").click(create_account, outputs=acc_status)

    with gr.Tabs():
        with gr.Tab("💰 Funds"):
            with gr.Row():
                with gr.Column():
                    deposit_amt = gr.Number(label="Deposit Amount")
                    deposit_output = gr.Textbox(label="Deposit Status", interactive=False)
                    gr.Button("💸 Deposit", variant="primary").click(deposit, inputs=deposit_amt, outputs=deposit_output)

                with gr.Column():
                    withdraw_amt = gr.Number(label="Withdraw Amount")
                    withdraw_output = gr.Textbox(label="Withdraw Status", interactive=False)
                    gr.Button("🏧 Withdraw", variant="primary").click(withdraw, inputs=withdraw_amt, outputs=withdraw_output)

        with gr.Tab("📈 Trading"):
            with gr.Row():
                with gr.Column():
                    buy_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Buy Symbol")
                    buy_qty = gr.Number(label="Quantity to Buy")
                    buy_output = gr.Textbox(label="Buy Status", interactive=False)
                    gr.Button("🛒 Buy Shares", variant="primary").click(buy_shares, inputs=[buy_symbol, buy_qty], outputs=buy_output)

                with gr.Column():
                    sell_symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Sell Symbol")
                    sell_qty = gr.Number(label="Quantity to Sell")
                    sell_output = gr.Textbox(label="Sell Status", interactive=False)
                    gr.Button("💼 Sell Shares", variant="primary").click(sell_shares, inputs=[sell_symbol, sell_qty], outputs=sell_output)

        with gr.Tab("📊 Reports"):
            with gr.Row(equal_height=True):
                with gr.Column():
                    port_output = gr.Textbox(label="Portfolio Value", interactive=False)
                    gr.Button("📦 Portfolio Value", variant="secondary").click(view_portfolio, outputs=port_output)

                    txn_output = gr.Textbox(label="Transaction History", interactive=False)
                    gr.Button("🧾 Transactions", variant="secondary").click(view_transactions, outputs=txn_output)

                with gr.Column():
                    hold_output = gr.Textbox(label="Holdings", interactive=False)
                    gr.Button("📁 Holdings", variant="secondary").click(view_holdings, outputs=hold_output)

                    pl_output = gr.Textbox(label="Profit / Loss", interactive=False)
                    gr.Button("📈 Profit / Loss", variant="secondary").click(view_profit_loss, outputs=pl_output)

    gr.Markdown(
        "<hr><p style='text-align:center; color:#9CA3AF;'>© 2025 RupeeRise – Built with 💚 in India 🇮🇳</p>"
    )

demo.launch()
