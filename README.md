# AmvTracker Plugin for Kodi

<p align="center">
  <img src="https://github.com/spoichiche/KodiAmvTrackerPlugin/blob/master/plugin.video.amvtracker/resources/icon.png">
</p>

**AmvTracker Plugin** is a Kodi addon that allows users to browse, search, and play anime music videos (AMVs) from their local AMV library managed by [AmvTracker](https://github.com/bsobotka/amv_tracker). This plugin bridges the gap between your organized AMV collection and the Kodi media center experience.

---

## Features

- 🎞 Browse your entire AMV collection directly in Kodi
- 🗃️ Group AMVs by Editors, Studios, Genres, Years, Contests, Anime sources, Song artists and Song genres
- 📶 Order by title / year / genre / studio / rating / playcount / filepath
- 🔎 Search by title, artist, anime, genre, or tags
- 📂 Support for AmvTracker's playcount, custom playlists, favorites and tags
- ⚙ Configurable connection to your local AmvTracker database
- 🎮 Remote-control ready for the full Kodi experience
- 🌍 Multi-language support (English 🇬🇧 and French 🇫🇷)

---

## Prerequisites

Before installing this plugin, ensure the following:

- You have a working installation of [Kodi](https://kodi.tv/) (version 21 "Omega" or newer recommended)
- You have [AmvTracker](https://github.com/bsobotka/amv_tracker) running locally or on your home network
- Your AMV library is indexed and accessible through the AmvTracker API

---

## Installation

1. Download the latest release of the plugin as a `.zip` file.
2. Open Kodi and go to:
   Add-ons > Install from zip file
4. Select the downloaded `.zip` file.
5. Once installed, go to:
   Add-ons > Video add-ons > AmvTracker
6. On first launch, configure the plugin to point the location to your local AmvTracker database:
   /path/to/your/AmvTracker/db_files/my_database.db
   - The name of the database can be configured in AmvTracker, so it might not be named "my_database.db" which is the default name
   - If you are running mulitple databases in AmvTracker, only one can be configured at a time for this plugin

---

## Configuration

You can access the settings via: 
  Add-ons > My add-ons > Video add-ons > AmvTracker > Configure
Settings include:
- **Database File**: The location to your local AmvTracker database

---

## Screenshots

![alt text](https://github.com/spoichiche/KodiAmvTrackerPlugin/blob/master/plugin.video.amvtracker/resources/screenshots/screenshot-01.jpg)

![alt text](https://github.com/spoichiche/KodiAmvTrackerPlugin/blob/master/plugin.video.amvtracker/resources/screenshots/screenshot-02.jpg)

![alt text](https://github.com/spoichiche/KodiAmvTrackerPlugin/blob/master/plugin.video.amvtracker/resources/screenshots/screenshot-03.jpg)

---

## Language Support

This plugin includes built-in support for the following languages:

- **English** 🇬🇧 (default)
- **French** 🇫🇷

Kodi will automatically use the appropriate language based on your Kodi system settings. To change the language:

1. Go to `Settings > Interface > Regional`
2. Select your preferred language under `Language`

If your language is supported, the plugin UI will update accordingly.

---

## Troubleshooting

- Ensure your AmvTracker database is accessible locally on your machine and that your have correctly set the filepath to the database in the addon settings.
- Ensure your Amvs can be played by Kodi
- Look in the Kodi logs for error messages if the plugin doesn't load or crashes.

---

## Development

Want to contribute or customize?

Clone the repo:
```bash
git clone https://github.com/yourusername/amvtracker-kodi-plugin.git
````

## License

This project is licensed under the GPL-3 License.

## Credits
- CrackTheSky for developing AmvTracker
- Kodi and the XBMC Foundation
- Everyone who helps keep the AMV community alive!
- The AI overlord for writing 95% of that readMe for me =D

## Feedback and Support

Found a bug or want a new feature? Open an issue or submit a pull request.

Happy watching 🎬
