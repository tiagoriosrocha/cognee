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
    <v-col cols="12" md="8" v-if="selectedNode">
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

    <v-col cols="12" md="12" v-else>
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

    <v-col cols="12" md="4" v-if="selectedNode">
      <v-card class="pa-4 fill-height" outlined>
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
        <v-card-title class="text-h6 font-weight-medium d-flex align-center">
          Detalhes das Propriedades do Grafo
          <v-spacer></v-spacer>
          <!-- Botão de minimizar -->
          <v-btn icon @click="cardMinimized = !cardMinimized" size="small">
            <v-icon>
              {{
                cardMinimized
                  ? "fa-solid fa-chevron-down"
                  : "fa-solid fa-chevron-up"
              }}
            </v-icon>
          </v-btn>
        </v-card-title>

        <v-expand-transition>
          <v-card-text v-show="!cardMinimized">
            <v-table>
              <thead>
                <tr>
                  <th class="text-left">ID do Nó</th>
                  <th class="text-left">Nome do Nó</th>
                  <th class="text-left">Outras Propriedades</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(node, key) in graphData.nodes"
                  :key="node.id"
                  :class="{
                    'selected-row': selectedNode && selectedNode.id === node.id,
                  }"
                >
                  <td>{{ key }}</td>
                  <td>{{ node.name }}</td>
                  <td>
                    <div v-for="(value, prop) in node" :key="prop">
                      <span v-if="prop !== 'name' && prop !== 'id'">
                        <strong>{{ prop }}:</strong>
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
        </v-expand-transition>
      </v-card>
    </v-col>
  </v-row>

  <v-snackbar
    v-model="snackbar"
    :timeout="3000"
    :color="snackbarColor"
    location="bottom"
  >
    <div class="d-flex align-center w-100">
      <span>{{ snackbarMessage }}</span>
      <v-spacer></v-spacer>
      <v-icon color="white">fa-solid fa-check</v-icon>
    </div>
  </v-snackbar>

  <v-snackbar
    v-model="processingSnackbar"
    color="info"
    location="bottom"
    :timeout="-1"
  >
    Processando a requisição, por favor aguarde... ({{ elapsed }}s)
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
      cardMinimized: false,
      snackbar: false,
      snackbarMessage: "",
      snackbarColor: "",
      processingSnackbar: false,
      elapsed: 0,
      timer: null,
      pollingInterval: null,
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
    // async processar() {
    //   if (!this.selectedItem || this.selectedProcessingType === null) {
    //     this.showSnackbar(
    //       "Por favor, selecione uma pergunta e um tipo de processamento.",
    //       "error"
    //     );
    //     return;
    //   }

    //   //this.processing = true;
    //   this.processingSnackbar = true;

    //   const payload = {
    //     selectedQuestion: this.selectedItem,
    //     processingType: this.selectedProcessingType,
    //   };

    //   try {
    //     const response = await fetch("http://localhost:5000/runquestion", {
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: JSON.stringify(payload),
    //     });

    //     if (!response.ok) {
    //       throw new Error(`Erro na requisição: ${response.statusText}`);
    //     }

    //     const data = await response.json();

    //     this.processedAnswer = data.final_answer;
    //     this.graphData.nodes = data.nodes;
    //     this.graphData.edges = data.edges;

    //     this.showSnackbar("Requisição concluída com sucesso!", "success");
    //     console.log("Resposta da API:", data);
    //   } catch (error) {
    //     this.showSnackbar("Ocorreu um erro no processamento.", "error");
    //     console.error("Erro na requisição:", error);
    //   } finally {
    //     // this.processing = false;
    //     this.processingSnackbar = false;
    //   }
    // },
    async processar() {
      if (!this.selectedItem || this.selectedProcessingType === null) {
        this.showSnackbar(
          "Por favor, selecione uma pergunta e um tipo de processamento.",
          "error"
        );
        return;
      }

      // Garante que não haja um polling antigo rodando
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
      }

      this.showSnackbarProcessando();

      const payload = {
        selectedQuestion: this.selectedItem,
        processingType: this.selectedProcessingType,
      };

      try {
        // 1. FAZ A REQUISIÇÃO PARA INICIAR O PROCESSO
        const response = await fetch("http://localhost:5000/runquestion", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        // O backend deve responder com 202 (Accepted)
        if (response.status !== 202) {
          const errorData = await response.json();
          throw new Error(
            `Erro ao iniciar a tarefa: ${errorData.erro || response.statusText}`
          );
        }

        const { task_id } = await response.json();

        // 2. INICIA O POLLING PARA VERIFICAR O STATUS
        this.iniciarPolling(task_id);
      } catch (error) {
        this.showSnackbar(
          "Ocorreu um erro ao iniciar o processamento.",
          "error"
        );
        console.error("Erro na requisição inicial:", error);
        this.hideSnackbarProcessando();
      }
    },

    // NOVO MÉTODO PARA CONTROLAR O POLLING
    iniciarPolling(taskId) {
      // Verifica o status a cada 2 segundos (2000 ms).
      this.pollingInterval = setInterval(async () => {
        try {
          const response = await fetch(
            `http://localhost:5000/status/${taskId}`
          );

          if (!response.ok) {
            // Se houver um erro de rede ou 500 no endpoint de status, para o polling.
            throw new Error(`Erro ao verificar status: ${response.statusText}`);
          }

          const data = await response.json();

          // 3. VERIFICA O STATUS RETORNADO PELA API
          if (data.status === "SUCCESS") {
            this.finalizarPollingComSucesso(data.result);
          } else if (data.status === "FAILURE") {
            this.finalizarPollingComErro(data.result);
          }
          // Se for 'PENDING' ou 'PROCESSING', não faz nada e continua o loop.
        } catch (error) {
          // Se a verificação de status falhar (ex: rede caiu), para tudo.
          this.finalizarPollingComErro({ detalhes: error.message });
        }
      }, 5000);
    },

    // NOVO MÉTODO PARA QUANDO O POLLING TERMINA COM SUCESSO
    finalizarPollingComSucesso(resultado) {
      clearInterval(this.pollingInterval); // Para de verificar
      this.pollingInterval = null;

      // Atualiza os dados da sua aplicação com o resultado
      this.processedAnswer = resultado.final_answer;
      this.graphData.nodes = resultado.nodes;
      this.graphData.edges = resultado.edges;

      this.hideSnackbarProcessando();
      this.showSnackbar("Processamento concluído com sucesso!", "success");
      console.log("Resposta final da API:", resultado);
    },

    // NOVO MÉTODO PARA QUANDO O POLLING TERMINA COM ERRO
    finalizarPollingComErro(erro) {
      clearInterval(this.pollingInterval); // Para de verificar
      this.pollingInterval = null;

      this.hideSnackbarProcessando();
      this.showSnackbar(
        "Ocorreu um erro no processamento do servidor.",
        "error"
      );
      console.error("Erro retornado pelo backend:", erro.detalhes);
    },
    onNodeSelected(node) {
      if (!node) {
        this.selectedNode = null;
        return;
      }
      this.selectedNode = node;
      console.log("Node selecionado:", node.id);
    },
    showSnackbar(message, color) {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.snackbar = true;
    },
    showSnackbarProcessando() {
      this.processingSnackbar = true;
      this.elapsed = 0;

      this.timer = setInterval(() => {
        this.elapsed++;
      }, 1000);
      console.log("mostrar processando");
    },
    hideSnackbarProcessando() {
      this.processingSnackbar = false;
      clearInterval(this.timer);
      this.timer = null;
      console.log("esconder processando");
    },
  },
  beforeUnmount() {
    clearInterval(this.timer);
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
.selected-row {
  background-color: #e0e0e0; /* cinza claro */
}
</style>
