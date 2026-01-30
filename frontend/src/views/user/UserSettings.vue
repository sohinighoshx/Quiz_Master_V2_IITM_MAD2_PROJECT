<template>
  <div class="user-settings">
    <!-- Header -->
    <div class="page-header">
      <h1>⚙️ User Settings</h1>
      <p>Customize your study space to match your style</p>
    </div>

    <div class="settings-grid">
      <!-- Left Column -->
      <div class="left-column">
        <!-- Profile Settings -->
        <div class="settings-card">
          <div class="card-header">
            <i class="bi bi-person-circle"></i>
            <h3>Profile Settings</h3>
          </div>
          <div class="card-body">
            <div class="form-group">
              <label><i class="bi bi-person"></i> Full Name</label>
              <input 
                v-model="profile.full_name" 
                placeholder="Enter your full name"
              />
              <small>This name will be displayed across the platform</small>
            </div>

            <div class="form-group">
              <label><i class="bi bi-envelope"></i> Email Address</label>
              <input 
                v-model="profile.email" 
                disabled
              />
              <small>Email cannot be changed</small>
            </div>

            <div class="form-group">
              <label><i class="bi bi-award"></i> Qualification</label>
              <input 
                v-model="profile.qualification" 
                placeholder="e.g., Bachelor of Computer Science"
              />
              <small>Your current academic or professional qualification</small>
            </div>

            <button 
              class="save-btn"
              @click="saveProfile"
              :disabled="isSaving"
            >
              <i class="bi" :class="isSaving ? 'bi-hourglass' : 'bi-check-circle'"></i>
              {{ isSaving ? 'Saving...' : 'Save Profile' }}
            </button>
          </div>
        </div>

        <!-- Theme Settings -->
        <div class="settings-card">
          <div class="card-header">
            <i class="bi bi-palette"></i>
            <h3>Theme & Appearance</h3>
          </div>
          <div class="card-body">
            <div class="theme-options">
              <button 
                class="theme-btn"
                :class="{ active: currentTheme === 'light' }"
                @click="setTheme('light')"
              >
                <i class="bi bi-sun"></i>
                <span>Light</span>
              </button>
              <button 
                class="theme-btn"
                :class="{ active: currentTheme === 'dark' }"
                @click="setTheme('dark')"
              >
                <i class="bi bi-moon"></i>
                <span>Dark</span>
              </button>
              <button 
                class="theme-btn"
                :class="{ active: currentTheme === 'auto' }"
                @click="setTheme('auto')"
              >
                <i class="bi bi-circle-half"></i>
                <span>Auto</span>
              </button>
            </div>
            <p class="theme-hint">Choose your preferred theme mode</p>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="right-column">
        <!-- Background Settings -->
        <div class="settings-card">
          <div class="card-header">
            <i class="bi bi-image"></i>
            <h3>Dashboard Background</h3>
          </div>
          <div class="card-body">
            <!-- Preview -->
            <div class="preview-section">
              <label>Current Background Preview</label>
              <div class="preview-container" @click="triggerFileInput">
                <div v-if="!backgroundUrl" class="default-preview">
                  <i class="bi bi-gradient"></i>
                  <p>Default Gradient Background</p>
                  <small>Click to upload your own image</small>
                </div>
                <div v-else class="image-preview">
                  <img :src="backgroundUrl" alt="Current Background" />
                  <div class="preview-overlay">
                    <span>Current Background</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Upload Controls -->
            <div class="upload-section">
              <label><i class="bi bi-cloud-upload"></i> Upload New Background</label>
              <div class="upload-controls">
                <input
                  type="file"
                  accept="image/*"
                  @change="handleBackgroundUpload"
                  ref="bgInput"
                  hidden
                />
                <button class="upload-btn" @click="triggerFileInput">
                  <i class="bi bi-folder2-open"></i>
                  Choose Image
                </button>
                <div class="file-info" v-if="backgroundFile">
                  <i class="bi bi-file-image"></i>
                  {{ backgroundFile.name }}
                  <button class="clear-btn" @click="clearBackgroundFile">
                    <i class="bi bi-x"></i>
                  </button>
                </div>
              </div>

              <div class="action-buttons">
                <button 
                  class="apply-btn"
                  @click="applyBackground"
                  :disabled="!backgroundUrl || isUploading"
                >
                  <i class="bi" :class="isUploading ? 'bi-hourglass' : 'bi-check2-circle'"></i>
                  {{ isUploading ? 'Applying...' : 'Apply Background' }}
                </button>
                
                <div class="secondary-actions">
                  <button 
                    v-if="backgroundUrl"
                    class="remove-btn"
                    @click="removeBackground"
                  >
                    <i class="bi bi-trash"></i>
                    Remove
                  </button>
                  <button 
                    class="reset-btn"
                    @click="setDefaultBackground"
                    :disabled="!backgroundUrl"
                  >
                    <i class="bi bi-arrow-clockwise"></i>
                    Reset
                  </button>
                </div>
              </div>

              <small class="upload-hint">
                <i class="bi bi-info-circle"></i>
                Recommended: 1920x1080px, JPG/PNG format. Max 5MB.
              </small>
            </div>
          </div>
        </div>

        <!-- Music Settings -->
        <div class="settings-card">
          <div class="card-header">
            <i class="bi bi-music-note-beamed"></i>
            <h3>Study Music</h3>
          </div>
          <div class="card-body">
            <!-- Current Music -->
            <div class="music-preview" v-if="musicUrl">
              <div class="music-info">
                <i class="bi bi-file-music"></i>
                <div>
                  <h4>Your Study Music</h4>
                  <small v-if="musicUploadDate">
                    Uploaded {{ formatDate(musicUploadDate) }}
                  </small>
                </div>
                <button class="delete-btn" @click="removeMusic">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
              <audio :src="musicUrl" controls controlsList="nodownload"></audio>
            </div>
            
            <div v-else class="no-music">
              <i class="bi bi-music-note-list"></i>
              <p>No study music uploaded yet</p>
            </div>

            <!-- Upload Music -->
            <div class="music-upload">
              <label><i class="bi bi-cloud-arrow-up"></i> Upload Music File</label>
              <div class="upload-controls">
                <input
                  type="file"
                  accept="audio/*"
                  @change="handleMusicUpload"
                  ref="musicInput"
                  hidden
                />
                <button class="upload-btn" @click="triggerMusicInput">
                  <i class="bi bi-file-earmark-music"></i>
                  Choose Audio File
                </button>
                <div class="file-info" v-if="musicFile">
                  <i class="bi bi-file-music"></i>
                  {{ musicFile.name }}
                  <button class="clear-btn" @click="clearMusicFile">
                    <i class="bi bi-x"></i>
                  </button>
                </div>
              </div>

              <div class="music-settings">
                <label class="toggle-switch">
                  <input type="checkbox" v-model="autoPlayMusic" />
                  <span class="toggle-slider"></span>
                  <span class="toggle-label">
                    <i class="bi bi-play-circle"></i>
                    Auto-play music on study start
                  </span>
                </label>
              </div>

              <small class="upload-hint">
                <i class="bi bi-info-circle"></i>
                Supports MP3, WAV, OGG formats. Max 10MB.
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <Toast 
      v-if="toast.show" 
      :message="toast.message" 
      :type="toast.type"
      @close="toast.show = false"
    />
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: "UserSettings",
  data() {
    return {
      isSaving: false,
      isUploading: false,
      
      profile: {
        full_name: "",
        email: "",
        qualification: ""
      },

      backgroundUrl: "",
      backgroundFile: null,
      musicUrl: "",
      musicFile: null,
      musicUploadDate: "",
      autoPlayMusic: true,
      currentTheme: 'light',
      
      toast: {
        show: false,
        message: "",
        type: "success"
      }
    };
  },

  async created() {
    await this.loadUserSettings();
  },

  methods: {
    async loadUserSettings() {
      try {
        const { data } = await axios.get("/user/settings");
        this.profile = data;

        // Load background
        const savedBg = localStorage.getItem("user_bg") || data.profile_bg;
        if (savedBg) {
          this.backgroundUrl = savedBg.startsWith('/') ? savedBg : `/${savedBg}`;
          localStorage.setItem("user_bg", this.backgroundUrl);
        }

        // Load music
        const savedMusic = localStorage.getItem("user_music") || data.study_music;
        if (savedMusic) {
          this.musicUrl = savedMusic.startsWith('/') ? savedMusic : `/${savedMusic}`;
          localStorage.setItem("user_music", this.musicUrl);
        }
        
        // Load theme preference
        this.currentTheme = localStorage.getItem("user_theme") || 'light';
        this.applyTheme(this.currentTheme);
        
        // Load autoplay preference
        const savedAutoPlay = localStorage.getItem("music_autoplay");
        this.autoPlayMusic = savedAutoPlay ? JSON.parse(savedAutoPlay) : true;
        
        // Apply background
        if (this.backgroundUrl) {
          this.$emit('update-background', this.backgroundUrl);
        }
      } catch (error) {
        console.error("Failed to load settings:", error);
        this.showToast("Failed to load settings. Please refresh.", "error");
      }
    },

    async saveProfile() {
      if (!this.profile.full_name?.trim()) {
        this.showToast("Please enter your full name", "warning");
        return;
      }

      this.isSaving = true;
      try {
        await axios.put("/user/settings/profile", this.profile);
        this.showToast("Profile updated successfully!");
      } catch (error) {
        console.error("Failed to save profile:", error);
        this.showToast("Failed to update profile. Please try again.", "error");
      } finally {
        this.isSaving = false;
      }
    },

    triggerFileInput() {
      this.$refs.bgInput.click();
    },

    triggerMusicInput() {
      this.$refs.musicInput.click();
    },

    handleBackgroundUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      if (!this.validateFile(file, ['image'], 5)) {
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        this.backgroundUrl = e.target.result;
        this.backgroundFile = file;
        this.showToast("Background preview loaded. Click 'Apply' to save.");
      };
      reader.onerror = () => {
        this.showToast("Failed to load image. Please try another file.", "error");
      };
      reader.readAsDataURL(file);
    },

    async applyBackground() {
      if (!this.backgroundUrl) {
        this.showToast("Please select a background image first", "warning");
        return;
      }

      this.isUploading = true;
      
      try {
        if (this.backgroundFile) {
          const formData = new FormData();
          formData.append("file", this.backgroundFile);

          const { data } = await axios.post("/user/settings/background", formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          
          this.backgroundUrl = data.background;
          this.backgroundFile = null;
        }
        
        localStorage.setItem("user_bg", this.backgroundUrl);
        this.$emit('update-background', this.backgroundUrl);
        this.showToast("Background applied successfully!");
        
        if (this.$refs.bgInput) {
          this.$refs.bgInput.value = '';
        }
      } catch (error) {
        console.error("Failed to upload background:", error);
        this.showToast("Failed to upload background. Please try again.", "error");
      } finally {
        this.isUploading = false;
      }
    },

    removeBackground() {
      if (!confirm("Remove background image?")) return;
      
      localStorage.removeItem("user_bg");
      this.backgroundUrl = "";
      this.backgroundFile = null;
      this.$emit('update-background', null);
      
      axios.delete("/user/settings/background").catch(() => {});
      this.clearFileInput();
      this.showToast("Background removed.");
    },

    clearBackgroundFile() {
      this.backgroundFile = null;
      this.$refs.bgInput.value = '';
    },

    setDefaultBackground() {
      if (confirm("Reset to default gradient background?")) {
        this.removeBackground();
      }
    },

    async handleMusicUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      if (!this.validateFile(file, ['audio'], 10)) {
        return;
      }

      try {
        const formData = new FormData();
        formData.append("file", file);

        const { data } = await axios.post("/user/settings/music", formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        
        this.musicUrl = `/${data.music}`;
        this.musicUploadDate = new Date().toISOString();
        localStorage.setItem("user_music", this.musicUrl);
        this.showToast("Music uploaded successfully!");
        
      } catch (error) {
        console.error("Failed to upload music:", error);
        this.showToast("Failed to upload music. Please try again.", "error");
      }
    },

    removeMusic() {
      if (!confirm("Remove study music?")) return;
      
      localStorage.removeItem("user_music");
      this.musicUrl = "";
      this.musicFile = null;
      
      axios.delete("/user/settings/music").catch(() => {});
      this.clearMusicInput();
      this.showToast("Study music removed.");
    },

    clearMusicFile() {
      this.musicFile = null;
      this.$refs.musicInput.value = '';
    },

    clearFileInput() {
      if (this.$refs.bgInput) {
        this.$refs.bgInput.value = '';
      }
    },

    clearMusicInput() {
      if (this.$refs.musicInput) {
        this.$refs.musicInput.value = '';
      }
    },

    setTheme(theme) {
      this.currentTheme = theme;
      localStorage.setItem("user_theme", theme);
      this.applyTheme(theme);
      this.showToast(`Theme changed to ${theme} mode`);
    },

    applyTheme(theme) {
      const html = document.documentElement;
      
      if (theme === 'dark') {
        html.classList.add('dark-theme');
        html.classList.remove('light-theme');
      } else if (theme === 'light') {
        html.classList.add('light-theme');
        html.classList.remove('dark-theme');
      } else {
        html.classList.remove('dark-theme', 'light-theme');
      }
    },

    validateFile(file, allowedTypes, maxSizeMB) {
      const fileType = allowedTypes.includes('image') ? 'image/' : 'audio/';
      
      if (!file.type.startsWith(fileType)) {
        this.showToast(`Please upload a ${allowedTypes[0]} file`, "warning");
        return false;
      }

      if (file.size > maxSizeMB * 1024 * 1024) {
        this.showToast(`File size should be less than ${maxSizeMB}MB`, "warning");
        return false;
      }

      return true;
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    showToast(message, type = "success") {
      this.toast = { show: true, message, type };
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    }
  },

  watch: {
    autoPlayMusic(newVal) {
      localStorage.setItem("music_autoplay", JSON.stringify(newVal));
    }
  }
};
</script>

<style scoped>
.user-settings {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.page-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(45deg, #007bff, #6610f2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

/* Layout */
.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Cards */
.settings-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.settings-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.card-header {
  background: linear-gradient(135deg, #007bff, #6610f2);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-header i {
  font-size: 1.5rem;
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.card-body {
  padding: 2rem;
}

/* Form Elements */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-group input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
}

.form-group small {
  display: block;
  margin-top: 0.5rem;
  color: #6c757d;
  font-size: 0.875rem;
}

/* Buttons */
.save-btn,
.apply-btn,
.upload-btn,
.theme-btn {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.save-btn {
  background: linear-gradient(135deg, #007bff, #6610f2);
  color: white;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.apply-btn {
  background: #17a2b8;
  color: white;
}

.apply-btn:hover:not(:disabled) {
  background: #138496;
  transform: translateY(-2px);
}

.upload-btn {
  background: #6c757d;
  color: white;
}

.upload-btn:hover {
  background: #5a6268;
}

.theme-btn {
  background: #f8f9fa;
  color: #333;
  border: 2px solid #e9ecef;
}

.theme-btn:hover {
  border-color: #007bff;
}

.theme-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

/* Theme Options */
.theme-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.theme-hint {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0;
}

/* Preview */
.preview-container {
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  margin: 1rem 0;
  transition: transform 0.3s ease;
}

.preview-container:hover {
  transform: scale(1.02);
}

.default-preview {
  background: linear-gradient(135deg, #6610f2 0%, #007bff 50%, #00d4ff 100%);
  color: white;
  padding: 3rem 2rem;
  text-align: center;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.default-preview i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.default-preview p {
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.default-preview small {
  opacity: 0.8;
}

.image-preview {
  position: relative;
  height: 200px;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-preview:hover .preview-overlay {
  opacity: 1;
}

.preview-overlay span {
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

/* Upload Section */
.upload-controls {
  margin: 1rem 0;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8f9fa;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.clear-btn {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  margin-left: auto;
}

.clear-btn:hover {
  color: #dc3545;
}

.action-buttons {
  margin: 1.5rem 0;
}

.secondary-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.remove-btn,
.reset-btn {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  background: white;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.remove-btn:hover {
  border-color: #dc3545;
  color: #dc3545;
}

.reset-btn:hover:not(:disabled) {
  border-color: #6c757d;
  color: #6c757d;
}

.reset-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Music Section */
.music-preview {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.music-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.music-info i {
  font-size: 2rem;
  color: #007bff;
}

.music-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.music-info small {
  color: #6c757d;
}

.delete-btn {
  margin-left: auto;
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
}

.delete-btn:hover {
  background: rgba(220, 53, 69, 0.1);
}

audio {
  width: 100%;
  border-radius: 8px;
}

.no-music {
  text-align: center;
  padding: 3rem 2rem;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.no-music i {
  font-size: 3rem;
  color: #6c757d;
  margin-bottom: 1rem;
}

.no-music p {
  color: #6c757d;
  margin: 0;
}

/* Toggle Switch */
.toggle-switch {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin: 1rem 0;
}

.toggle-switch input {
  display: none;
}

.toggle-slider {
  position: relative;
  width: 50px;
  height: 26px;
  background: #ccc;
  border-radius: 34px;
  margin-right: 1rem;
  transition: background 0.3s ease;
}

.toggle-slider:before {
  content: "";
  position: absolute;
  width: 22px;
  height: 22px;
  left: 2px;
  bottom: 2px;
  background: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
}

input:checked + .toggle-slider {
  background: #007bff;
}

input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #333;
  font-weight: 500;
}

/* Upload Hint */
.upload-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6c757d;
  font-size: 0.875rem;
  margin-top: 1rem;
}

/* Responsive */
@media (max-width: 1024px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .user-settings {
    padding: 1rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .card-body {
    padding: 1.5rem;
  }
  
  .theme-options {
    grid-template-columns: 1fr;
  }
  
  .secondary-actions {
    flex-direction: column;
  }
}
</style>