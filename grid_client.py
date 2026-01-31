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
            pageInfo {{
              hasPreviousPage
              hasNextPage
              startCursor
              endCursor
            }}
            totalCount
            edges {{
              cursor
              node {{
                id
                name
                nameShortened
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
        query = f"""
        query GetRecentSeries {{
          allSeries(
            first: {limit}
            orderBy: StartTimeScheduled
          ) {{
            totalCount
            pageInfo {{
              hasPreviousPage
              hasNextPage
              startCursor
              endCursor
            }}
            edges {{
              cursor
              node {{
                id
                title {{
                  nameShortened
                }}
                tournament {{
                  nameShortened
                }}
                startTimeScheduled
                format {{
                  name
                  nameShortened
                }}
                teams {{
                  baseInfo {{
                    id
                    name
                    logoUrl
                    colorPrimary
                    colorSecondary
                  }}
                  scoreAdvantage
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
            title {
              nameShortened
            }
            tournament {
              nameShortened
            }
            startTimeScheduled
            format {
              name
              nameShortened
            }
            teams {
              baseInfo {
                id
                name
                logoUrl
                colorPrimary
                colorSecondary
              }
              scoreAdvantage
            }
          }
        }
        """
        variables = {"id": series_id}
        return self._execute_query(query, variables)

    def get_team_stats(self, team_id: str = "83") -> Optional[Dict[str, Any]]:
        """
        Note: The teamStatistics field is currently not available in the Central Data API.
        This method is kept for future compatibility but returns None to avoid errors.
        """
        # query = f"""
        # query TeamStatisticsForLastThreeMonths {{
        #   teamStatistics(teamId: "{team_id}", filter: {{ timeWindow: LAST_3_MONTHS }}) {{
        #     id
        # ...
        # """
        return None

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
            valid
            updatedAt
            format
            started
            finished
            teams {
              name
              won
            }
            games {
              sequenceNumber
              teams {
                name
                score
                players {
                  name
                  kills
                  deaths
                  netWorth
                  money
                  position {
                    x
                    y
                  }
                }
              }
            }
          }
        }
        """
        variables = {"id": series_id}
        data = self._execute_query(query, variables, url=self.LIVE_URL)
        return data['seriesState'] if data else None