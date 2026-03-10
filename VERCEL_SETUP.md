# Host CULT TRADERS CALCULATOR on Vercel

Your Discord bot runs as a **serverless function**: Discord sends an HTTP POST to your Vercel URL when someone uses a slash command. No long-running process needed.

## 1. Discord Developer Portal

1. Go to [Discord Developer Portal](https://discord.com/developers/applications/) → your application.
2. **Bot** tab: copy your **token** (for registering commands).
3. **General Information**: copy **Application ID** and **Public Key** (needed for Vercel).

## 2. Set Interactions URL

1. In the Developer Portal, open **General Information**.
2. Under **Interactions Endpoint URL**, set:
   - `https://YOUR_VERCEL_DOMAIN.vercel.app/api/interactions`
   - Replace with your real Vercel URL after first deploy.
3. Save.

## 3. Deploy on Vercel

1. Push this project to GitHub (or use Vercel CLI).
2. [Import the project on Vercel](https://vercel.com/new).
3. In **Settings → Environment Variables** add:
   - `DISCORD_PUBLIC_KEY` = your app **Public Key** (from General Information).
4. Deploy.

Your live URL will be like: `https://your-project.vercel.app`.  
Interactions URL: `https://your-project.vercel.app/api/interactions`.

## 4. Register slash commands (one time)

Slash commands must be registered with Discord using your **bot token** and **Application ID**.

**Option A – Local (recommended)**

```bash
set DISCORD_TOKEN=your_bot_token_here
set DISCORD_APP_ID=your_application_id_here
python register_commands.py
```

**Option B – PowerShell**

```powershell
$env:DISCORD_TOKEN="your_bot_token_here"
$env:DISCORD_APP_ID="your_application_id_here"
python register_commands.py
```

After this, `/lot`, `/pairs`, and `/quick` will appear in your Discord server.

## 5. Invite the bot

In Developer Portal → **OAuth2 → URL Generator**:

- Scopes: `bot`, `applications.commands`
- Bot permissions: **Send Messages**, **Embed Links**
- Use the generated URL to invite the bot to your server.

## Summary

| What              | Where / How |
|-------------------|-------------|
| Public Key        | Developer Portal → General Information → Public Key → `DISCORD_PUBLIC_KEY` on Vercel |
| Interactions URL  | Developer Portal → General Information → `https://YOUR_VERCEL_DOMAIN/api/interactions` |
| Register commands | Run `register_commands.py` once with `DISCORD_TOKEN` and `DISCORD_APP_ID` |

Never put your bot token in Vercel env vars; only the **Public Key** is needed for the serverless endpoint.
