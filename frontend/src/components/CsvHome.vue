<template>
    <div class="container">
        <h1>CSV Application</h1>
        <hr>
        <button type="button" class="btn btn-success btn-sm"
        v-on:click="pickFile">Upload CSV File</button>
        <input
            type="file"
            style="display: none"
            ref="fileInput"
            accept=".csv"
            v-on:change="uploadFile"
        />
        <div v-if="uploadedFileName != null">
             <h3>Uploaded File</h3>
             <p>{{ uploadedFileName }}</p>
        </div>
        <h3>Previous Uploads</h3>
        <table class="table table-hover">
            <tr>
                <th scope="col">Date</th>
                <th scope="col">Name</th>
            </tr>
            <tbody>
            <tr v-for="(csvFile, index) in csvDataList" :key="index">
                <td>{{ csvFile.date }}</td>
                <td>{{ csvFile.name }}</td>
                <td>
                <button type="button" class="btn btn-info btn-sm"
                  v-on:click="viewFile(csvFile.name)">View</button>
                <button type="button" class="btn btn-info btn-sm"
                  v-on:click="deleteFile(csvFile.name)">Delete</button>
                <button type="button" class="btn btn-danger btn-sm"
                  v-on:click="downloadCsvFile(csvFile.name)">Download</button>
                <button type="button" class="btn btn-danger btn-sm"
                  v-on:click="viewStats(csvFile.name)">Stats</button>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<!--
ToDo: I don't like having JS in the same file like this.
--
Keeping styling, JS and HTML in one file is a Vue style,
I'm going to trust the framework's design for now.
See Mark Coopers answer here:
https://stackoverflow.com/questions/48185655/can-we-keep-html-js-and-css-files-separate-while-creating-vue-js-components-lik
-->

<script>
import axios from 'axios';
import router from '@/router';

const axiosInstance = axios.create({ baseURL: 'http://localhost:5000' });

export default {
  data() {
    return {
      csvDataList: [],
      uploadedFileName: null,
    };
  },

  methods: {
    getCsvFiles() {
      const path = '/csv';
      axiosInstance.get(path)
        .then((res) => {
          this.csvDataList = res.data.csvDataList;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    pickFile() {
      this.$refs.fileInput.click();
    },

    uploadFile(event) {
      // get local file
      const file = event.target.files;
      const fileReader = new FileReader();
      fileReader.addEventListener('load', () => {
        this.fileUrl = fileReader.result;
      });
      fileReader.readAsDataURL(file[0]);
      this.uploadedFileName = file[0].name;

      // upload
      const formData = new FormData();
      formData.append(this.uploadedFileName, file[0]);
      const path = '/csv';
      axiosInstance.post(path, formData)
        .then(() => {
          this.getCsvFiles();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    viewFile(name) {
      console.log(name);
      router.push({ name: 'ViewCsv', params: { name } });
    },

    deleteFile(name) {
      const path = `/csv/delete/${name}`;
      axiosInstance.delete(path)
        .then(() => {
          this.getCsvFiles();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    downloadCsvFile(name) {
      const path = `/csv/download/${name}`;
      axiosInstance.get(path, {
        responseType: 'blob',
      })
        .then((res) => {
          const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/csv' }));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', name);
          document.body.appendChild(link);
          link.click();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    viewStats(name) {
      console.log(name);
      router.push({ name: 'StatsCsv', params: { name } });
    },
  },

  created() {
    this.getCsvFiles();
  },
};
</script>
