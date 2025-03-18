from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from wiki_music.url_finder import get_random_music_url_with_summary

app = FastAPI(
    title="Wiki Music API",
    description="API for finding random Wikipedia articles about music"
)

# Configure CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/random-music")
async def get_random_music():
    """Get a random Wikipedia article about music."""
    try:
        url, summary = get_random_music_url_with_summary()
        return {
            "url": url,
            "summary": summary,
            # Wikipedia URLs can be embedded by adding /embed/ after wikipedia.org
            "embed_url": url.replace("wikipedia.org", "wikipedia.org/embed")
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 