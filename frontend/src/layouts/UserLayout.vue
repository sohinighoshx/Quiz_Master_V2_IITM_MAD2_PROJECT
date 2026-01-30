<template>
  <div class="user-layout">

    <!-- Sidebar -->
    <Sidebar @toggle="handleSidebarToggle" />

    <!-- Main Content -->
    <div :class="['main-content', { collapsed: isSidebarCollapsed }]">
      <router-view />
    </div>

  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";

export default {
  name: "UserLayout",
  components: { Sidebar },

  data() {
    return {
      isSidebarCollapsed: false
    };
  },

  methods: {
    handleSidebarToggle(collapsed) {
      this.isSidebarCollapsed = collapsed;
    }
  }
};
</script>

<style scoped>
.user-layout {
  display: flex;
  min-height: 100vh;
}

/* Main content */
.main-content {
  margin-left: 250px;
  width: calc(100% - 250px);
  background: linear-gradient(135deg, #ff009d, #00aeff);
  transition: all 0.3s ease;
}

.main-content.collapsed {
  margin-left: 80px;
  width: calc(100% - 80px);
}
</style>
