import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import Vue from 'vue';
import Vuetify from 'vuetify/lib';


Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi',
  },
  /*theme: {
    themes: {
      light: {
        primary: "#1E88E5", // #E53935
        secondary: "#00897B", // #FFCDD2
        accent: "#B9F6CA", // #3F51B5
      },
    },
  }*/
});
