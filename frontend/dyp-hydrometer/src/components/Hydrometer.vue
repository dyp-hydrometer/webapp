<template>
  <v-container fluid>
    <v-card-text>
        <div class="display-1 font-weight-thin">Specific Gravity Trend</div>
    </v-card-text>
    <v-sparkline
        :value="sg"
        color="#00ACC1"
        height="50"
        padding="7"
        line-width="1"
        stroke-linecap="round"
        label-size="3"
        smooth
        light
    />

    <v-card-text>
        <div class="display-1 font-weight-thin">Temperature Trend</div>
    </v-card-text>
    <v-sparkline
        :value="temperatures"
        color="#FFA726"
        height="50"
        padding="7"
        line-width="1"
        stroke-linecap="round"
        label-size="3"
        smooth
        light
    />

    <v-data-table
        :headers="headers"
        :items="data"
        :items-per-page="10"
        class="elevation-1">
    </v-data-table>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
    data: () => ({
        hydrometer: null,
        data: [],
        temperatures: [],
        sg: [],
        labels: [],
        headers: [
            {
                text: 'Entry Time',
                align: 'left',
                sortable: true,
                value: 'time',
            },
            { text: 'Specific Gravity', value: 'specific_gravity' },
            { text: 'Temperature', value: 'temp' },
        ],
    }),
    methods: {
        getHydrometer(id) {
            const path = `http://${process.env.VUE_APP_API_URL}/hydrometers/${id}`;
            axios.get(path)
                .then((res) => {
                    this.data = res.data["data"];
                    this.hydrometer = res.data["hydrometer"];
                    this.parseData();
                })
                .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
                });
        },
        watch: {
            // call again the method if the route changes
            '$route': 'getHydrometer'
        },
        parseData() {
            this.temperatures = this.data.map(function(x) { return x["temp"]});
            this.sg = this.data.map(function(x) { return x["specific_gravity"]});
            this.labels = this.data.map(function(x) { return x["time"]});
        }
    },
    created() {
        this.getHydrometer(parseInt(this.$route.params.id));
    },
}
</script>