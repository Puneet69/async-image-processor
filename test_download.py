import requests

url = "https://photos.google.com/share/AF1QipON2kqRoqul6i5hQD8xixc4xOQOQ412wo6flNs2ZrNHy86Rg6Xt0uX97YIFkcS7Gg/photo/AF1QipMvB4a-vUtUvJuWgv9dPEp_YnVQGibtE-PntEYf?key=Tk1pUDBORHBuZEFvc21kVEhISzVNYndDd1R5RUJ3"

try:
    response = requests.get(url)
    response.raise_for_status()  # raise error for bad status
    print(f"Image downloaded successfully! Size: {len(response.content)} bytes")
except Exception as e:
    print(f"Failed to download image: {e}")
