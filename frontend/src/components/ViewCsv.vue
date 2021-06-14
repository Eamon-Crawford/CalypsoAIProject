<template>
    <div class="container">
        <h1>CSV Application</h1>
        <hr>
        <button type="button" class="btn btn-success btn-sm"
        v-on:click="goHome">Go to Home</button>

        <div v-if="fileName != null">
            <h3>{{ fileName }}</h3>
            <h5>Page Number {{pageNumber}} </h5>
        </div>

        <button type="button" class="btn btn-success btn-sm"
        v-on:click="prevPage">Prev Page</button>

        <input type="number" v-model="goToPageNumber"/>
        <button type="button" class="btn btn-success btn-sm"
        v-on:click="goToPage(goToPageNumber)">Go to Page</button>

        <button type="button" class="btn btn-success btn-sm"
        v-on:click="nextPage">Next Page</button>
        <!-- Assuming the csv headers are fixed,
        and that we dont handle files that are not of this format -->
        <table class="table table-hover">
            <tr>
                <th scope="col">Index</th>
                <th scope="col">GUID</th>
                <th scope="col">Name</th>
                <th scope="col">First</th>
                <th scope="col">Last</th>
                <th scope="col">Email</th>
                <th scope="col">Value</th>
                <th scope="col">Date</th>
                <th scope="col">Phone</th>
                <th scope="col">Age</th>
                <th scope="col">State</th>
                <th scope="col">Street</th>
            </tr>
            <tbody>
            <tr v-for="(row, index) in csvFileData" :key="index">
                <td>{{ (index + 1) + (500 * pageNumber) }}</td>
                <td>{{ row.guid }}</td>
                <td>{{ row.name }}</td>
                <td>{{ row.first }}</td>
                <td>{{ row.last }}</td>
                <td>{{ row.email }}</td>
                <td>{{ row.value }}</td>
                <td>{{ row.date }}</td>
                <td>{{ row.phone }}</td>
                <td>{{ row.age }}</td>
                <td>{{ row.state }}</td>
                <td>{{ row.street }}</td>
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
      csvFileData: [],
      fileName: route.params.name,
      pageNumber: 0,
      goToPageNumber: null,
    };
  },

  methods: {
    getCsvfile() {
      const path = `/csv/view/${this.fileName}/${this.pageNumber}`;
      axiosInstance.get(path)
        .then((res) => {
          this.csvFileData = res.data.csvContentList;
          if (res.data.pageNumber - 1 !== this.pageNumber) {
            this.pageNumber = res.data.pageNumber - 1;
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    nextPage() {
      this.pageNumber++;
      this.getCsvfile();
    },

    goToPage(goToPageNumber) {
      this.pageNumber = goToPageNumber;
      this.getCsvfile();
    },

    prevPage() {
      if (this.pageNumber > 0) {
        this.pageNumber--;
        this.getCsvfile();
      }
    },

    goHome() {
      router.push({ name: 'CsvHome' });
    },
  },
  created() {
    this.getCsvfile();
  },
};
</script>
