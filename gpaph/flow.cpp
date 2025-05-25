#include <iostream>
#include <vector>
int max_flow(std::vector<int> adj[], int capacity[][], bool visited[], int s, int t) {
  int flow = 0;
  while (true) {
    std::fill(visited, visited + n, false);
    int f = dfs(adj, capacity, visited, s, t, INF);
    if (f == 0) break;
    flow += f;
  }
  return flow;
}

int main() {
  int n, m;
  std::cin >> n >> m;
  std::vector<int> adj[n]; // список смежности
  int capacity[n][n];      // пропускные способности
  bool visited[n];
  for (int i = 0; i < m; i++) {
    int u, v, c;
    std::cin >> u >> v >> c;
    adj[u].push_back(v);
    capacity[u][v] += c;
  }
  int s, t;
  std::cin >> s >> t;
  std::cout << "Maximum flow: " << max_flow(adj, capacity, s, t) << std::endl;
}
