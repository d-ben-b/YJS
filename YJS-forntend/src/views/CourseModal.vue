<template>
  <div class="modal-overlay" v-if="show">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ isEditing ? "編輯課程" : "新增課程" }}</h3>
        <button class="close-btn" @click="$emit('close')">✖</button>
      </div>
      <form @submit.prevent="submitForm">
        <div class="form-row">
          <div class="form-group">
            <label>課程名稱</label>
            <input type="text" v-model="localFormData.course_name" required />
          </div>

          <div class="form-group">
            <label>教育訓練類型</label>
            <select v-model="localFormData.training_type_name">
              <option value="" disabled>選擇類型</option>
              <option
                v-for="(type, index) in trainingTypes"
                :key="index"
                :value="type">
                {{ type }}
              </option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>部門</label>
            <select v-model="localFormData.department_name">
              <option value="" disabled>選擇部門</option>
              <option v-for="(item, index) in department" :key="index">
                {{ item }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>單位</label>
            <select v-model="localFormData.unit_name">
              <option value="" disabled>選擇單位</option>
              <option v-for="(item, index) in unit" :key="index">
                {{ item }}
              </option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>工作項目</label>
            <select v-model="localFormData.work_item_name">
              <option value="" disabled>選擇項目</option>
              <option v-for="(item, index) in relateWorkItems" :key="index">
                {{ item }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <div v-if="upload.length > 0">
              <label>課程檔案</label>
            </div>
          </div>
        </div>

        <div class="start form-row">
          <div class="form-group">
            <label>SOP/SIP</label>
            <textarea v-model="localFormData.sop_sip"></textarea>
          </div>
          <div class="form-group">
            <div class="form-row">
              <div class="image-upload-container">
                <!-- 預覽已上傳的圖片 -->
                <div
                  v-for="(file, index) in uploadedFiles"
                  :key="index"
                  class="image-preview">
                  <img :src="file.preview" :alt="'圖片' + (index + 1)" />
                  <button class="remove-btn" @click="removeImage(index)">
                    ✖
                  </button>
                </div>

                <!-- 新增圖片按鈕 -->
                <div class="add-image" @click="triggerFileInput">
                  <br />
                  <span>+</span>
                  <p>新增圖片</p>
                  <input
                    type="file"
                    ref="fileInput"
                    accept="image/*"
                    @change="handleFileUpload"
                    style="display: none" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full">
            <label>教學重點</label>
            <textarea
              v-model="localFormData.key_points"
              class="full"></textarea>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full">
            <label>評量項目與標準</label>
            <textarea
              v-model="localFormData.evaluation_criteria"
              class="full"></textarea>
          </div>
        </div>

        <div class="form-actions">
          <base-button buttonType="edit">
            {{ isEditing ? "儲存" : "新增" }}
          </base-button>
          <base-button
            buttonType="delete"
            @click="$emit('close')"
            :buttonBackground="true">
            取消</base-button
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch } from "vue";

  const props = defineProps(["show", "isEditing", "formData", "allCourses"]);
  const localFormData = ref({ ...props.formData });
  const allData = ref([]);
  const trainingTypes = ref([]);
  const relateWorkItems = ref([]);
  const upload = ref([]);
  const unit = ref([]);
  const department = ref([]);
  const uploadedFiles = ref([]);
  const fileInput = ref(null);
  const emit = defineEmits(["submit", "close"]);

  watch(
    () => props.formData,
    (newVal) => {
      localFormData.value = { ...newVal };
      allData.value = [...props.allCourses];
      findTrainingTypes();
    }
  );
  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    files.forEach((file) => {
      const preview = URL.createObjectURL(file);
      uploadedFiles.value.push({ file, preview });
    });
  };

  const removeImage = (index) => {
    const file = uploadedFiles.value[index];
    URL.revokeObjectURL(file.preview); // 釋放資源
    uploadedFiles.value.splice(index, 1);
  };

  const triggerFileInput = () => {
    fileInput.value.click(); // 觸發隱藏的檔案輸入框
  };

  const submitForm = () => {
    const data = { ...localFormData.value };
    if (uploadedFiles.value.length > 0) {
      data.uploadedFiles = uploadedFiles.value; // 將所有圖片檔案附加到資料中
    }
    emit("submit", data);
  };

  const findTrainingTypes = () => {
    const mapToUnique = (key) => [
      ...new Set(allData.value.map((course) => course[key])),
    ];

    trainingTypes.value = mapToUnique("training_type_name");
    relateWorkItems.value = mapToUnique("work_item_name");
    unit.value = mapToUnique("unit_name");
    department.value = mapToUnique("department_name");
  };
</script>

<style scoped>
  .full {
    width: 100%;
    height: 65px;
  }
  .start {
    justify-content: flex-start !important;
  }
  .modal-overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 70px;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    z-index: 1000;
  }

  .modal {
    position: relative;
    background: #fff;
    padding: 20px 39px;
    width: 707px;
    height: 547px;
    top: 109px;
    left: 110px;
    border-radius: 31px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  }

  .modal-header {
    color: #666666;
    height: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
  }
  .modal-header h3 {
    font-size: 20px;
    font-weight: 700;
    line-height: 24.2px;
    text-align: left;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    margin: 0;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }

  .form-group {
    display: flex;
    flex-wrap: nowrap;
    margin-bottom: 15px;
    align-items: center;
  }

  .form-group label {
    width: 100px;
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    margin-right: 10px;
  }

  input,
  textarea,
  select {
    width: 184px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    resize: none;
  }
  .form-row {
    display: flex;
    gap: 20px;
    justify-content: space-between;
    margin-bottom: 10px;
    width: 100%;
  }

  .form-actions {
    display: flex;
    justify-content: flex-start;
    gap: 10px;
  }

  .save-btn,
  .cancel-btn {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .save-btn {
    background-color: #4caf50;
    color: white;
  }

  .cancel-btn {
    background-color: #f44336;
    color: white;
  }
  .image-upload-container {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }

  .image-preview {
    position: relative;
    width: 74px;
    height: 58px;
    border: 1px solid #ccc;
    border-radius: 4px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .image-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .remove-btn {
    position: absolute;
    top: 2px;
    right: 2px;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 12px;
    width: 18px;
    height: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }

  .add-image {
    width: 74px;
    height: 58px;
    border: 1px dashed #ccc;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #666;
    cursor: pointer;
    font-size: 14px;
  }

  .add-image span {
    font-size: 20px;
    font-weight: bold;
  }
  .add-image p {
    margin-top: 0;
  }

  .add-image:hover {
    background-color: #f9f9f9;
  }
</style>
