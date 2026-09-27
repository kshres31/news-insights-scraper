import argparse, csv, json, logging, time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
from .parser import Headline, parse_headlines

def fetch(url: str, retries: int = 2) -> str:
    request=Request(url,headers={"User-Agent":"HeadlineHarvest/0.1 (+educational portfolio project)"})
    for attempt in range(retries+1):
        try:
            with urlopen(request,timeout=10) as response: return response.read().decode(response.headers.get_content_charset() or "utf-8")
        except URLError:
            if attempt == retries: raise
            wait=2**attempt; logging.warning("Request failed; retrying in %s second(s)",wait); time.sleep(wait)
    raise RuntimeError("request failed")

def export(items: list[Headline], path: Path) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.suffix.lower()==".json": path.write_text(json.dumps([item.as_dict() for item in items],indent=2),encoding="utf-8")
    elif path.suffix.lower()==".csv":
        with path.open("w",newline="",encoding="utf-8") as stream:
            writer=csv.DictWriter(stream,fieldnames=["title","url"]); writer.writeheader(); writer.writerows(item.as_dict() for item in items)
    else: raise ValueError("output must end in .json or .csv")

def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description="Collect linked headlines from a web page")
    parser.add_argument("url"); parser.add_argument("--output","-o",type=Path,default=Path("headlines.json")); parser.add_argument("--limit",type=int,default=25)
    args=parser.parse_args(argv)
    if args.limit<1: parser.error("limit must be positive")
    logging.basicConfig(level=logging.INFO,format="%(levelname)s: %(message)s")
    try: items=parse_headlines(fetch(args.url),args.url)[:args.limit]; export(items,args.output)
    except (OSError,ValueError) as exc: logging.error("%s",exc); return 1
    print(f"Saved {len(items)} headlines to {args.output}"); return 0

if __name__=="__main__": raise SystemExit(main())

