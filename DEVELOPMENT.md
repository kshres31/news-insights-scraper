# Development summary

- **Project:** Headline Harvest
- **Built:** A headline scraper with retries, link cleanup, limits, and JSON/CSV output.
- **Skills:** HTTP requests, HTML parsing, URL handling, logging, exports, and fixture tests.
- **Problem:** An inline smoke command broke because PowerShell changed its nested quotes.
- **Solution:** Replaced the fragile check with a saved HTML fixture and repeatable unit tests.
- **Next improvement:** Add configurable rules for different site layouts.

