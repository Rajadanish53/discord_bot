import discord
from discord.ext import commands
from discord import app_commands
import datetime

# Bot setup (default intents - no privileged intents needed in Developer Portal)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'🎉 CULT TRADERS CALCULATOR is now online!')
    print('✅ Professional trading calculator ready!')

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="risk management 📈"
    ))


def calculate_lot_size(account_balance, risk_percent, stop_loss_pips, instrument):
    """Calculate lot size based on instrument type"""
    risk_amount = account_balance * (risk_percent / 100)

    # PIP VALUES FOR MAJOR PAIRS
    pip_values = {
        # FOREX PAIRS
        'EURUSD': 10.0, 'GBPUSD': 10.0, 'USDJPY': 9.0, 'USDCHF': 10.0,
        'AUDUSD': 10.0, 'USDCAD': 10.0, 'NZDUSD': 10.0,

        # CROSSES
        'EURGBP': 10.0, 'EURJPY': 10.0, 'GBPJPY': 10.0,
        'AUDJPY': 10.0, 'CADJPY': 9.0, 'CHFJPY': 9.0,

        # METALS
        'XAUUSD': 10.0, 'GOLD': 10.0, 'XAGUSD': 5.0, 'SILVER': 5.0,

        # INDICES
        'US30': 1.0, 'US100': 2.0, 'SPX500': 0.5, 'NAS100': 2.0, 'DOW': 1.0,

        # COMMODITIES
        'USOIL': 10.0, 'UKOIL': 10.0, 'OIL': 10.0, 'XTIUSD': 10.0,

        # CRYPTO
        'BTCUSD': 1.0, 'ETHUSD': 1.0, 'XRPUSD': 1.0, 'LTCUSD': 1.0,
    }

    pip_value = pip_values.get(instrument.upper(), 10.0)
    lot_size = risk_amount / (stop_loss_pips * pip_value)

    # Minimum lot size
    if lot_size < 0.01:
        lot_size = 0.01

    return round(lot_size, 2), risk_amount, pip_value


@bot.tree.command(name="lot", description="Calculate lot size for any trading pair")
@app_commands.describe(
    acc_size="Your account size in USD",
    risk="Risk percentage (1-5% recommended)",
    pair="Trading pair (XAUUSD, EURUSD, US100, etc.)",
    sl="Stop loss in pips"
)
async def lot(interaction: discord.Interaction, acc_size: float, risk: float, pair: str, sl: float):
    """Professional lot size calculator for all pairs"""
    if risk > 20:
        await interaction.response.send_message("❌ Risk should not exceed 20%!")
        return

    if sl <= 0:
        await interaction.response.send_message("❌ Stop loss must be greater than 0!")
        return

    lot_size, risk_amount, pip_value = calculate_lot_size(acc_size, risk, sl, pair)

    # Get current timestamp in the format from screenshot
    current_time = datetime.datetime.now().strftime("%m/%d/%y, %I:%M %p").replace(" 0", " ").lstrip("0")

    # Create embed
    embed = discord.Embed(
        title="CULT TRADERS CALCULATOR APP",
        description=f"{current_time}",
        color=0x00ff00
    )

    embed.add_field(
        name="**LOT SIZE CALCULATOR**",
        value="\u200b",
        inline=False
    )

    embed.add_field(
        name="ACCOUNT SIZE",
        value=f"${acc_size:,.1f}",
        inline=False
    )

    embed.add_field(
        name="RISK",
        value=f"{risk}% = ${risk_amount:.1f}",
        inline=False
    )

    embed.add_field(
        name="PAIR",
        value=pair.upper(),
        inline=False
    )

    embed.add_field(
        name="STOP-LOSS",
        value=f"{sl} pips",
        inline=False
    )

    embed.add_field(
        name="CALCULATED LOT SIZE",
        value=f"**{lot_size:.2f}**",
        inline=False
    )

    embed.set_footer(text="BY CULT TRADERS")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="pairs", description="Show all supported trading pairs")
async def pairs(interaction: discord.Interaction):
    embed = discord.Embed(
        title="SUPPORTED TRADING PAIRS",
        color=0x0099ff
    )

    embed.add_field(
        name="MAJOR FOREX",
        value="EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, USDCAD, NZDUSD",
        inline=False
    )

    embed.add_field(
        name="CROSS PAIRS",
        value="EURGBP, EURJPY, GBPJPY, AUDJPY, CADJPY, CHFJPY",
        inline=False
    )

    embed.add_field(
        name="METALS",
        value="XAUUSD (Gold), XAGUSD (Silver)",
        inline=False
    )

    embed.add_field(
        name="INDICES",
        value="US30 (Dow Jones), US100 (NASDAQ), SPX500 (S&P 500)",
        inline=False
    )

    embed.add_field(
        name="COMMODITIES",
        value="USOIL, UKOIL",
        inline=False
    )

    embed.add_field(
        name="CRYPTO",
        value="BTCUSD, ETHUSD, XRPUSD, LTCUSD",
        inline=False
    )

    embed.add_field(
        name="USAGE",
        value="Use `/lot acc_size:1000 risk:2 pair:XAUUSD sl:50`",
        inline=False
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="quick", description="Quick lot size examples")
async def quick(interaction: discord.Interaction):
    embed = discord.Embed(
        title="QUICK EXAMPLES",
        color=0xffa500
    )

    embed.add_field(
        name="Example 1:",
        value="`/lot acc_size:1000 risk:2 pair:XAUUSD sl:50`\n• ACCOUNT SIZE: $1,000.0\n• RISK: 2.0% = $20.0\n• PAIR: XAUUSD\n• STOP-LOSS: 50 pips\n• CALCULATED LOT SIZE: **0.04**",
        inline=False
    )

    embed.add_field(
        name="Example 2:",
        value="`/lot acc_size:5000 risk:1 pair:EURUSD sl:30`\n• ACCOUNT SIZE: $5,000.0\n• RISK: 1.0% = $50.0\n• PAIR: EURUSD\n• STOP-LOSS: 30 pips\n• CALCULATED LOT SIZE: **0.17**",
        inline=False
    )

    embed.add_field(
        name="Risk Management",
        value="Maximum Risk Limit: **20%**\nRecommended: 1-2% risk per trade",
        inline=False
    )

    await interaction.response.send_message(embed=embed)






# Start the bot
print("🔄 Starting CULT TRADERS CALCULATOR...")
print("✅ Maximum risk limit: 20%")
bot.run(TOKEN)