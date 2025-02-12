# RITO\_RANK

## Overview

This is a **Discord bot** that integrates with the **Riot Games API** to fetch **ranked solo queue stats** for League of Legends players. Users can retrieve their **tier, rank, and win rate** using a **slash command** in Discord by providing their **RiotID (Game Name + Tag)**.

## Features

- Retrieves **PUUID** using **RiotID** (game name + tag).
- Retrieves **Summoner ID** using PUUID.
- Retrieves **ranked solo queue stats** (Tier, Rank, Winrate).
- Implements a **Discord slash command (********`/get_rank_stats`*********).
- Validates user input (name and tag length).
- Sends a **welcome message** when a new member joins.
- Includes a simple `$say` command to repeat text in uppercase.
- Syncs slash commands automatically on bot startup.

## Setup & Installation

### **1. Install Dependencies**

Make sure you have **Python 3.10+** installed. Then install the required dependencies:

```bash
pip install -r requirements.txt
```

### **2. Get API Keys**

- **Riot Games API Key:** [Get it from Riot Developer Portal](https://developer.riotgames.com/).
- **Discord Bot Token:** [Create a bot in the Discord Developer Portal](https://discord.com/developers/applications).

### \*\*3. Configure \*\***`config.json`**

Create a `config.json` file in the same directory as `rito_rank_v6.py` and add:

```json
{
    "rito_token": "YOUR_RIOT_API_KEY",
    "disco_token": "YOUR_DISCORD_BOT_TOKEN"
}
```

### **4. Run the Bot**

```bash
python rito_rank_v6.py
```

## Usage

### \*\*Slash Command: \*\***`/get_rank_stats`**

- **Usage:** `/get_rank_stats region summoner_name tag`
- **Example:** `/get_rank_stats Europe West Faker 123`
- **Output:**
  ```
  Faker#123 ranked stats:
  Rank: DIAMOND I
  Winrate: 57.89%
  ```

### \*\*Text Command: \*\***`$say`**

- **Usage:** `$say thanks for watching!`
- **Output:** `THANKS FOR WATCHING!`

### **Auto Welcome Message**

- When a new member joins, the bot sends:
  ```
  @User Welcome to the loli gang, homie ╰(*°▽°*)╯
  ```

## Supported Regions

The following regions are supported in the dropdown menu:

- `North America (na1)`
- `Middle East (me1)`
- `Europe West (euw1)`
- `Europe Nordic & East (eun1)`
- `Oceania (oc1)`
- `Korea (kr)`
- `Japan (jp1)`
- `Brazil (br1)`
- `LAS (la2)`
- `LAN (la1)`
- `Russia (ru1)`
- `Turkey (tr1)`
- `Taiwan (tw2)`
- `Vietnam (vn2)`
- `Singapore (SG2)`

## Notes & Limitations

- The bot uses `discord.Intents.all()` (not recommended for production).
- Some summoners **may not have ranked stats**.
- Only **solo queue rank** is fetched (not flex or TFT ranks).

## Future Improvements

- Add support for **flex queue ranks**.
- Improve **error handling** for API failures.

## License

This project is **open-source** and free to use.

