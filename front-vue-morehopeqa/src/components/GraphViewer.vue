<template>
  <div class="graph-container">
    <v-network-graph
      :nodes="nodes"
      :edges="edges"
      :layouts="layouts"
      :configs="configs"
      :event-handlers="graphEvents"
    />
  </div>
</template>

<script>
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
      layouts: {
        nodeSpacing: 100,
      },
      configs: {
        view: {
          scalingObjects: true,
          layout: "force",
          fit: true,
          zoom: 0.5,
        },
        node: {
          normal: {
            color: "#6c8cff",
          },
          label: {
            color: "#000",
            fontFamily: "sans-serif",
            fontSize: 10,
            textAnchor: "start",
          },
        },
        edge: {
          normal: {
            color: "#999",
            width: 1,
          },
          label: {
            color: "#555",
            fontSize: 3,
          },
        },
      },
    };
  },
  methods: {
    handleNodeClick(nodeId) {
      console.log("componente - clicou no nó", nodeId.node);
      //const nodeData = this.nodes[nodeId]; //pega os dados
      this.$emit("node-selected", { id: nodeId.node }); //emite para o pai
    },
  },
  computed: {
    graphEvents() {
      return {
        "node:click": this.handleNodeClick,
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
}
</style>
