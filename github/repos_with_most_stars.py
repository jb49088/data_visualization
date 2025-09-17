import plotly.express as px
import requests


def main(language=""):
    """Fetch and visualize most-starred GitHub repositories, optionally filtered by language."""
    response = _call_api(language)
    response_dict = response.json()
    _log_api_info(response, response_dict)
    repo_links, repo_names, stars, hover_texts = _extract_data(response_dict)
    _create_visual(language, repo_links, repo_names, stars, hover_texts)


def _call_api(language):
    """Make GitHub API call to search for repositories with >10k stars."""
    if language:
        url = "https://api.github.com/search/repositories"
        url += f"?q=language:{language}+sort:stars+stars:>10000"
    else:
        url = "https://api.github.com/search/repositories"
        url += "?q=stars:>10000+sort:stars"

    headers = {"Accept": "application/vnd.github.v3+json"}
    return requests.get(url, headers=headers)


def _log_api_info(response, response_dict):
    """Print API response status and result completeness."""
    print(f"Status code: {response.status_code}")
    print(f"Complete results: {not response_dict['incomplete_results']}")


def _extract_data(response_dict):
    """Extract repo links, names, stars, and hover text from API response."""
    repo_dicts = response_dict["items"]
    repo_links, repo_names, stars, hover_texts = [], [], [], []
    for repo_dict in repo_dicts:
        # Turn repo names into active links
        repo_name = repo_dict["name"]
        repo_url = repo_dict["html_url"]
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"

        repo_links.append(repo_link)
        repo_names.append(repo_name)
        stars.append(repo_dict["stargazers_count"])

        # Build hover texts
        owner = repo_dict["owner"]["login"]
        description = repo_dict["description"]
        hover_text = f"{owner}<br />{description}"
        hover_texts.append(hover_text)

    return repo_links, repo_names, stars, hover_texts


def _create_visual(language, repo_links, repo_names, stars, hover_texts):
    """Create and display interactive bar chart of repository star counts."""
    if language:
        title = f"Most-Starred {language.title()} Projects on GitHub"
    else:
        title = "Most-Starred Projects on GitHub"
    labels = {"x": "Repository", "y": "Stars"}
    fig = px.bar(
        x=repo_links, y=stars, title=title, labels=labels, hover_name=hover_texts
    )

    # Customize hover template to show clean repo names
    fig.update_traces(
        customdata=repo_names,  # Pass clean names as custom data
        hovertemplate="<b>%{hovertext}</b><br>"
        + "Repository: %{customdata}<br>"
        + "Stars: %{y}<br>"
        + "<extra></extra>",
    )

    fig.update_layout(
        title_font_size=28,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
    )
    fig.update_traces(marker_color="SteelBlue", marker_opacity=0.6)
    fig.show()


if __name__ == "__main__":
    main()
