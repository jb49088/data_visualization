import plotly.express as px
import requests


def main(sort_by, language=""):
    response = _call_api(sort_by, language)
    response_dict = response.json()
    _log_api_info(response, response_dict)
    repo_links, repo_names, sort_values, hover_texts = _extract_data(
        sort_by, response_dict
    )
    _create_visual(language, repo_links, repo_names, sort_values, hover_texts, sort_by)


def _call_api(sort_by, language):
    url = _construct_url(sort_by, language)
    headers = {"Accept": "application/vnd.github.v3+json"}
    return requests.get(url, headers=headers)


def _construct_url(sort_by, language):
    base_url = "https://api.github.com/search/repositories"

    if sort_by == "stars":
        query = "stars:>10000&sort=stars&order=desc"
    elif sort_by == "forks":
        query = "forks:>10000&sort=forks&order=desc"

    if language:
        query = f"language:{language}+" + query

    return f"{base_url}?q={query}"


def _log_api_info(response, response_dict):
    print(f"Status code: {response.status_code}")
    print(f"Complete results: {not response_dict['incomplete_results']}")


def _extract_data(sort_by, response_dict):
    repo_dicts = response_dict["items"]
    repo_links, repo_names, sort_values, hover_texts = [], [], [], []

    for repo_dict in repo_dicts:
        repo_name = repo_dict["name"]
        repo_url = repo_dict["html_url"]
        repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
        repo_links.append(repo_link)
        repo_names.append(repo_name)

        if sort_by == "stars":
            value = repo_dict["stargazers_count"]
        elif sort_by == "forks":
            value = repo_dict["forks_count"]

        sort_values.append(value)
        owner = repo_dict["owner"]["login"]
        description = repo_dict["description"]
        hover_text = f"{owner}<br />{description}"
        hover_texts.append(hover_text)

    return repo_links, repo_names, sort_values, hover_texts


def _create_visual(
    language, repo_links, repo_names, y_values, hover_texts, sort_by_str
):
    metrics = {"stars": ("Starred", "Stars"), "forks": ("Forked", "Forks")}

    verb, y_label = metrics[sort_by_str]

    title = (
        f"Most-{verb} {language.title()} Repositories on GitHub"
        if language
        else f"Most-{verb} Repositories on GitHub"
    )

    labels = {"x": "Repository", "y": y_label}
    fig = px.bar(
        x=repo_links, y=y_values, title=title, labels=labels, hover_name=hover_texts
    )
    fig.update_traces(
        customdata=repo_names,
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Repository: %{customdata}<br>"
            f"{y_label}: %{{y}}<br>"
            "<extra></extra>"
        ),
    )
    fig.update_layout(
        title_font_size=28,
        xaxis_title_font_size=20,
        yaxis_title_font_size=20,
    )
    fig.update_traces(marker_color="SteelBlue", marker_opacity=0.6)
    fig.show()


if __name__ == "__main__":
    main("forks", "python")
