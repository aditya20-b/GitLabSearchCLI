# GitLab Repository Search Tool

## Introduction
The GitLab Repository Search Tool is a Python script designed to search GitLab repositories using a specified keyword. It utilizes the GitLab API to fetch repositories that match the keyword and formats the results in JSON. This tool is useful for developers, researchers, or anyone interested in finding GitLab repositories by keywords related to their interests or projects.


## Features
- **Keyword Searching**: Allows users to search for repositories using specific keywords.
- **Pagination Handling**: Manages API pagination to fetch all results.
- **Rate Limit Handling**: Includes handling of GitLab's API rate limits.
- **Output Customization**: Users can specify an output file to save the search results.

## Installation
1. **Clone the Repository:**
```sh
git clone https://github.com/aditya20-b/GitLabSearchCLI.git
cd GitLabSearchCLI
```
2. **Install Dependencies:**
```sh
pip install -r requirements.txt
```

## Usage
```sh
python3 gitlab_search.py [-h] [-o OUTPUT] [-p PAGE_SIZE] [-l] [-v] keyword
```
### Arguments
| Argument | Description |
| --- | --- |
| keyword | Keyword to search for in GitLab repositories. |
| -h, --help | Show the help message and exit. |
| -o OUTPUT, --output OUTPUT | Output file to save the search results. |
| -p PAGE_SIZE, --page_size PAGE_SIZE | Number of results to fetch per page. |
| -l, --log | Enable logging. |
| -v, --verbose | Enable verbose logging. |

### Examples
- **Basic Usage:**
```sh
python3 gitlab_search.py "python"
```
- **With All Options:**
```sh
python gitlab_search.py --api_key "your_api_key_here" "keyword" --per_page 30 --output "result.json"
```

Replace `your_api_key_here` with your GitLab API key. You can generate a new API key by going to your GitLab profile settings and navigating to `Access Tokens` under `Access Tokens & SSH Keys`.

## License
This project is licensed under the MIT License. See `LICENSE` for more information.
