<template>
  <v-container fluid>
    <v-container fluid style="height: 400px">
        <line-chart v-if="data.loaded" :chart-data="datacollection" style="width:100%;height:100%;"></line-chart>
    </v-container>
    <!--<line-chart :chart-data="datacollection"></line-chart>-->


    <v-data-table
        :headers="headers"
        :items="data"
        :items-per-page="10"
        class="elevation-1">
    </v-data-table>
  </v-container>
</template>

<script>
import LineChart from './LineChart.js'
import axios from 'axios';

export default {
    components: {
      LineChart
    },
    data: () => ({
        hydrometer: null,
        data: [],
        temperatures: [],
        sg: [],
        labels: [],
        datacollection: { labels: [], datasets: []},
        options: {responsive: true, maintainAspectRatio: false},
        loaded : false,
        //temperatures: [78.3, 77.2, 78, 77.5, 77.3, 77.4],
        //sg: [1.17, 1.171, 1.169, 1.17, 1.172, 1.170],
        //labels: ["2019-10-16 03:17:24", "2019-10-16 03:17:29", "2019-10-16 03:17:34", "2019-10-16 03:17:39", "2019-10-16 03:17:44", "2019-10-16 03:17:49"],
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
            this.datacollection.labels = this.data.map(function(x) { return x["time"]});
            this.datacollection.datasets = [
                {
                    label: 'Specific Gravity',
                    backgroundColor: '#f893a5',
                    borderColor: '#f893a5',
                    data: this.data.map(function(x) { return x["specific_gravity"]}),
                    fill: false,
                    responsive: true
                },
            ];
            this.data.loaded = true;
            this.renderChart(this.datacollection, this.options)
        }
    },
    created() {
        this.getHydrometer(parseInt(this.$route.params.id));
    },
    mounted () {
        this.renderChart(this.datacollection, this.options)
    }
}
</script>

<style>
  .small {
    margin:  100px auto;
  }
</style>