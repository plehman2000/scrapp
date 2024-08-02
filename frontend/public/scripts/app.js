// Create a new graph
const graph = new graphology.Graph();

// Add some nodes
graph.addNode('A', { x: 0, y: 0, size: 10, label: 'Node A', color: '#ff0000' });
graph.addNode('B', { x: 1, y: 1, size: 10, label: 'Node B', color: '#00ff00' });
graph.addNode('C', { x: -1, y: 1, size: 10, label: 'Node C', color: '#0000ff' });

// Add some edges
graph.addEdge('A', 'B');
graph.addEdge('B', 'C');
graph.addEdge('C', 'A');

// Create the renderer
const container = document.getElementById('sigma-container');
const renderer = new sigma.Sigma(graph, container);

// Refresh the renderer
renderer.refresh();
