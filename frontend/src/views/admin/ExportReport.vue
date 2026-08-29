<!-- ✅ ExportReport.vue -->
<template>
  <div class="container py-5 text-center">
    <h3>Export Admin Report</h3>
    <button @click="exportCSV" class="btn btn-dark mt-3">Download CSV</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  methods: {
    async exportCSV() {
      const token = localStorage.getItem('token')
      const res = await axios.get('/admin/export', {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'admin_report.csv')
      document.body.appendChild(link)
      link.click()
    }
  }
}
</script>
