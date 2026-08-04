# pylastfm

Last.fm artist catalog bulk harvester grouped onto the
[harvestkit](https://github.com/LeMetadatarr/harvestkit) resumable-harvest
engine. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper collection into its own standalone package.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `lastfm_artists` | `lastfm_artists` | Last.fm `tag.getTopArtists` + `artist.getInfo`, ~200 tags (requires `LASTFM_API_KEY`) |

## Install

```bash
pip install pylastfm
# or, for the HuggingFace publisher (via harvestkit):
pip install "pylastfm[hf]"
# or, for Cloudflare-guarded sources:
pip install "pylastfm[stealth]"
```

## Usage

```bash
# list every registered scraper
pylastfm-harvest --list

# harvest one source (resumable — safe to Ctrl-C and rerun)
LASTFM_API_KEY=xxx pylastfm-harvest lastfm_artists --output ~/.cache/metadatarr/scrapers/
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
