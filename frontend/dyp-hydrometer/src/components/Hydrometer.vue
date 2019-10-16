<template>
  <v-container fluid>
    <v-sparkline
        :value="sg"
        :labels="labels"
        color="rgba(0, 0, 0, .7)"
        height="50"
        padding="7"
        line-width="1"
        stroke-linecap="round"
        label-size="3"
        show-labels
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
            { text: 'RSSI', value: 'rssi' },
        ],
    }),
    methods: {
        getHydrometer(id) {
            const path = `http://localhost:5000/api/hydrometers/${id}`;
            axios.get(path)
                .then((res) => {
                    this.data = res.data["data"];
                    this.hydrometer = res.data["hydrometer"]
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