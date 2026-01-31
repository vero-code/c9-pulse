# grid_client.py
import requests
import json
from typing import Dict, Any, Optional, List, Union

class GridClient:
    # Open Platform Endpoints
    API_URL: str = "https://api-op.grid.gg/central-data/graphql"
    LIVE_URL: str = "https://api-op.grid.gg/live-data-feed/series-state/graphql"

    def __init__(self, api_key: str) -> None:
        """
        Initialize Grid API client.
        
        Args:
            api_key: GRID API authentication key.
        """
        if not api_key:
            raise ValueError("API Key is missing!")

        self.api_key: str = api_key
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def _execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None, url: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a GraphQL query against the GRID API.
        
        Args:
            query: The GraphQL query string.
            variables: Optional variables for the query.
            url: The API endpoint URL. Defaults to central data API.
            
        Returns:
            The 'data' portion of the response or None if the request fails.
        """
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
        """
        Retrieve a list of available tournaments.
        
        Args:
            limit: Maximum number of tournaments to return.
            
        Returns:
            Tournament data dictionary or None.
        """
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
        """
        Retrieve a list of recently started or scheduled series.
        
        Args:
            limit: Maximum number of series to return.
            
        Returns:
            Series list data dictionary or None.
        """
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
        Retrieve comprehensive details for a specific match series.
        
        Args:
            series_id: The ID of the series.
            
        Returns:
            Detailed series data or None.
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
        """
        Retrieve historical performance statistics for a specific team.
        
        Args:
            team_id: The ID of the team.
            
        Returns:
            Team statistics data or None.
        """
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
        Retrieve real-time state and player stats for a live or recent series.
        
        Args:
            series_id: The ID of the series.
            
        Returns:
            Current series state data or None.
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