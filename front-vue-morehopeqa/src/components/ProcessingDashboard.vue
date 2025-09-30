<template>
  <v-card class="pa-4" outlined>
    <v-card-title class="text-h6 font-weight-medium">
      Processar com Cognee
    </v-card-title>
    <v-card-text>
      <v-row align="center">
        <v-col cols="12" md="10">
          <v-combobox
            label="Selecione o Tipo de Processamento"
            :items="processingOptions"
            item-title="text"
            item-value="value"
            v-model="selectedProcessingType"
            variant="outlined"
            density="compact"
            hide-details
          ></v-combobox>
        </v-col>
        <v-col cols="12" md="2">
          <v-btn
            color="primary"
            block
            size="large"
            :disabled="!selectedProcessingType || !selectedItem"
            :loading="processing"
            @click="processar"
          >
            Processar
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>

  <v-row v-if="processedAnswer">
    <v-col cols="12">
      <v-card class="pa-4 mt-2" outlined>
        <v-card-title class="text-h6 font-weight-medium">
          Resposta Final:
        </v-card-title>
        <v-card-text>{{ processedAnswer }}</v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <v-row v-if="processedAnswer">
    <v-col cols="12" md="8">
      <v-card class="pa-4 min-h-600" outlined>
        <v-card-title class="text-h6 font-weight-medium">
          Grafo do Processamento Cognee
        </v-card-title>
        <v-card-text class="d-flex align-center justify-center fill-height">
          <GraphViewer
            :nodes="graphData.nodes"
            :edges="graphData.edges"
            @node-selected="onNodeSelected"
          ></GraphViewer>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="12" md="4">
      <v-card class="pa-4 min-h-600" outlined>
        <v-card-title class="text-h6 font-weight-medium">
          Detalhes do Nodo
        </v-card-title>
        <v-card-text>
          <div v-if="selectedNode">
            <v-list dense>
              <v-list-item v-for="(value, key) in selectedNode" :key="key">
                <v-list-item-title
                  ><strong>{{ key }}:</strong></v-list-item-title
                >
                <v-list-item-subtitle class="wrap-text">{{
                  typeof value === "object" ? JSON.stringify(value) : value
                }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </div>
          <p v-else class="text-medium-emphasis">
            Selecione um nó do grafo para ver os detalhes.
          </p>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <v-divider v-if="processedAnswer" class="my-6"></v-divider>

  <v-row v-if="processedAnswer">
    <v-col cols="12">
      <v-card class="pa-4" outlined>
        <v-card-title class="text-h6 font-weight-medium">
          Detalhes das Propriedades do Grafo
        </v-card-title>
        <v-card-text>
          <v-table>
            <thead>
              <tr>
                <th class="text-left">ID do Nó</th>
                <th class="text-left">Nome do Nó</th>
                <th class="text-left">Outras Propriedades</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(node, id) in graphData.nodes" :key="id">
                <td>{{ id }}</td>
                <td>{{ node.name }}</td>
                <td>
                  <div v-for="(value, key) in node" :key="key">
                    <span v-if="key !== 'name'">
                      <strong>{{ key }}:</strong>
                      {{
                        typeof value === "object"
                          ? JSON.stringify(value)
                          : value
                      }}
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>

  <v-snackbar
    v-model="snackbar"
    :timeout="3000"
    :color="snackbarColor"
    location="bottom"
  >
    {{ snackbarMessage }}
  </v-snackbar>

  <v-snackbar
    v-model="processingSnackbar"
    :timeout="0"
    color="info"
    location="bottom"
  >
    Processando a requisição, por favor aguarde...
    <v-progress-circular
      indeterminate
      color="white"
      class="ml-4"
      size="20"
    ></v-progress-circular>
  </v-snackbar>
</template>

<script>
import GraphViewer from "./GraphViewer.vue";

export default {
  name: "ProcessingDashboard",
  components: {
    GraphViewer,
  },
  props: {
    selectedItem: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      processingOptions: [
        { text: "Main question", value: 1 },
        { text: "Sequence questions", value: 2 },
        { text: "Main question with ontology", value: 3 },
        { text: "Sequence question with ontology", value: 4 },
      ],
      selectedProcessingType: null,
      processing: false,
      processedAnswer: null,
      snackbar: false,
      snackbarMessage: "",
      snackbarColor: "",
      processingSnackbar: false,
      graphData: {
        nodes: {},
        edges: {},
      },
      selectedNode: null,
    };
  },
  computed: {},
  mounted() {
    if (this.processingOptions.length > 0) {
      this.selectedProcessingType = this.processingOptions[0].value;
    }
  },
  methods: {
    async processar() {
      if (!this.selectedItem || this.selectedProcessingType === null) {
        this.showSnackbar(
          "Por favor, selecione uma pergunta e um tipo de processamento.",
          "error"
        );
        return;
      }

      //this.processing = true;
      this.processingSnackbar = true;

      const payload = {
        selectedQuestion: this.selectedItem,
        processingType: this.selectedProcessingType,
      };

      try {
        const response = await fetch("http://localhost:5000/runquestion", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`Erro na requisição: ${response.statusText}`);
        }

        const data = await response.json();

        this.processedAnswer = data.final_answer;
        this.graphData.nodes = data.nodes;
        this.graphData.edges = data.edges;

        this.showSnackbar("Requisição concluída com sucesso!", "success");
        console.log("Resposta da API:", data);
      } catch (error) {
        this.showSnackbar("Ocorreu um erro no processamento.", "error");
        console.error("Erro na requisição:", error);
      } finally {
        // this.processing = false;
        this.processingSnackbar = false;
      }
    },
    onNodeSelected(node) {
      console.log("Nodo clicado:", node);
      this.selectedNode = node;
    },
    showSnackbar(message, color) {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.snackbar = true;
    },
  },
};
</script>

<style scoped>
.min-h-600 {
  min-height: 600px;
}
.wrap-text {
  white-space: normal !important;
}
.context-wrapper,
.subquestions-wrapper {
  white-space: normal;
  overflow: visible;
  margin-top: 8px;
}
.context-list,
.subquestions-list {
  list-style-type: none;
  padding-left: 0;
}
.context-list li,
.subquestions-list li {
  margin-bottom: 8px;
  line-height: 1.5;
}
</style>
