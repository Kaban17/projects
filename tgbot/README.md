# SRT Subtitle Processor API

This project is a FastAPI-based API for processing `.srt` subtitle files.

## Features

-   **Accepts `.srt` files**: Upload `.srt` files via an API endpoint.
-   **Text Analysis**: Extracts all unique words from the subtitles.
-   **Translation**: Translates the unique words to Russian.
-   **New File Generation**: Creates a new `.srt` file with word translations appended to each subtitle line.
-   **Statistics**: Calculates the top 100 most frequent words, total word count, and unique word count.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd tgbot
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    poetry install
    ```

3.  **Activate the virtual environment:**
    ```bash
    poetry shell
    ```

## Running the Application

To start the API server, run the following command:
```bash
python3 main.py
```
The API server will be available at `http://localhost:8000`.

## API Usage

You can interact with the API through the documentation available at `http://localhost:8000/docs` or using tools like `curl`.

### Processing a file

Send a `POST` request to the `/process-srt/` endpoint with your `.srt` file attached.

**Example with `curl`:**
```bash
curl -X POST -F "file=@/path/to/your/file.srt" http://localhost:8000/process-srt/
```

### Response

On success, you will receive a JSON response containing statistics and a download link:

```json
{
  "message": "File processed successfully.",
  "statistics": { ... },
  "download_url": "/downloads/translated_your_file.srt"
}
```

You can download the processed file from the provided `download_url`.