<template>
  <div>
    <multiselect
      v-model="internalValue"
      :options="pokemonOptions"
      :multiple="true"
      :max="maxSelection"
      track-by="value"
      label="label"
      placeholder="Selecione os Pokémon"
      @input="onInput"
      :custom-label="customLabel"
      :show-labels="false"
      :close-on-select="false"
      :clear-on-select="false"
      :preserve-search="true"
      :preselect-first="false"
      :loading="loading"
      :searchable="true"
    >
      <template #option="{ option }">
        <div class="d-flex align-items-center">
          <img :src="option.img" :alt="option.label" width="24" class="me-2" />
          {{ option.label }}
        </div>
      </template>

      <template #tag="{ option, remove }">
        <span class="multiselect__tag d-flex align-items-center">
          <img :src="option.img" :alt="option.label" width="20" class="me-1" />
          {{ option.label }}
          <i class="multiselect__tag-icon" @click="remove(option)"/>
        </span>
      </template>
    </multiselect>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect';

export default {
  components: { Multiselect },
  props: {
    modelValue: {
      type: Array,
      default: () => [],
    },
    maxSelection: {
      type: Number,
      default: 5,
    },
  },
  data() {
    return {
      pokemonOptions: [],
      internalValue: this.modelValue,
      loading: false,
    };
  },
  watch: {
    modelValue(newVal) {
      this.internalValue = newVal;
    },
    internalValue(newVal) {
      this.$emit('update:modelValue', newVal);
    },
  },
  mounted() {
    this.loadPokemonOptions();
  },
  methods: {
    async loadPokemonOptions() {
      this.loading = true;
      try {
        const res = await fetch('https://pokeapi.co/api/v2/pokemon?limit=151');
        const data = await res.json();
        this.pokemonOptions = data.results.map((p, idx) => ({
          value: p.name,
          label: p.name.charAt(0).toUpperCase() + p.name.slice(1),
          img: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${idx + 1}.png`,
        }));
      } catch (error) {
        console.error('Erro ao carregar Pokémon:', error);
      } finally {
        this.loading = false;
      }
    },
    customLabel(option) {
      return `${option.label}`;
    },
    onInput(value) {
      this.internalValue = value;
    },
  },
};
</script>

<style scoped>
.multiselect__tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.multiselect__tag img {
  width: 20px;
  height: 20px;
}
.multiselect__option img {
  width: 24px;
  height: 24px;
  margin-right: 8px;
}
</style>