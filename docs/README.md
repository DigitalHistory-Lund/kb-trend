# KB-Trend Web Interface

A browser-based tool for querying Swedish National Library newspaper archives and downloading results as CSV.

## Usage

Open `index.html` in a web browser or visit the GitHub Pages URL.

### Form Input Mode

1. Enter a keyword to search for
2. Optionally specify:
   - Journal name (leave blank to search all journals)
   - Date range (from/to years)
   - Proximity markers for specialized searches
3. Click "Search & Download CSV"
4. CSV file downloads automatically with ISO datetime filename

### Direct API URL Mode

1. Switch to "Direct API URL" tab
2. Paste a complete KB.se API URL
3. Click "Fetch & Download CSV"
4. CSV file downloads automatically

## Features

- **Bookmarkable URLs**: All search parameters are in the URL, so you can bookmark or share searches
- **Auto-run**: Add `&autorun=true` to URL to automatically execute the search on page load
- **CSV Format**: Includes metadata (search URL, SPA URL, datetime) in the header, followed by year,count data

## Example URLs

Form mode:
```
?mode=form&keyword=gosse&from=1900&to=2000
```

Direct mode:
```
?mode=direct&apiurl=https://data.kb.se/search/?q=ja&searchGranularity=part
```

Auto-run:
```
?mode=form&keyword=gosse&autorun=true
```

## CSV Output

Each CSV file is named with an ISO datetime (e.g., `2025-01-15T103045Z.csv`) and contains:

```csv
# KB-Trend Search Results
# Encoding: UTF-8
# Search URL: https://data.kb.se/search/?q=...
# SPA URL: https://...
# Search datetime: 2025-01-15T10:30:45Z
#
year,count
1900,123
1901,456
...
```

**Note**: Files are UTF-8 encoded. Metadata lines (starting with #) appear above the CSV header.

## GitHub Pages Setup

To host this on GitHub Pages:

1. Ensure this `docs/` folder is in your repository
2. Go to Settings → Pages
3. Set Source to "Deploy from a branch"
4. Select branch (`main` or `dev`) and folder (`/docs`)
5. Save and wait for deployment

The site will be available at: `https://USERNAME.github.io/REPO-NAME/`
