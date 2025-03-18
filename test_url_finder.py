from wiki_music.url_finder import get_random_music_url, get_random_music_url_with_summary

print("Finding a random music URL...")
url = get_random_music_url()
print(f"Found URL: {url}")

print("\nFinding another with its summary...")
url, summary = get_random_music_url_with_summary()
print(f"Summary: {summary}")
print(f"URL: {url}") 