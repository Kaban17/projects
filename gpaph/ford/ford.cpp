#include <iostream>
#include <vector>
#include <queue>
#include <climits>
#include <algorithm>
#include <map>

using namespace std;

class Graph {
    int V;
    vector<vector<int>> capacity;
    vector<vector<int>> flow; // Матрица потоков
    vector<vector<int>> adj;

public:
    Graph(int V) : V(V) {
        capacity.resize(V, vector<int>(V, 0));
        flow.resize(V, vector<int>(V, 0));
        adj.resize(V);
    }

    void addEdge(int u, int v, int cap) {
        adj[u].push_back(v);
        adj[v].push_back(u);
        capacity[u][v] = cap;
    }

    bool bfs(int s, int t, vector<int>& parent) {
        fill(parent.begin(), parent.end(), -1);
        queue<int> q;
        q.push(s);
        parent[s] = -2;

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : adj[u]) {
                if (parent[v] == -1 && capacity[u][v] > flow[u][v]) {
                    parent[v] = u;
                    if (v == t) return true;
                    q.push(v);
                }
            }
        }
        return false;
    }

    int maxFlow(int s, int t) {
        int total_flow = 0;
        vector<int> parent(V);

        while (bfs(s, t, parent)) {
            int path_flow = INT_MAX;
            for (int v = t; v != s; v = parent[v]) {
                int u = parent[v];
                path_flow = min(path_flow, capacity[u][v] - flow[u][v]);
            }

            for (int v = t; v != s; v = parent[v]) {
                int u = parent[v];
                flow[u][v] += path_flow;
                flow[v][u] -= path_flow; // Учитываем обратное ребро
            }

            total_flow += path_flow;
        }

        return total_flow;
    }

    // Вывод ненулевых потоков
    void printFlow() {
        cout << "Распределение потока по рёбрам:\n";
        for (int u = 0; u < V; ++u) {
            for (int v : adj[u]) {
                if (flow[u][v] > 0) {
                    cout << u << " -> " << v << ": " << flow[u][v] << "/" << capacity[u][v] << endl;
                }
            }
        }
    }
};

int main() {
    int V = 8; // Вершины 0..7 (1..7 в задании)
    Graph g(V);

    // Добавляем рёбра (start, end, capacity)
    g.addEdge(1, 3, 12);
    g.addEdge(1, 4, 9);
    g.addEdge(1, 6, 7);
    g.addEdge(2, 3, 8);
    g.addEdge(2, 4, 5);
    g.addEdge(2, 5, 9);
    g.addEdge(2, 7, 13);
    g.addEdge(3, 4, 6);
    g.addEdge(3, 5, 5);
    g.addEdge(3, 7, 5);
    g.addEdge(4, 5, 13);
    g.addEdge(4, 7, 7);
    g.addEdge(5, 6, 4);
    g.addEdge(6, 3, 15);
g.addEdge(6, 2, 3);
    int source = 1;
    int sink = 7;

    int max_flow = g.maxFlow(source, sink);
    cout << "Максимальный поток: " << max_flow << "\n\n";

    g.printFlow(); // Вывод фактических потоков

    return 0;
}
