<template>
    <v-data-iterator
      :items="items"
      :items-per-page.sync="itemsPerPage"
      :footer-props="{ itemsPerPageOptions }"
    >
      <template v-slot:default="props">
        <v-row>
          <v-col
            v-for="hydrometer in props.items"
            :key="hydrometer.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card>
              <v-card-title><h4>{{ hydrometer.id }}</h4></v-card-title>
              <v-divider></v-divider>
              <v-list dense>
                <v-list-item>
                  <v-list-item-content>Color:</v-list-item-content>
                  <v-list-item-content class="align-end">{{ hydrometer.color }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>Created At:</v-list-item-content>
                  <v-list-item-content class="align-end">{{ hydrometer.created_at }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>Active:</v-list-item-content>
                  <v-list-item-content class="align-end">{{ hydrometer.active ? "Yes" : "No" }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>Battery:</v-list-item-content>
                  <v-list-item-content class="align-end">{{ hydrometer.battery }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>Interval:</v-list-item-content>
                  <v-list-item-content class="align-end">{{ hydrometer.interval }}</v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>Profile:</v-list-item-content>
                  <v-list-item-content class="align-end">{{ hydrometer.profile }}</v-list-item-content>
                </v-list-item>
              </v-list>
              <v-divider></v-divider>
              <v-btn
                :to="`hydrometers/${hydrometer.id}`"
                class="ma-2"
                href=""
                :loading="loading"
                :disabled="loading"
                color="secondary"
                @click="loader = 'loading'"
              >
                View Data
              </v-btn>
              <v-btn
                class="ma-2"
                :loading="loading"
                :disabled="loading"
                outlined 
                color="success"
                @click="loader = 'loading'"
              >
                <v-icon left>mdi-pencil</v-icon> Edit
              </v-btn>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
      itemsPerPageOptions: [4, 8, 12],
      itemsPerPage: 4,
      items: [],
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        color: '',
        active: '',
        profile: '',
      },
  }),
  methods: {
    getHydrometers() {
      const path = 'http://localhost:5000/api/hydrometers/';
      axios.get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editHydrometer(Hydrometer) {
      this.editForm = Hydrometer;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editHydrometerModal.hide();
      let active = true;
      if (!this.editForm.active[0]) active = false;
      const payload = {
        color: this.editForm.color,
        profile: this.editForm.profile,
        active,
      };
      this.updateHydrometer(payload, this.editForm.id);
    },
    updateHydrometer(payload, HydrometerID) {
      const path = `http://localhost:5000/api/hydrometers/${HydrometerID}`;
      axios.put(path, payload)
        .then(() => {
          this.getHydrometers();
          this.message = 'Hydrometer successfully updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getHydrometers();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editHydrometerModal.hide();
      this.initForm();
      this.getHydrometers();
    },
  },
  created() {
    this.getHydrometers();
  },
};
</script>