<template>
  <div class="graph-container">
    <v-network-graph :nodes="nodes" :edges="edges" />
  </div>
</template>

<script>
export default {
  name: "GraphViewer",
  data() {
    return {
      nodes: {
        "803c8a2a-b00a-50a6-8b0f-9f813d689532": {
          name: "Node 803c8a2a...",
        },
        "6bd2234d-5266-5519-bfa9-f2a746931895": {
          name: "text_253becda393cc4221094e8eb3cabf879",
        },
        "b661854d-2f9b-5b09-93f9-77be0be05db9": {
          name: "rachel elizabeth lynne mckee wallingford",
        },
      },
      edges: {
        edge1: {
          source: "803c8a2a-b00a-50a6-8b0f-9f813d689532",
          target: "6bd2234d-5266-5519-bfa9-f2a746931895",
        },
        edge2: {
          source: "803c8a2a-b00a-50a6-8b0f-9f813d689532",
          target: "b661854d-2f9b-5b09-93f9-77be0be05db9",
        },
      },
    };
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
