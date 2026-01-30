<template>
  <div class="dashboard-wrapper">
    <Sidebar @toggle="isSidebarCollapsed = $event" />
    
    <div :class="['content-area', { 'sidebar-collapsed': isSidebarCollapsed }]">
      <!-- Header -->
      <div class="header-section">
        <h2 class="fw-bold text-white">📚 Study Notes</h2>
        <p class="opacity-75 text-white">
          Explore public notes curated by subject and chapter
        </p>
      </div>

      <!-- Filters -->
      <div class="filter-card">
        <div class="filter-grid">
          <div class="filter-group">
            <label class="form-label fw-semibold">Subject</label>
            <select 
              v-model="selectedSubject" 
              @change="handleSubjectChange"
              class="form-select"
            >
              <option value="">All Subjects</option>
              <option v-for="s in subjects" :key="s.id" :value="s.id">
                {{ s.name }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label class="form-label fw-semibold">Chapter</label>
            <select 
              v-model="selectedChapter" 
              @change="fetchNotes"
              class="form-select" 
              :disabled="!selectedSubject"
            >
              <option value="">Select chapter</option>
              <option v-for="c in chapters" :key="c.id" :value="c.id">
                {{ c.name }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label class="form-label fw-semibold">Search Content</label>
            <div class="search-wrapper">
              <i class="bi bi-search search-icon"></i>
              <input
                v-model="search"
                type="text"
                class="form-control"
                placeholder="Title or keywords..."
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-grow text-light" role="status"></div>
        <p class="mt-3 fw-light">Retrieving notes...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="!filteredNotes.length" class="empty-state">
        <div class="empty-icon">📂</div>
        <h4 class="text-muted">No notes available</h4>
        <p class="text-muted">
          Try selecting a different subject or chapter to see shared materials.
        </p>
      </div>

      <!-- Notes Grid -->
      <div v-else class="notes-grid">
        <div 
          v-for="note in filteredNotes" 
          :key="note.id" 
          class="note-card"
          @click="openNote(note)"
        >
          <div class="note-header">
            <h5 class="note-title">{{ note.title }}</h5>
            <span class="note-badge">Note</span>
          </div>
          <p class="note-preview">{{ truncate(note.content) }}</p>
          <button class="note-action-btn">
            Open Full Note
          </button>
        </div>
      </div>

      <!-- Note Modal -->
      <NoteModal 
        v-if="activeNote" 
        :note="activeNote" 
        @close="activeNote = null" 
      />
    </div>
  </div>
</template>

<script>
import axios from "@/axios";
import Sidebar from '@/components/Sidebar.vue';
import NoteModal from '@/components/NoteModal.vue';

export default {
  name: "UserReadNotes",
  components: { Sidebar, NoteModal },
  
  data() {
    return {
      isSidebarCollapsed: false,
      subjects: [],
      chapters: [],
      notes: [],
      selectedSubject: "",
      selectedChapter: "",
      search: "",
      loading: false,
      activeNote: null
    };
  },

  async mounted() {
    await this.fetchSubjects();
  },

  computed: {
    filteredNotes() {
      const query = this.search.toLowerCase().trim();
      if (!query) return this.notes;
      
      return this.notes.filter(note => 
        note.title.toLowerCase().includes(query) ||
        note.content.toLowerCase().includes(query)
      );
    }
  },

  methods: {
    async fetchSubjects() {
      try {
        const { data } = await axios.get("/user/subjects");
        this.subjects = data;
      } catch (error) {
        console.error("Failed to fetch subjects:", error);
      }
    },

    async handleSubjectChange() {
      this.selectedChapter = "";
      this.notes = [];
      
      if (!this.selectedSubject) {
        this.chapters = [];
        return;
      }

      try {
        const { data } = await axios.get(`/user/chapters/${this.selectedSubject}`);
        this.chapters = data;
      } catch (error) {
        console.error("Failed to fetch chapters:", error);
        this.chapters = [];
      }
    },

    async fetchNotes() {
      if (!this.selectedChapter) return;
      
      this.loading = true;
      try {
        const { data } = await axios.get(`/user/study_space/${this.selectedChapter}`);
        this.notes = data;
      } catch (error) {
        console.error("Failed to fetch notes:", error);
        this.notes = [];
      } finally {
        this.loading = false;
      }
    },

    openNote(note) {
      this.activeNote = note;
    },

    truncate(text) {
      return text.length > 150 ? text.slice(0, 150) + "..." : text;
    }
  }
};
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.content-area {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
  padding: 2rem;
}

.content-area.sidebar-collapsed {
  margin-left: 80px;
}

/* Header */
.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

/* Filter Card */
.filter-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-select, .form-control {
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-select:focus, .form-control:focus {
  border-color: #4a6cf7;
  box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
  outline: none;
}

/* Search */
.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
  z-index: 10;
}

.search-wrapper .form-control {
  padding-left: 2.5rem;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 4rem 0;
  color: white;
}

/* Empty State */
.empty-state {
  background: white;
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.2;
  margin-bottom: 1rem;
}

/* Notes Grid */
.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

/* Note Card */
.note-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.note-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.note-title {
  color: #333;
  font-weight: 600;
  margin: 0;
  flex: 1;
  font-size: 1.1rem;
}

.note-badge {
  background: rgba(74, 108, 247, 0.1);
  color: #4a6cf7;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-left: 0.5rem;
}

.note-preview {
  color: #666;
  line-height: 1.6;
  flex: 1;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.note-action-btn {
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  width: 100%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.note-action-btn:hover {
  background: #3a5ce5;
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .content-area {
    margin-left: 0 !important;
    padding: 1rem;
  }
  
  .filter-grid {
    grid-template-columns: 1fr;
  }
  
  .notes-grid {
    grid-template-columns: 1fr;
  }
}
</style>