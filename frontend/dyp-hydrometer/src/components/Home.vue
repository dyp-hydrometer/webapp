<template>
<v-row justify="center">
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
            <v-list >
              <v-list-item>
                <v-list-item-content>Color:</v-list-item-content>
                <v-list-item-content class="align-end">{{ hydrometer.color }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Created At:</v-list-item-content>
                <v-list-item-content class="align-end">{{ hydrometer.created_at }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Brew Start:</v-list-item-content>
                <v-list-item-content class="align-end">{{ hydrometer.brew_start }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Brew in Progress:</v-list-item-content>
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
              <v-list-item v-if="hydrometer.profile !== null">
                <v-list-item-content>Profile:</v-list-item-content>
                <v-list-item-content class="align-end">{{ profiles[hydrometer.profile].text }}</v-list-item-content>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-btn
              :to="`hydrometers/${hydrometer.id}`"
              class="ma-2"
              color="secondary"
            >
              View
            </v-btn>
            <v-btn
              class="ma-2"
              outlined 
              color="success"
              @click.stop="$set(editForm, hydrometer.id, true);"
            >
              <v-icon left>mdi-pencil</v-icon> Edit
            </v-btn>
            <v-btn
              @click="new_brew(hydrometer.id)"
              class="ma-2"
              color="secondary"
            >
              New Brew
            </v-btn>
          </v-card>

          <v-dialog v-model="editForm[hydrometer.id]" persistent max-width="600px" :key="hydrometer.id">
            <!-- <template v-slot:activator="{ on }">
              <v-btn color="primary" dark v-on="on">Open Dialog</v-btn>
            </template> -->
            <v-card>
              <v-card-title>
                <span class="headline">{{ hydrometer.id }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field label="Color" v-model="items[hydrometer.id-1].color" :value="hydrometer.color" required></v-text-field>
                    </v-col>
                    <!--<v-col cols="12" sm="6" md="4">
                      <v-text-field label="Interval" :value="hydrometer.interval"  v-model="items[hydrometer.id-1].interval" required></v-text-field>
                    </v-col>-->
                    <v-col cols="12" sm="6" md="4">
                      <v-select :items="profiles" label="Profiles" v-model="items[hydrometer.id-1].profile" :value="hydrometer.profile"></v-select>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-switch :active="hydrometer.active" v-model="items[hydrometer.id-1].active" class="ma-2" label="Brew in Progress"></v-switch>
                  </v-row>
                  <v-row>
                    <v-time-picker
                      v-model="items[hydrometer.id-1].interval"
                      :value="hydrometer.interval"
                      class="mt-2"
                      use-seconds="true"
                      format="24hr"
                    ></v-time-picker>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click.stop="$set(editForm, hydrometer.id, false)">Close</v-btn>
                <v-btn color="blue darken-1" text @click="editHydrometer(hydrometer.id)">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>
    </template>
  </v-data-iterator>
</v-row>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
      itemsPerPageOptions: [4, 8, 12],
      itemsPerPage: 4,
      items: [],
      profiles: [{text: "None", value: null}],
      message: '',
      showMessage: false,
      editForm: {},
  }),
  methods: {
    getHydrometers() {
      const path = `http://${process.env.VUE_APP_API_URL}/hydrometers/`;
      axios.get(path)
        .then((res) => {
          res.data.forEach(function(hydrometer){
            if (hydrometer.profile === null) {
              hydrometer.profile = 1
            }
          })
          this.items = res.data;
          // eslint-disable-next-line
          console.log(this.items);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getProfiles() {
      const path = `http://${process.env.VUE_APP_API_URL}/profiles/`;
      axios.get(path)
        .then((res) => {
          res.data.map((profile)=>{
            this.profiles.push({text: profile.name, value: profile.id});
          });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editHydrometer(id) {
      const payload = {
        color: this.items[id-1].color,
        interval: this.items[id-1].interval,
        profile: this.items[id-1].profile,
        active: this.items[id-1].active,
      };
      // eslint-disable-next-line
      console.log(payload);
      this.updateHydrometer(payload, id);
      this.editForm[id] = false;
    },
    updateHydrometer(payload, HydrometerID) {
      //
      //const path = `http://localhost:5000/api/hydrometers/${HydrometerID}`;
      const path = `http://${process.env.VUE_APP_API_URL}/hydrometers/${HydrometerID}/`;
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
    new_brew(id)
    {
      //
      //const path = `http://localhost:5000/api/hydrometers/${HydrometerID}`;
      const payload = {}
      const path = `http://${process.env.VUE_APP_API_URL}/hydrometers/${id}/brew_start`;
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
    }
  },
  created() {
    this.getHydrometers();
    this.getProfiles();
  },
};
</script>