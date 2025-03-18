import uvicorn

def main():
    uvicorn.run(
        "wiki_music.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )

if __name__ == "__main__":
    main() 