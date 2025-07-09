<template>
  <div class="card bg-secondary text-white p-3" style="width: 18rem;">
    <h5 class="card-title text-center">{{ capitalizedName }}</h5>
    <img :src="spriteUrl" class="card-img-top mx-auto" style="width: 96px;" :alt="pokemon.name" />
    <div class="text-center my-2">
      <span class="badge me-1 text-white" v-for="type in types" :key="type"
        :style="{ backgroundColor: getTypeColor(type) }">
        {{ capitalize(type) }}
      </span>
    </div>
    <div class="card-body">
      <div v-for="stat in stats" :key="stat.name">
        <div class="mb-1"><strong>{{ capitalize(stat.name) }}:</strong> {{ stat.value }}</div>
        <div class="progress mb-2" style="height: 8px;">
          <div class="progress-bar" :class="getStatColor(stat.value)" :style="{ width: stat.percent + '%' }"></div>
        </div>
      </div>

      <div class="text-center mb-3">
        <h6 class="mb-0">Habilidade</h6>
        <span class="badge bg-light text-dark px-2 py-1 fs-6">
          {{ capitalize(pokemon.ability) }}
        </span>
      </div>

      <div class="text-center mb-3">
        <h6 class="mb-0">Item</h6>
        <span class="badge bg-light text-dark px-2 py-1 fs-6">
          {{ capitalize(pokemon.item) }}
        </span>
      </div>

      <div class="text-center mb-3">
        <h6 class="mb-0">Tipo Tera</h6>
        <span class="badge text-white px-2 py-1 fs-6"
          :style="{ backgroundColor: getTypeColor(pokemon.teraType.toLowerCase()) }">
          {{ capitalize(pokemon.teraType) }}
        </span>
      </div>

      <div class="mt-3">
        <h6 class="text-center">Movimentos</h6>
        <ul class="list-group list-group-flush">
          <li v-for="(move, index) in pokemon.moves" :key="index" class="list-group-item bg-secondary text-white p-1">
            {{ capitalize(move) }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    pokemon: Object,
  },
  data() {
    return {
      spriteUrl: '',
      types: [],
      stats: [],
    };
  },
  computed: {
    capitalizedName() {
      return this.capitalize(this.pokemon.name);
    },
  },
  async mounted() {
    const response = await fetch(`https://pokeapi.co/api/v2/pokemon/${this.pokemon.name}`);
    const data = await response.json();

    this.spriteUrl = data.sprites.front_default;
    this.types = data.types.map((t) => t.type.name);
    this.stats = data.stats.map((s) => {
      const value = s.base_stat;
      return {
        name: s.stat.name.replace('-', ' '),
        value,
        percent: Math.min((value / 200) * 100, 100),
      };
    });
  },
  methods: {
    getTypeColor(type) {
      const typeColors = {
        normal: '#A8A77A', fire: '#EE8130', water: '#6390F0',
        electric: '#F7D02C', grass: '#7AC74C', ice: '#96D9D6',
        fighting: '#C22E28', poison: '#A33EA1', ground: '#E2BF65',
        flying: '#A98FF3', psychic: '#F95587', bug: '#A6B91A',
        rock: '#B6A136', ghost: '#735797', dragon: '#6F35FC',
        dark: '#705746', steel: '#B7B7CE', fairy: '#D685AD',
      };
      return typeColors[type] || '#777';
    },
    getStatColor(stat) {
      if (stat >= 130) return 'bg-primary';
      if (stat >= 90) return 'bg-warning';
      return 'bg-danger';
    },
    capitalize(str) {
      return str?.charAt(0)?.toUpperCase() + str?.slice(1);
    },
  },
};
</script>