import requests
import os

PERSONAL_ACCESS_TOKEN = os.environ.get("PERSONAL_ACCESS_TOKEN", "")

def run_graphql_query(query):
    headers = {"Authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}"}
    request = requests.post(
        "https://api.github.com/graphql", json={"query": query}, headers=headers
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed to run by returning code {request.status_code}")
        
def collect_issues(organization, label):
    """
    Fetches all issues from organization with the particular label.
    Returns a list of (title, url) tuples.
    """
    query = r"""
    {
      search(first: 100, type: ISSUE, query: "is:open is:issue archived:false user:%s label:\"%s\"") {
        edges {
          node {
            ... on Issue {
              createdAt
              title
              url
            }
          }
        }
      }
    }
    """ % (
        organization,
        label,
    )

    query_result = run_graphql_query(query)
    nodes = query_result["data"]["search"]["edges"]

    return list(map(lambda n: (n["node"]["title"], n["node"]["url"]), nodes))

def main():
    print("# Good first issues")
    for (title, url) in collect_issues("coderefinery", "good first issue"):
        print(f"- [{title}]({url})")

if __name__ == "__main__":
    main()
