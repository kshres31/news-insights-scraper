# Headline Harvest

A small command-line tool that collects linked headlines from an HTML page. It uses only the Python standard library and limits itself to links inside heading tags.

## Run

Check a site's terms and `robots.txt` before scraping it. Use a slow, reasonable schedule.

```powershell
$env:PYTHONPATH = "src"
python -m headline_harvest.cli "https://example.com/news" --output headlines.json
python -m headline_harvest.cli "https://example.com/news" --output headlines.csv --limit 10
```

The client sends a clear user agent, retries temporary request failures, resolves relative links, removes duplicates, and exports JSON or CSV.

Run offline tests with `python -m unittest discover -s tests -v`. A future version could read site-specific selectors from configuration.

