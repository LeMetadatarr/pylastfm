# Dataset

## What this repo produces

`pylastfm` harvests artist profiles from Last.fm. It walks about 200 music tags through the `tag.getTopArtists` endpoint and enriches each artist with `artist.getInfo`. The output is one JSONL file where each row is a distinct artist.

## Dataset format

One row per artist. Each row is a JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `mbid` | string or null | MusicBrainz identifier when available. |
| `name` | string | Artist name. |
| `url` | string | Last.fm artist page URL. |
| `listeners` | integer or null | Number of Last.fm listeners. |
| `playcount` | integer or null | Number of Last.fm plays. |
| `tags` | list of strings | Up to 15 genre or descriptor tags. |
| `similar_artists` | list of strings | Up to 10 related artist names. |
| `bio_summary` | string or null | Short biography text, truncated to 600 characters. |
| `entity_type` | string | Always `"musician"`. |

## How to generate it

Install the package and run the harvester with a Last.fm API key:

```bash
pip install pylastfm
LASTFM_API_KEY=xxx pylastfm-harvest lastfm_artists \
  --output ~/.cache/metadatarr/scrapers/
```

The harvest is resumable. You can stop it with Ctrl-C and rerun the same command to continue from the last checkpoint.

## Worth publishing on Hugging Face?

Yes. The dataset is a clean, structured artist catalog with tags, listener counts, similar-artist links, and short biographies. It is useful for music research and contains no personally identifiable information.

## ML tasks served

- Music recommendation and similarity modeling.
- Artist genre and tag classification.
- Entity linking between Last.fm names and other music databases.
- Knowledge graph construction for artists, genres, and relationships.
