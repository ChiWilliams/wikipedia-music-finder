import uvicorn

def main():
    uvicorn.run(
        "wiki_music.api.main:app",
        host="0.0.0.0",
        port=8000,
    )

if __name__ == "__main__":
    main() 