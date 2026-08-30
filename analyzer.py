import httpx

GITHUB_API = "https://api.github.com"


async def get_user_profile(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API}/users/{username}")

        if response.status_code == 404:
            return None
            
        return response.json()

async def get_user_repos(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/users/{username}/repos",
            params = {"per_page": 100, "sort": "updated"}
        )
        return response.json()


def analyze_repos(repos: list):
    if not repos:
        return{}

    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    top_languages = sorted(languages, key=lambda x: languages[x], reverse=True)[:8]

    most_starred = max(repos, key=lambda r: r.get("stargazers_count", 0))

    total_stars = sum(r.get("stargazers_count", 0) for r in repos)

    return{
        "total_repos": len(repos),
        "top_languages": top_languages,
        "total_stars": total_stars,
        "avg_stars": round(total_stars/len(repos), 2),
        "most_starred_repo": {
            "name": most_starred["name"],
            "stars": most_starred["stargazers_count"],
            "url": most_starred["html_url"]
        }
    }

async def analyze_user(username: str):
    profile = await get_user_profile(username)

    if profile is None:
        return None

    repos = await get_user_repos(username)
    repo_stats = analyze_repos(repos)

    return{
        "username": profile["login"],
        "name": profile.get("name", "Not provided"),
        "bio": profile.get("bio", "Not provided"),
        "followers": profile["followers"],
        "following": profile["following"],
        "public_repos": profile["public_repos"],
        "account_created": profile["created_at"][:10],
        "profile_url": profile["html_url"],
        **repo_stats  
    }