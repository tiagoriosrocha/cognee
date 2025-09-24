<template>
  <v-app>
    <!-- Menu Superior (App-Bar) -->
    <v-app-bar :elevation="10" rounded>
      <template v-slot:prepend>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>MorehopeQA</v-app-bar-title>

      <template v-slot:append>
        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>

    <!-- Conteúdo Principal -->
    <v-main>
      <v-container>
        <!-- Linha 1: Coluna Única com Texto Centralizado -->
        <v-row class="mt-4">
          <v-col class="text-center">
            <h1 class="text-h4 font-weight-bold">MorehopeQA - Cognee</h1>
            <p class="text-subtitle-1 mt-2">
              This notebook loads the MoreHopQA dataset and presents some
              exploratory visualizations using Altair. The dataset contains
              complex questions that require multiple reasoning steps. Columns
              record everything from the original question and its answer to the
              decomposition into subquestions, the supporting paragraphs used,
              and metadata about reasoning type, decomposition patterns, and
              simplifications of the question.
            </p>
          </v-col>
        </v-row>

        <!-- Divisor Visual -->
        <v-divider class="my-6"></v-divider>

        <!-- Linha 2: Duas Colunas -->
        <v-row>
          <v-col cols="12" md="8">
            <v-card class="pa-4 min-h-400" outlined>
              <v-card-title>Graph Visualization</v-card-title>
              <v-card-text
                >Conteúdo da primeira coluna. Aqui você pode colocar texto,
                imagens ou outros componentes.</v-card-text
              >
            </v-card>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="pa-4" outlined>
              <v-card-title>Properties</v-card-title>
              <v-card-text
                >Conteúdo da terceira coluna. O Vuetify é totalmente responsivo
                por padrão.</v-card-text
              >
            </v-card>
          </v-col>
        </v-row>

        <v-row class="mb-4">
          <v-col cols="12">
            <h2 class="text-h4 font-weight-bold text-center">
              Dataset Details
            </h2>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>
                <h3 class="text-h6 font-weight-bold">
                  Example of a dataset record:
                </h3>
              </v-card-title>
              <v-card-text>
                <ul class="list-none">
                  <li><strong>_id</strong>: 5ae5072e55429960a22e0246_13</li>
                  <li>
                    <strong>question</strong>: How many repeated letters are
                    there in the first name of the current drummer of the band
                    who did the song "What Lovers Do"?
                  </li>
                  <li><strong>answer</strong>: 1</li>
                  <li>
                    <strong>previous_question</strong>: Who is the current
                    drummer of the band who did the song "What Lovers Do"?
                  </li>
                  <li><strong>previous_answer</strong>: Matt Flynn</li>
                  <li>
                    <strong>question_decomposition</strong>: [{'sub_id': '1',
                    'question': 'Which band did the song "What Lovers Do"?',
                    'answer': 'Maroon 5', 'paragraph_support_title': 'What
                    Lovers Do'}, {'sub_id': '2', 'question': 'Who is the current
                    drummer of Maroon 5?', 'answer': 'Matt Flynn',
                    'paragraph_support_title': 'Maroon 5'}, {'sub_id': '3',
                    'question': 'How many repeated letters are there in the
                    first name of Matt Flynn?', 'answer': '1',
                    'paragraph_support_title': '', 'details': [{'sub_id': '3_1',
                    'question': 'What is the first name of Matt Flynn?',
                    'answer': 'Matt', 'paragraph_support_title': ''}, {'sub_id':
                    '3_2', 'question': 'How many repeated letters are there in
                    Matt?', 'answer': '1', 'paragraph_support_title': ''}]}]
                  </li>
                  <li>
                    <strong>context</strong>: [['Maroon 5', ['Maroon 5 is an
                    American pop rock band that originated in Los Angeles,
                    California.', ' It currently consists of lead vocalist Adam
                    Levine, keyboardist and rhythm guitarist Jesse Carmichael,
                    bassist Mickey Madden, lead guitarist James Valentine,
                    drummer Matt Flynn and keyboardist PJ Morton.']], ['What
                    Lovers Do', ['"What Lovers Do" is a song by American pop
                    rock band Maroon 5 featuring American R&B singer Sza.', " It
                    was released on August 30, 2017, as the third single from
                    the band's upcoming sixth studio album (2017).", ' The song
                    contains an interpolation of the 2016 song "Sexual" by
                    Neiked featuring Dyo, therefore Victor Rådström, Dyo and
                    Elina Stridh are credited as songwriters.']]]
                  </li>
                  <li><strong>answer_type</strong>: number</li>
                  <li><strong>previous_answer_type</strong>: person</li>
                  <li><strong>no_of_hops</strong>: 2</li>
                  <li>
                    <strong>reasoning_type</strong>: Commonsense, Arithmetic
                  </li>
                  <li>
                    <strong>pattern</strong>: How many repeated letters are
                    there in the first name of #Name?
                  </li>
                  <li>
                    <strong>subquestion_patterns</strong>: ['What is the first
                    name of #Name?', 'How many repeated letters are there in
                    #Ans1?']
                  </li>
                  <li>
                    <strong>cutted_question</strong>: the current drummer of the
                    band who did the song "What Lovers Do"
                  </li>
                  <li>
                    <strong>ques_on_last_hop</strong>: How many repeated letters
                    are there in the first name of the current drummer of Maroon
                    5?
                  </li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card class="pa-4" outlined>
              <v-card-title>
                <h3 class="text-h6 font-weight-bold">
                  Summary of MoreHopQA columns
                </h3>
              </v-card-title>
              <v-card-text>
                <ul>
                  <li>
                    <strong>question</strong> → Original question in the
                    dataset.
                  </li>
                  <li>
                    <strong>answer</strong> → Expected final answer for the
                    question.
                  </li>
                  <li>
                    <strong>answer_type</strong> → Type of the answer (e.g.,
                    entity, number, yes/no).
                  </li>
                  <li>
                    <strong>reasoning_type</strong> → Type of reasoning required
                    (e.g., <em>Symbolic, Arithmetic, Commonsense</em>).
                  </li>
                  <li>
                    <strong>decomp_len</strong> → Number of hops (subquestions)
                    used in the question decomposition.
                  </li>
                  <li>
                    <strong>question_decomposition</strong> → List of
                    subquestions/hops, each with supporting information and
                    links.
                  </li>
                  <li>
                    <strong>paragraph_support_title</strong>
                    <em>(inside decomposition)</em> → Paragraph(s) used to
                    answer that subquestion.
                  </li>
                  <li>
                    <strong>pattern</strong> → Global logical structure of the
                    question (e.g.,
                    <em>sequential, intersection, comparison</em>).
                  </li>
                  <li>
                    <strong>subquestion_pattern</strong> → Logical structure of
                    each subquestion in the decomposition (e.g.,
                    <em>lookup, bridge</em>).
                  </li>
                  <li>
                    <strong>cutted_question</strong> → Simplified/reduced
                    version of the original question.
                  </li>
                  <li>
                    <strong>ques_on_last_hop</strong> → Flag indicating if the
                    final answer depends only on the last hop.
                  </li>
                  <li>
                    <strong>id</strong> → Unique identifier of the question in
                    the dataset.
                  </li>
                  <li>
                    <strong>supporting_facts</strong> → List of facts (titles
                    and sentences) justifying the answer.
                  </li>
                  <li>
                    <strong>num_paragraphs</strong> <em>(derived)</em> → Number
                    of supporting paragraphs (created during preprocessing).
                  </li>
                </ul>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Rodapé -->
    <v-footer app color="blue-grey-darken-4" dark>
      <v-container>
        <v-row>
          <v-col class="text-center" cols="12">
            <span class="text-body-2">&copy; 2025 MorehopeQA - Cognee</span>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "VuetifyLayout",
};
</script>

<style scoped>
.min-h-300 {
  min-height: 300px;
}

.min-h-400 {
  min-height: 400px;
}

.list-none {
  list-style: none;
}
</style>
