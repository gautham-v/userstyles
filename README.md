# userstyles

Calm versions of sites I use every day. Each style swaps the site's colors for one warm
palette: dark by default, paper-light when macOS is in light mode. It also hides the
ads, upsells, AI panels and engagement bait.

| Style | What it removes |
| --- | --- |
| [DuckDuckGo](https://raw.githubusercontent.com/gautham-v/userstyles/main/duckduckgo-calm.user.css) | Ads, Duck.ai / Search Assist, promos |
| [ESPN](https://raw.githubusercontent.com/gautham-v/userstyles/main/espn-calm.user.css) | Betting, tickets, ESPN+ upsells, ads, autoplay video |
| [Gmail](https://raw.githubusercontent.com/gautham-v/userstyles/main/gmail-calm.user.css) | Gemini, side panel, storage and footer noise |
| [Google Calendar](https://raw.githubusercontent.com/gautham-v/userstyles/main/gcal-calm.user.css) | Gemini, side panel, upsells; softens event colors |
| [LinkedIn](https://raw.githubusercontent.com/gautham-v/userstyles/main/linkedin-calm.user.css) | Premium, News, puzzles, ads rail; icon-only nav |
| [Reddit](https://raw.githubusercontent.com/gautham-v/userstyles/main/reddit-calm.user.css) | Ads, trending, upsells, awards (new UI) |
| [Sleeper](https://raw.githubusercontent.com/gautham-v/userstyles/main/sleeper-calm.user.css) | Picks, Pick'em, app-download prompts; mutes the neon |
| [X](https://raw.githubusercontent.com/gautham-v/userstyles/main/x-calm.user.css) | Metrics, Grok, Premium, trends |
| [Yahoo Fantasy](https://raw.githubusercontent.com/gautham-v/userstyles/main/yahoo-fantasy-calm.user.css) | Ads, betting, Plus upsells, video |
| [YouTube](https://raw.githubusercontent.com/gautham-v/userstyles/main/youtube-calm.user.css) | Shorts, Premium, ads, shelves |

## Install

1. Install [Stylus](https://add0n.com/stylus.html) for Firefox or Chrome.
2. Click a style in the table above. Stylus opens an install page.
3. Turn Dark Reader (or any other dark-mode extension) off for that site, or it will
   fight the style.

Stylus checks this repo for updates. To change the palette, open the style's settings
in Stylus. Every color is a variable, and some styles have extra toggles.

## Caveats

These sites change their markup often, and some (Gmail, LinkedIn) use obfuscated class
names. When a site ships a redesign, parts of a style can break until it's updated.

`tools/sleeper/` holds the scripts that generated the big color-remap section of the
Sleeper style from Sleeper's CSS bundle.

## License

MIT
