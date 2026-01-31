# grid_client.py
import requests
import json
from typing import Dict, Any, Optional, List, Union

class GridClient:
    # Open Platform Endpoints
    API_URL: str = "https://api-op.grid.gg/central-data/graphql"
    LIVE_URL: str = "https://api-op.grid.gg/live-data-feed/series-state/graphql"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("API Key is missing!")

        self.api_key: str = api_key
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def _execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None, url: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Internal method to execute GraphQL queries."""
        if url is None:
            url = self.API_URL
        try:
            response = requests.post(
                url,
                json={'query': query, 'variables': variables},
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    print("❌ Grid API Error:")
                    print(json.dumps(data['errors'], indent=2))
                    return None
                return data['data']
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return None

    def get_tournaments(self, limit: int = 3) -> Optional[Dict[str, Any]]:
        """Retrieves a list of tournaments."""
        query = f"""
        query GetTournaments {{
          tournaments(first: {limit}) {{
            totalCount
            edges {{
              node {{
                id
                name
              }}
            }}
          }}
        }}
        """
        return self._execute_query(query)

    def get_recent_series(self, limit: int = 5) -> Optional[Dict[str, Any]]:
        """Retrieves a list of recent series (matches) from any tournament."""
        # Using 'baseInfo' as discovered in the GQL Playground documentation
        query = f"""
        query GetRecentSeries {{
          allSeries(
            first: {limit}
            orderBy: StartTimeScheduled
          ) {{
            totalCount
            edges {{
              node {{
                id
                startTimeScheduled
                tournament {{
                    nameShortened
                }}
                teams {{
                  baseInfo {{
                    name
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        return self._execute_query(query)

    def get_match_details(self, series_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Retrieves detailed information for a specific series.
        Includes games, teams, players, and performance stats.
        """
        query = """
        query GetMatchDetails($id: ID!) {
          series(id: $id) {
            id
            format {
              name
            }
            games {
              id
              sequenceNumber
              teams {
                baseInfo {
                  name
                }
                players {
                  player {
                    baseInfo {
                      name
                    }
                  }
                  stats {
                    kills
                    deaths
                    assists
                  }
                }
              }
            }
          }
        }
        """
        variables = {"id": series_id}
        return self._execute_query(query, variables)

    def get_team_stats(self, team_id: str = "83") -> Optional[Dict[str, Any]]:
        """Retrieves statistics for a specific team over the last three months."""
        query = f"""
        query TeamStatisticsForLastThreeMonths {{
          teamStatistics(teamId: "{team_id}", filter: {{ timeWindow: LAST_3_MONTHS }}) {{
            series {{
              count
              kills {{
                sum
                avg
              }}
            }}
            game {{
              count
              wins {{
                percentage
              }}
            }}
            segment {{
              deaths {{
                sum
                avg
              }}
            }}
          }}
        }}
        """
        return self._execute_query(query)

    def get_series_state(self, series_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Retrieves live series state including real-time player stats.
        Uses the Live Data Feed endpoint.
        """
        query = """
        query GetSeriesState($id: ID!) {
          seriesState(id: $id) {
            id
            valid
            games {
              id
              sequenceNumber
              teams {
                name
                score
                players {
                  name
                  kills
                  deaths
                  killAssistsGiven
                }
              }
            }
          }
        }
        """
        variables = {"id": series_id}
        data = self._execute_query(query, variables, url=self.LIVE_URL)
        return data['seriesState'] if data else None