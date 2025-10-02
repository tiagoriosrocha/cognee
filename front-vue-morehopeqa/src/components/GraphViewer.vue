<template>
  <div class="graph-container">
    <v-network-graph
      :nodes="nodes"
      :edges="edges"
      :configs="configs"
      :event-handlers="graphEvents"
    />
  </div>
</template>

<script>
import * as vNG from "v-network-graph";
import { ForceLayout } from "v-network-graph/lib/force-layout";

export default {
  name: "GraphViewer",
  props: {
    nodes: {
      type: Object,
      default: () => ({}),
    },
    edges: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      configs: vNG.defineConfigs({
        view: {
          layoutHandler: new ForceLayout({
            positionFixedByDrag: false,
            positionFixedByClickWithAltKey: true,
            createSimulation: (d3, nodes, edges) => {
              const forceLink = d3.forceLink(edges).id((d) => d.id);
              return d3
                .forceSimulation(nodes)
                .force("link", forceLink.distance(100).strength(0.5))
                .force("charge", d3.forceManyBody().strength(-500))
                .force("center", d3.forceCenter())
                .force("collide", d3.forceCollide(50))
                .alphaMin(0.001);
            },
          }),
        },
        node: {
          normal: {
            radius: 15,
            color: (node) => {
              switch (node.type) {
                case "entity":
                  return "#6c8cff"; // azul
                case "ontolgy":
                  return "#ff6c6c"; // vermelho
                case "individual":
                  return "#6cff8c"; // verde
                default:
                  return "#cccccc"; // cinza padrão
              }
            },
          },
          label: {
            visible: true,
            fontSize: 12,
            textAnchor: "middle",
          },
        },
        edge: {
          normal: {
            width: 1,
            color: "#999",
          },
          label: {
            color: "#555",
            fontSize: 10,
          },
        },
      }),
    };
  },
  computed: {
    graphEvents() {
      return {
        "node:click": (nodeId) => {
          const nodeData = this.nodes[nodeId.node];
          console.log("Nodo clicado:", nodeData);
          this.$emit("node-selected", nodeData);
        },
      };
    },
  },
};
</script>

<style scoped>
.graph-container {
  width: 100%;
  height: 600px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}
</style>
