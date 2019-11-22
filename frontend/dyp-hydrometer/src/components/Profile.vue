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
          v-for="profile in props.items"
          :key="profile.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card>
            <v-card-title><h4>{{ profile.id }}</h4></v-card-title>
            <v-divider></v-divider>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>Name:</v-list-item-content>
                <v-list-item-content class="align-end">{{ profile.name }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Description:</v-list-item-content>
                <v-list-item-content class="align-end">{{ profile.description }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Duration:</v-list-item-content>
                <v-list-item-content class="align-end">{{ profile.duration }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Required Gravity:</v-list-item-content>
                <v-list-item-content class="align-end">{{ profile.req_gravity }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Required Temperature:</v-list-item-content>
                <v-list-item-content class="align-end">{{ profile.req_temp }}</v-list-item-content>
              </v-list-item>
            </v-list>
            <v-divider></v-divider>
            <v-btn
              class="ma-2"
              outlined 
              color="success"
              @click.stop="$set(editForm, profile.id, true);"
            >
              <v-icon left>mdi-pencil</v-icon> Edit
            </v-btn>
          </v-card>

          <v-dialog v-model="editForm[profile.id]" persistent max-width="600px" :key="profile.id">
            <!-- <template v-slot:activator="{ on }">
              <v-btn color="primary" dark v-on="on">Open Dialog</v-btn>
            </template> -->
            <v-card>
              <v-card-title>
                <span class="headline">{{ profile.id }}</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field label="Name" v-model="items[profile.id-1].name" :value="profile.name" required></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field label="Description" :value="items[profile.id-1].description"  v-model="profile.description" required></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field label="Duration" v-model="items[profile.id-1].duration" :value="profile.duration" required></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field label="SG" :value="profile.req_gravity"  v-model="items[profile.id-1].req_gravity" required></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field label="Temperature" v-model="items[profile.id-1].req_temp" :value="profile.req_temp" required></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click.stop="$set(editForm, profile.id, false)">Close</v-btn>
                <v-btn color="blue darken-1" text @click="editProfile(profile.id)">Save</v-btn>
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
      message: '',
      showMessage: false,
      editForm: {},
  }),
  methods: {
    getProfiles() {
      const path = `http://${process.env.VUE_APP_API_URL}/profiles/`;
      axios.get(path)
        .then((res) => {
          this.items = res.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    editProfile(id) {
      const payload = {
        description: this.items[id-1].description,
        duration: this.items[id-1].duration,
        name: this.items[id-1].name,
        req_gravity: this.items[id-1].req_gravity,
        req_temp: this.items[id-1].req_temp,
      };
      // eslint-disable-next-line
      console.log(payload);
      this.updateProfile(payload, id);
      this.editForm[id] = false;
    },
    updateProfile(payload, id) {
      //
      const path = `http://${process.env.VUE_APP_API_URL}/profiles/${id}/`;
      axios.put(path, payload)
        .then(() => {
          this.getProfiles();
          this.message = 'Profile successfully updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getProfiles();
        });
    },
  },
  created() {
    this.getProfiles();
  },
};
</script>