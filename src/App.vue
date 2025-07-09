<template>
  <div class="min-vh-100 bg-dark text-white align-items-center justify-content-center">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-4">
      <div class="container-fluid">
        <a class="navbar-brand d-flex align-items-center" href="#">
          <img src="/pokeball.svg" style="max-width:32px" class="px-1" />
          PokéHelper
        </a>

        <div class="ms-auto d-flex align-items-center">
          <label class="me-2 mb-0 fw-semibold">Ruleset:</label>
          <select class="form-select form-select-sm bg-light text-dark" v-model="selectedRuleset">
            <option v-for="r in rulesets" :value="r">r</option>
          </select>
        </div>
      </div>
    </nav>

    <div class="container py-5">
      <div class="bg-secondary bg-opacity-75 rounded-4 shadow-lg p-5">

        <h1 class="text-center fw-bold mb-4 display-5">
         Escolha seus Pokémon
        </h1>

        <PokemonSelect :max-selection="MAX_SELECTION" v-model="selectedPokemon" />

        <div class="text-center mt-4">
          <button class="btn btn-light btn-lg px-4 py-2 fw-semibold" @click="recommend">
            <font-awesome-icon icon="wand-magic-sparkles" class="me-2 text-primary"></font-awesome-icon>
            Recomendar Pokémon
          </button>
        </div>

        <div v-if="loading" class="text-center mt-4">
          <div class="spinner-border text-light" role="status"></div>
          <div class="mt-2">
            <i class="fa-spin me-2"></i>Carregando recomendações...
          </div>
        </div>

        <div v-if="recommendations.length" class="mt-5">
          <h3 class="text-center mb-3">
            <font-awesome-icon icon="lightbulb" class="me-2 text-info"></font-awesome-icon>Recomendações
          </h3>
          <div class="d-flex flex-wrap justify-content-center gap-3">
            <PokemonCard v-for="p in recommendations" :key="p.name" :pokemon="p" />
          </div>
        </div>

        <AlertModal ref="alertModal" />
      </div>
    </div>
  </div>
</template>


<script>
import PokemonSelect from './components/PokemonSelect.vue';
import PokemonCard from './components/PokemonCard.vue';
import AlertModal from './components/AlertModal.vue';

export default {
  name: 'App',
  components: {
    PokemonSelect,
    PokemonCard,
    AlertModal,
  },
  data() {
    return {
      selectedPokemon: [],
      recommendations: [],
      rulesets: [],
      selectedRuleset: "gen9vgc2025regg-0",
      loading: false,
      MAX_SELECTION: 5,
    };
  },
  mounted(){
    this.getRulesets();
  },
  methods: {
    async recommend() {
      if (this.selectedPokemon.length === 0) {
        this.$refs.alertModal.show('Selecione pelo menos 1 Pokémon antes de continuar.');
        return;
      }

      this.loading = true;
      try {
        const response = await fetch('http://localhost:8000/recommend', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ selected_pokemon: this.selectedPokemon.flatMap(x => x.label), ruleset: this.selectedRuleset }),
        });

        if (!response.ok) {
          throw new Error(`Erro do servidor: ${response.status}`);
        }

        const data = await response.json();
        this.recommendations = data;
      } catch (error) {
        this.sendError(error);
      } finally {
        this.loading = false;
      }
    },
    async getRulesets() {
      this.loading = true;
      try {
        const response = await fetch('http://localhost:8000/rulesets');

        if (!response.ok) {
          throw new Error(`Erro do servidor: ${response.status}`);
        }

        const data = await response.json();
        if(data == null || data.length == 0)
          data = ['gen9vgc2025regg-0'];
        this.selectedRuleset = data[0];
        this.rulesets = data;
      } catch (error) {
        this.sendError(error);
      } finally {
        this.loading = false;
      }
    },
    sendError(error) {
      this.$refs.alertModal.show(
        `Erro de conexão com o servidor. Verifique se a API está rodando corretamente.<br><br><code>${error.message}</code>`
      );
    },
  },
};
</script>