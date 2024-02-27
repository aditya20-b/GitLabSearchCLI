import requests
import json
import argparse
import time
import os
import logging
from tqdm import tqdm


def setup_logger():
    """
    Set up a basic logger.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def get_gitlab_repos(api_key, keyword, per_page=20, additional_filters=None):
    """
    Search GitLab repositories using the specified keyword and handle pagination.

    :param api_key: GitLab API key for authentication.
    :param keyword: Keyword to search for in the repositories.
    :param per_page: Number of results per page.
    :param additional_filters: Dictionary of additional search filters such as {'language': 'Python'}.
    :return: List of repositories.
    """
    all_repos = []
    page = 1
    api_url = "https://gitlab.com/api/v4/projects"
    headers = {"PRIVATE-TOKEN": api_key}
    params = {"search": keyword, "per_page": per_page}

    if additional_filters:
        params.update(additional_filters)

    try:
        initial_response = requests.get(api_url, headers=headers, params=params)
        initial_response.raise_for_status()  # Raise exception if status code is not 200
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        return all_repos

    total_pages = int(initial_response.headers.get("X-Total-Pages", 1))

    with tqdm(total=total_pages, desc="Fetching Pages") as progress_bar:
        while page <= total_pages:
            params["page"] = page
            response = requests.get(api_url, headers=headers, params=params)

            if response.status_code == 429:
                # Handle rate limiting
                logging.warning(
                    f"Rate limit exceeded. Retrying after {response.headers.get('Retry-After', 60)} seconds."
                )
                time.sleep(int(response.headers.get("Retry-After", 60)))
                continue
            elif response.status_code != 200:
                logging.error(f"Failed to fetch data: {response.status_code}")
                break

            repos = response.json()
            all_repos.extend(repos)
            page += 1
            progress_bar.update(1)

    return all_repos


def format_results(keyword, repos):
    """
    Format the list of repositories into the desired JSON structure.

    :param keyword: Search keyword.
    :param repos: List of repositories.
    :return: JSON string of the formatted results.
    """
    formatted_results = {
        "Keyword": keyword,
        "repos": [{"name": repo["name"], "url": repo["web_url"]} for repo in repos],
    }

    return json.dumps(formatted_results, indent=4)


def main():
    api_key = os.environ.get("GITLAB_API_KEY")
    parser = argparse.ArgumentParser(description="Search GitLab repositories.")
    parser.add_argument("--api_key", help="GitLab API key", default=api_key)
    parser.add_argument("keyword", help="Keyword to search for")
    parser.add_argument(
        "--per_page", help="Number of results per page", type=int, default=20
    )
    parser.add_argument("--output", "-o", help="Output file name", default=False)

    args = parser.parse_args()

    setup_logger()
    logging.info("Starting GitLab repository search...")

    if not args.api_key:
        logging.error(
            "GitLab API key not found. Set the GITLAB_API_KEY environment variable or pass it as an argument."
        )
        return

    repos = get_gitlab_repos(args.api_key, args.keyword, args.per_page)
    if not repos:
        logging.info("No repositories found.")
        return

    results = format_results(args.keyword, repos)

    if args.output:
        with open(args.output, "w") as f:
            f.write(results)
        logging.info(f"Results saved to {args.output}")
    print(results)


if __name__ == "__main__":
    main()
