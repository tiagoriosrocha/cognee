<template>
  <v-app>
    <v-app-bar :elevation="10">
      <template v-slot:prepend>
        <v-icon icon="mdi-menu"></v-icon>
      </template>
      <v-app-bar-title>Cognee - MorehopeQA</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn icon="mdi-magnify"></v-btn>
      <v-btn icon="mdi-dots-vertical"></v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid class="pa-6">
        <v-row class="mb-4">
          <v-col cols="12">
            <h1 class="text-h4 font-weight-bold text-center">
              Dashboard de Análise
            </h1>
          </v-col>
        </v-row>

        <v-divider class="my-6"></v-divider>

        <!-- Tabela de Perguntas -->
        <v-row class="mb-6">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title class="text-h6 font-weight-medium">
                Selecione uma Pergunta
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :items="dataset"
                  :headers="tableHeaders"
                  item-value="_id"
                  @click:row="selectItem"
                  class="elevation-1"
                  :row-props="rowProps"
                ></v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Detalhes do Item Selecionado -->
        <v-row v-if="selectedItem" class="mb-6">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title class="text-h6 font-weight-medium">
                Detalhes do Item
              </v-card-title>
              <v-card-text>
                <v-list dense>
                  <v-list-item>
                    <v-list-item-title><strong>ID:</strong></v-list-item-title>
                    <v-list-item-subtitle class="wrap-text">{{
                      selectedItem._id
                    }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title
                      ><strong>Pergunta:</strong></v-list-item-title
                    >
                    <v-list-item-subtitle class="wrap-text">{{
                      selectedItem.question
                    }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title
                      ><strong>Resposta Esperada:</strong></v-list-item-title
                    >
                    <v-list-item-subtitle class="wrap-text">{{
                      selectedItem.answer
                    }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title
                      ><strong>Hops (Subperguntas):</strong></v-list-item-title
                    >
                    <v-list-item-subtitle class="wrap-text">{{
                      selectedItem.no_of_hops
                    }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title
                      ><strong>Tipo de Raciocínio:</strong></v-list-item-title
                    >
                    <v-list-item-subtitle class="wrap-text">{{
                      selectedItem.reasoning_type
                    }}</v-list-item-subtitle>
                  </v-list-item>

                  <!-- Texto de Contexto -->
                  <v-list-item>
                    <v-list-item-title
                      ><strong>Texto de Contexto:</strong></v-list-item-title
                    >
                    <div class="context-wrapper">
                      <ul class="context-list">
                        <li
                          v-for="(context, index) in contextText"
                          :key="index"
                        >
                          <strong>{{ context.title }}:</strong>
                          <span class="context-text">{{ context.text }}</span>
                        </li>
                      </ul>
                    </div>
                  </v-list-item>

                  <!-- Sub-perguntas -->
                  <v-list-item>
                    <v-list-item-title
                      ><strong>Sub-Perguntas:</strong></v-list-item-title
                    >
                    <div class="subquestions-wrapper">
                      <ul class="subquestions-list">
                        <li v-for="sub in subQuestions" :key="sub.sub_id">
                          <strong>{{ sub.sub_id }}:</strong> {{ sub.question }}
                          <em>(Resposta: {{ sub.answer }})</em>
                          <span v-if="sub.paragraph_support_title">
                            — Contexto: {{ sub.paragraph_support_title }}</span
                          >
                        </li>
                      </ul>
                    </div>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Mensagem caso nenhum item seja selecionado -->
        <v-row v-else class="mb-6">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-text
                class="text-center text-subtitle-1 text-medium-emphasis"
              >
                Clique em uma linha da tabela para ver os detalhes.
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-divider class="my-6"></v-divider>

        <v-row class="mb-4">
          <v-col cols="12">
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
          </v-col>
        </v-row>

        <v-row v-if="processedAnswer" class="mb-6">
          <v-col cols="12">
            <v-card class="pa-4" outlined>
              <v-card-title class="text-h6 font-weight-medium">
                Resultado do Processamento
              </v-card-title>
              <v-card-text>
                <v-list dense>
                  <v-list-item>
                    <v-list-item-title
                      ><strong>Resposta Processada:</strong></v-list-item-title
                    >
                    <v-list-item-subtitle class="wrap-text">
                      {{ processedAnswer }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-divider v-if="processedAnswer" class="my-6"></v-divider>

        <v-row v-if="processedAnswer">
          <v-col cols="12" md="8">
            <v-card class="pa-4 min-h-600" outlined>
              <v-card-title class="text-h6 font-weight-medium">
                Grafo do Processamento Cognee
              </v-card-title>
              <v-card-text
                class="d-flex align-center justify-center fill-height"
              >
                <p class="text-medium-emphasis">
                  [Gráfico Graphly será exibido aqui]
                </p>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="pa-4 min-h-600" outlined>
              <v-card-title class="text-h6 font-weight-medium">
                Detalhes do Nodo
              </v-card-title>
              <v-card-text>
                <p class="text-medium-emphasis">
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
                      <th class="text-left">Propriedade</th>
                      <th class="text-left">Tipo</th>
                      <th class="text-left">Origem</th>
                      <th class="text-left">Descrição</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colspan="4" class="text-center text-medium-emphasis">
                        Tabela de propriedades será exibida aqui.
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-snackbar
      v-model="snackbar"
      :timeout="3000"
      :color="snackbarColor"
      location="bottom"
    >
      {{ snackbarMessage }}
    </v-snackbar>

    <v-footer app color="blue-grey-darken-4" dark>
      <v-container>
        <v-row>
          <v-col class="text-center" cols="12">
            <span class="text-body-2">&copy; 2025 Cognee</span>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
import dataset from "./dataset.json";

export default {
  name: "CogneeDashboard",
  data() {
    return {
      dataset,
      selectedItem: null,
      tableHeaders: [
        { title: "ID", align: "start", sortable: false, key: "_id" },
        { title: "Pergunta", align: "start", key: "question" },
        { title: "Hops", align: "end", key: "no_of_hops" },
        { title: "Tipo de Raciocínio", align: "start", key: "reasoning_type" },
      ],
      processingOptions: [
        { text: "Main question", value: 1 },
        { text: "Sequence questions", value: 2 },
        { text: "Main question with ontology", value: 3 },
        { text: "Sequence questions with ontology", value: 4 },
      ],
      processingTypes: [
        "Main question with ontology",
        "Sequence questions with ontology",
      ],
      selectedProcessingType: null,
      modelSelection: null,
      processing: false,
      snackbar: false,
      snackbarMessage: "",
      snackbarColor: "",
      processedAnswer: null,
      processedGraph: null,
    };
  },
  computed: {
    contextText() {
      if (!this.selectedItem || !this.selectedItem.context) return [];
      return this.selectedItem.context.map(([title, paragraphs]) => ({
        title,
        text: paragraphs.join(" "),
      }));
    },
    subQuestions() {
      if (!this.selectedItem || !this.selectedItem.question_decomposition)
        return [];

      const flattenSubQuestions = (subs) => {
        return subs.flatMap((sub) => {
          let result = [
            {
              sub_id: sub.sub_id,
              question: sub.question,
              answer: sub.answer,
              paragraph_support_title: sub.paragraph_support_title || "",
            },
          ];
          if (sub.details && sub.details.length) {
            result = result.concat(flattenSubQuestions(sub.details));
          }
          return result;
        });
      };

      return flattenSubQuestions(this.selectedItem.question_decomposition);
    },
  },
  mounted() {
    if (this.processingOptions.length > 0) {
      this.selectedProcessingType = this.processingOptions[0];
    }
  },
  methods: {
    selectItem(event, { item }) {
      this.selectedItem = item.raw || item || null;
      console.log("Item selecionado:", this.selectedItem);
    },
    rowProps({ item }) {
      const isMatch = this.selectedItem && this.selectedItem._id === item._id;
      return { class: isMatch ? "selected-row" : "" };
    },
    async processar() {
      if (!this.selectedItem || this.selectedProcessingType === null) {
        this.showSnackbar(
          "Por favor, selecione uma pergunta e um tipo de processamento.",
          "error"
        );
        return;
      }

      this.processing = true;

      const payload = {
        selectedQuestion: this.selectedItem,
        processingType: this.selectedProcessingType,
      };

      try {
        const response = await fetch("http://localhost:5000/processarquery", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`Erro na requisição: ${response.statusText}`);
        }

        const data = await response.json();

        this.processedAnswer = data.answer;
        this.processedGraph = data.graph;

        this.showSnackbar("Requisição concluída com sucesso!", "success");
        console.log("Resposta da API:", data);
      } catch (error) {
        this.showSnackbar("Ocorreu um erro no processamento.", "error");
        console.error("Erro na requisição:", error);
      } finally {
        this.processing = false;
      }
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

.context-wrapper {
  white-space: normal;
  overflow: visible;
  margin-top: 8px;
}

.context-list {
  list-style-type: none;
  padding-left: 0;
}

.context-list li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.context-text {
  display: block;
  white-space: normal;
  overflow: visible;
  text-overflow: unset;
  line-height: 1.5;
}

.subquestions-wrapper {
  white-space: normal;
  overflow: visible;
  margin-top: 8px;
}

.subquestions-list {
  list-style-type: none;
  padding-left: 0;
}

.subquestions-list li {
  margin-bottom: 6px;
  line-height: 1.5;
}

/* Estilo para a linha selecionada */
.v-data-table .v-data-table__tbody tr.selected-row {
  background-color: #07f04d !important;
  font-weight: bold !important;
  color: black !important;
}
</style>
