<template>
    <div>
        <h1>CSV Application</h1>
        <hr>
        <button type="button" v-on:click="goHome">Go to Home</button>

        <div v-if="fileName != null">
            <h3>{{ fileName }}</h3>
            <h5>Page Number {{pageNumber}} </h5>
        </div>

        <table>
            <tr>
                <th scope="col">Year</th>
                <th scope="col">Count</th>
            </tr>
            <tbody>
            <tr v-for="(item, index) in csvYearStats" :key="index">
                <td>{{ index }}</td>
                <td>{{ item }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';
import router from '@/router';

const axiosInstance = axios.create({ baseURL: 'http://localhost:5000' });

export default {
  data() {
    const route = useRoute();
    return {
      csvYearStats: [],
      fileName: route.params.name,
    };
  },

  methods: {
    getFileStats() {
      const path = `/csv/stats/${this.fileName}`;
      axiosInstance.get(path)
        .then((res) => {
          this.csvYearStats = res.data.csvYearStats;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    goHome() {
      router.push({ name: 'CsvHome' });
    },
  },
  created() {
    this.getFileStats();
  },
};
</script>
